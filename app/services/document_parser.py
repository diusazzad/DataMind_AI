import io
import re
from typing import Dict, List, NamedTuple
import pypdf


class ParsedPage(NamedTuple):
    page_number: int
    text: str


class DocumentChunk(NamedTuple):
    chunk_id: str
    document_id: str
    document_name: str
    page_number: int
    chunk_index: int
    content: str


class DocumentParserService:
    @staticmethod
    def extract_text_pages(file_content: bytes, filename: str) -> List[ParsedPage]:
        """Extracts text page by page from PDF or plain text files."""
        lower_name = filename.lower()
        pages: List[ParsedPage] = []

        if lower_name.endswith('.pdf'):
            try:
                reader = pypdf.PdfReader(io.BytesIO(file_content))
                for i, page in enumerate(reader.pages):
                    extracted = page.extract_text() or ""
                    cleaned = re.sub(r'\s+', ' ', extracted).strip()
                    if cleaned:
                        pages.append(ParsedPage(page_number=i + 1, text=cleaned))
            except Exception as e:
                raise ValueError(f"Failed to parse PDF document '{filename}': {str(e)}")
        elif lower_name.endswith(('.txt', '.md', '.markdown', '.json', '.csv')):
            try:
                text_content = file_content.decode('utf-8')
            except UnicodeDecodeError:
                text_content = file_content.decode('latin1', errors='ignore')

            # Break large text into ~1500 char virtual pages
            paragraphs = text_content.split('\n\n')
            current_page_text = []
            current_len = 0
            page_idx = 1

            for p in paragraphs:
                cleaned_p = p.strip()
                if not cleaned_p:
                    continue
                current_page_text.append(cleaned_p)
                current_len += len(cleaned_p)
                if current_len >= 1500:
                    pages.append(ParsedPage(page_number=page_idx, text="\n\n".join(current_page_text)))
                    page_idx += 1
                    current_page_text = []
                    current_len = 0

            if current_page_text:
                pages.append(ParsedPage(page_number=page_idx, text="\n\n".join(current_page_text)))
        else:
            raise ValueError(f"Unsupported document format: '{filename}'. Supported: .pdf, .txt, .md")

        if not pages:
            raise ValueError(f"No readable text could be extracted from '{filename}'.")

        return pages

    @classmethod
    def chunk_pages(
        cls,
        pages: List[ParsedPage],
        document_id: str,
        document_name: str,
        chunk_size: int = 600,
        chunk_overlap: int = 100
    ) -> List[DocumentChunk]:
        """Splits document pages into semantically bounded overlapping chunks."""
        chunks: List[DocumentChunk] = []
        global_chunk_idx = 0

        for page in pages:
            page_text = page.text
            if len(page_text) <= chunk_size:
                chunks.append(
                    DocumentChunk(
                        chunk_id=f"{document_id}_p{page.page_number}_c{global_chunk_idx}",
                        document_id=document_id,
                        document_name=document_name,
                        page_number=page.page_number,
                        chunk_index=global_chunk_idx,
                        content=page_text
                    )
                )
                global_chunk_idx += 1
                continue

            # Split by sentences or paragraph boundaries
            sentences = re.split(r'(?<=[.!?])\s+', page_text)
            current_chunk = []
            current_length = 0

            for sentence in sentences:
                sentence_len = len(sentence)
                if current_length + sentence_len > chunk_size and current_chunk:
                    chunk_str = " ".join(current_chunk).strip()
                    chunks.append(
                        DocumentChunk(
                            chunk_id=f"{document_id}_p{page.page_number}_c{global_chunk_idx}",
                            document_id=document_id,
                            document_name=document_name,
                            page_number=page.page_number,
                            chunk_index=global_chunk_idx,
                            content=chunk_str
                        )
                    )
                    global_chunk_idx += 1

                    # Retain overlap sentences
                    overlap_chunk = []
                    overlap_len = 0
                    for prev in reversed(current_chunk):
                        if overlap_len + len(prev) <= chunk_overlap:
                            overlap_chunk.insert(0, prev)
                            overlap_len += len(prev)
                        else:
                            break

                    current_chunk = overlap_chunk
                    current_length = sum(len(s) for s in current_chunk)

                current_chunk.append(sentence)
                current_length += sentence_len

            if current_chunk:
                chunk_str = " ".join(current_chunk).strip()
                chunks.append(
                    DocumentChunk(
                        chunk_id=f"{document_id}_p{page.page_number}_c{global_chunk_idx}",
                        document_id=document_id,
                        document_name=document_name,
                        page_number=page.page_number,
                        chunk_index=global_chunk_idx,
                        content=chunk_str
                    )
                )
                global_chunk_idx += 1

        return chunks
