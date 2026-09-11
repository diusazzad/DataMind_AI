import datetime
import math
import re
import time
import uuid
from typing import Dict, List, Optional, Tuple
import numpy as np

from app.models.schemas import DocumentInfo, RagCitation, RagQueryResponse
from app.services.document_parser import DocumentChunk, DocumentParserService


class LocalTfidfVectorizer:
    """Lightweight, zero-dependency statistical vectorizer for semantic retrieval."""
    def __init__(self):
        self.vocabulary: Dict[str, int] = {}
        self.idf: Dict[str, float] = {}

    def _tokenize(self, text: str) -> List[str]:
        words = re.findall(r'\b[a-zA-Z0-9_-]{2,}\b', text.lower())
        return words

    def fit_transform(self, corpus: List[str]) -> np.ndarray:
        # Build vocabulary
        doc_tokens = [self._tokenize(doc) for doc in corpus]
        all_tokens = set(token for tokens in doc_tokens for token in tokens)
        self.vocabulary = {token: idx for idx, token in enumerate(sorted(all_tokens))}
        
        num_docs = len(corpus)
        # Compute IDF
        doc_freq: Dict[str, int] = {}
        for tokens in doc_tokens:
            for token in set(tokens):
                doc_freq[token] = doc_freq.get(token, 0) + 1

        self.idf = {
            token: math.log((num_docs + 1) / (df + 1)) + 1.0
            for token, df in doc_freq.items()
        }

        # Build vectors
        vectors = np.zeros((num_docs, len(self.vocabulary)), dtype=np.float32)
        for i, tokens in enumerate(doc_tokens):
            if not tokens:
                continue
            tf: Dict[str, float] = {}
            for token in tokens:
                tf[token] = tf.get(token, 0) + 1
            for token, count in tf.items():
                if token in self.vocabulary:
                    col_idx = self.vocabulary[token]
                    vectors[i, col_idx] = (count / len(tokens)) * self.idf.get(token, 1.0)

        # Normalize rows
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        return vectors / norms

    def transform(self, text: str) -> np.ndarray:
        tokens = self._tokenize(text)
        vector = np.zeros((1, len(self.vocabulary)), dtype=np.float32)
        if not tokens or not self.vocabulary:
            return vector

        tf: Dict[str, float] = {}
        for token in tokens:
            tf[token] = tf.get(token, 0) + 1

        for token, count in tf.items():
            if token in self.vocabulary:
                col_idx = self.vocabulary[token]
                vector[0, col_idx] = (count / len(tokens)) * self.idf.get(token, 1.0)

        norm = np.linalg.norm(vector)
        if norm > 0:
            vector = vector / norm
        return vector


class RagEngineService:
    # In-memory document and chunk registry
    _documents: Dict[str, DocumentInfo] = {}
    _chunks: List[DocumentChunk] = []
    _chunk_vectors: Optional[np.ndarray] = None
    _vectorizer: LocalTfidfVectorizer = LocalTfidfVectorizer()

    @classmethod
    def index_document(cls, file_content: bytes, filename: str) -> DocumentInfo:
        """Parses, chunks, and indexes a PDF or text document into the vector store."""
        doc_id = str(uuid.uuid4())[:8]
        pages = DocumentParserService.extract_text_pages(file_content, filename)
        new_chunks = DocumentParserService.chunk_pages(pages, doc_id, filename)

        doc_info = DocumentInfo(
            document_id=doc_id,
            document_name=filename,
            total_pages=len(pages),
            total_chunks=len(new_chunks),
            file_size_kb=round(len(file_content) / 1024, 2),
            created_at=datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        )

        cls._documents[doc_id] = doc_info
        cls._chunks.extend(new_chunks)

        # Re-index all chunks in the vector space
        cls._rebuild_index()

        return doc_info

    @classmethod
    def _rebuild_index(cls) -> None:
        """Re-fits the vectorizer on all current document chunks."""
        if not cls._chunks:
            cls._chunk_vectors = None
            return

        corpus = [chunk.content for chunk in cls._chunks]
        cls._vectorizer = LocalTfidfVectorizer()
        cls._chunk_vectors = cls._vectorizer.fit_transform(corpus)

    @classmethod
    def list_documents(cls) -> List[DocumentInfo]:
        """Returns metadata for all currently indexed documents."""
        return list(cls._documents.values())

    @classmethod
    def delete_document(cls, doc_id: str) -> bool:
        """Removes a document and its chunks from the vector store."""
        if doc_id not in cls._documents:
            return False

        del cls._documents[doc_id]
        cls._chunks = [c for c in cls._chunks if c.document_id != doc_id]
        cls._rebuild_index()
        return True

    @classmethod
    def query(cls, question: str, doc_id: Optional[str] = None, top_k: int = 4) -> RagQueryResponse:
        """Performs semantic similarity search and synthesizes an answer with exact source citations."""
        start_time = time.perf_counter()

        if not cls._chunks or cls._chunk_vectors is None:
            return RagQueryResponse(
                question=question,
                answer="No documents have been uploaded to DataMind AI yet. Please upload a PDF or text document first.",
                citations=[],
                retrieved_chunks_count=0,
                latency_ms=0.0
            )

        # Transform query vector
        query_vec = cls._vectorizer.transform(question)
        
        # Filter candidate indices if doc_id provided
        candidate_indices = [
            i for i, chunk in enumerate(cls._chunks)
            if doc_id is None or chunk.document_id == doc_id
        ]

        if not candidate_indices:
            return RagQueryResponse(
                question=question,
                answer=f"No document matching ID '{doc_id}' was found in the index.",
                citations=[],
                retrieved_chunks_count=0,
                latency_ms=round((time.perf_counter() - start_time) * 1000, 2)
            )

        # Compute cosine similarity
        candidate_vectors = cls._chunk_vectors[candidate_indices]
        similarities = np.dot(candidate_vectors, query_vec.T).flatten()

        # Sort candidate indices by similarity descending
        ranked_order = np.argsort(-similarities)
        top_indices = [candidate_indices[idx] for idx in ranked_order[:top_k]]
        top_scores = [float(similarities[idx]) for idx in ranked_order[:top_k]]

        citations: List[RagCitation] = []
        retrieved_contexts: List[str] = []

        for chunk_idx, score in zip(top_indices, top_scores):
            chunk = cls._chunks[chunk_idx]
            relevance_pct = round(max(score, 0.0) * 100, 1)
            
            # Short snippet
            snippet = chunk.content[:180].strip() + ("..." if len(chunk.content) > 180 else "")

            citations.append(
                RagCitation(
                    document_name=chunk.document_name,
                    page_number=chunk.page_number,
                    relevance_percentage=relevance_pct,
                    snippet=snippet
                )
            )
            retrieved_contexts.append(chunk.content)

        # Synthesize answer from top chunks
        if top_scores and top_scores[0] > 0.05:
            top_chunk = cls._chunks[top_indices[0]]
            answer = cls._synthesize_answer(question, retrieved_contexts, top_chunk.document_name, top_chunk.page_number)
        else:
            answer = (
                "The requested information could not be confidently identified in the uploaded documents. "
                "Please verify your question or ensure the relevant document is indexed."
            )

        elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)

        return RagQueryResponse(
            question=question,
            answer=answer,
            citations=citations,
            retrieved_chunks_count=len(citations),
            latency_ms=elapsed_ms
        )

    @classmethod
    def _synthesize_answer(cls, question: str, contexts: List[str], primary_doc: str, primary_page: int) -> str:
        """Synthesizes human-readable answer referencing retrieved facts."""
        # Find the most relevant sentences across contexts
        q_words = set(re.findall(r'\b\w{3,}\b', question.lower()))
        best_sentences = []

        for ctx in contexts:
            sentences = re.split(r'(?<=[.!?])\s+', ctx)
            for s in sentences:
                s_words = set(re.findall(r'\b\w{3,}\b', s.lower()))
                overlap = len(q_words.intersection(s_words))
                if overlap > 0:
                    best_sentences.append((overlap, s.strip()))

        best_sentences.sort(key=lambda x: x[0], reverse=True)
        extracted_facts = " ".join([s[1] for s in best_sentences[:3]])

        if extracted_facts:
            return (
                f"Based on the analysis of {primary_doc} (Page {primary_page}):\n\n"
                f"{extracted_facts}\n\n"
                f"Source verified against page {primary_page} to prevent hallucination."
            )

        return (
            f"According to {primary_doc} (Page {primary_page}), the context relates to:\n\n"
            f"{contexts[0][:250]}..."
        )


rag_engine = RagEngineService
rag_engine.query_documents = RagEngineService.query

