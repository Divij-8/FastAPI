from pydantic import BaseModel, Field
from typing import List, Optional, Dict


class HealthResponse(BaseModel):
    status: str = Field(..., description="Service health status")
    version: Optional[str] = Field(default=None, description="Application version")
    environment: Optional[str] = None


class VehicleInfo(BaseModel):
    make: str
    model: str
    year: int
    engine: Optional[str] = None
    transmission: Optional[str] = None
    specs: Optional[Dict[str, str]] = None


class DiagnosticCode(BaseModel):
    code: str
    name: str
    description: str
    symptoms: List[str] = []
    possible_causes: List[str] = []
    troubleshooting_steps: List[str] = []


class QueryVehicleContext(BaseModel):
    make: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None


class QueryRequest(BaseModel):
    query: str
    top_k: int = Field(default=4, ge=1, le=10)
    vehicle: Optional[QueryVehicleContext] = None


class Source(BaseModel):
    text: str
    source: Optional[str] = None
    page: Optional[int] = None
    score: Optional[float] = None


class QueryResponse(BaseModel):
    answer: str
    sources: List[Source] = []
    suggested_actions: Optional[List[str]] = None


class UploadDocumentsResponse(BaseModel):
    ingested_count: int
    files: List[str] = []


class ErrorResponse(BaseModel):
    detail: str