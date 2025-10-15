from fastapi import APIRouter, HTTPException

from ..config import get_settings
from ..models import QueryRequest, QueryResponse, Source
from ..services.rag_service import RagService

router = APIRouter(tags=["query"])

_settings = get_settings()
_rag = RagService(settings=_settings)


@router.post("/query", response_model=QueryResponse)
def query_rag(payload: QueryRequest) -> QueryResponse:
    if not payload.query or not payload.query.strip():
        raise HTTPException(status_code=400, detail="Query text is required")

    vehicle = payload.vehicle.model_dump() if payload.vehicle else None
    try:
        answer, sources = _rag.query(payload.query, top_k=payload.top_k, vehicle=vehicle)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {e}")

    return QueryResponse(
        answer=answer,
        sources=[Source(**s) for s in sources],
    )