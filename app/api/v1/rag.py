from typing import List
from fastapi import APIRouter, File, HTTPException, UploadFile
from app.models.schemas import DocumentInfo, RagQueryRequest, RagQueryResponse, RagUploadResponse
from app.services.rag_engine import RagEngineService

router = APIRouter(prefix="/rag", tags=["Document Intelligence (RAG)"])


@router.post("/upload", response_model=RagUploadResponse)
async def upload_and_index_document(file: UploadFile = File(...)):
    """Upload a PDF, TXT, or Markdown document to parse, chunk, and index into the semantic vector store."""
    if not file.filename:
        raise HTTPException(status_code=400, detail="A valid file with a filename must be provided.")

    content = await file.read()
    if len(content) == 0:
        raise HTTPException(status_code=400, detail="The uploaded document is empty.")

    try:
        doc_info = RagEngineService.index_document(content, file.filename)
        return RagUploadResponse(
            success=True,
            document=doc_info,
            message=f"Successfully indexed '{file.filename}' into {doc_info.total_chunks} semantic chunks across {doc_info.total_pages} pages."
        )
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process document: {str(e)}")


@router.get("/documents", response_model=List[DocumentInfo])
def list_indexed_documents():
    """Returns metadata for all documents currently indexed in the vector store."""
    return RagEngineService.list_documents()


@router.delete("/documents/{document_id}")
def delete_indexed_document(document_id: str):
    """Deletes a document and all its corresponding chunks from the vector store."""
    deleted = RagEngineService.delete_document(document_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Document with ID '{document_id}' not found.")
    return {"success": True, "message": f"Document '{document_id}' successfully removed from vector store."}


@router.post("/query", response_model=RagQueryResponse)
def query_document_knowledge_base(request: RagQueryRequest):
    """Answers questions based on indexed documents with exact source citations (file name and page numbers)."""
    question = request.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    try:
        return RagEngineService.query(
            question=question,
            doc_id=request.document_id,
            top_k=request.top_k
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"RAG query execution error: {str(e)}")
