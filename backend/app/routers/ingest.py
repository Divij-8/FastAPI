from typing import List

from fastapi import APIRouter, File, UploadFile, HTTPException

from ..config import get_settings
from ..models import UploadDocumentsResponse
from ..services.rag_service import RagService

router = APIRouter(tags=["ingestion"])

_settings = get_settings()
_rag = RagService(settings=_settings)


@router.post("/upload-documents", response_model=UploadDocumentsResponse)
async def upload_documents(files: List[UploadFile] = File(...)) -> UploadDocumentsResponse:
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")

    pdf_files = []
    filenames = []
    for f in files:
        if f.content_type not in ("application/pdf", "application/octet-stream") and not f.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail=f"Unsupported file type for {f.filename}. Only PDF allowed.")
        content = await f.read()
        pdf_files.append((content, f.filename))
        filenames.append(f.filename)

    try:
        count = _rag.ingest_pdfs(pdf_files)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to ingest documents: {e}")

    return UploadDocumentsResponse(ingested_count=count, files=filenames)