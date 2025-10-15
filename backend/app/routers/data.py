from fastapi import APIRouter, HTTPException

from ..services.data_service import DataService
from ..models import DiagnosticCode, VehicleInfo

router = APIRouter(prefix="", tags=["data"])

_data_service = DataService()


@router.get("/diagnostic-codes/{code}", response_model=DiagnosticCode)
def get_diagnostic_code(code: str) -> DiagnosticCode:
    data = _data_service.get_diagnostic_code(code)
    if not data:
        raise HTTPException(status_code=404, detail="Diagnostic code not found")
    return data


@router.get("/vehicle-info/{make}/{model}/{year}", response_model=VehicleInfo)
def get_vehicle_info(make: str, model: str, year: int) -> VehicleInfo:
    data = _data_service.get_vehicle_info(make, model, year)
    if not data:
        raise HTTPException(status_code=404, detail="Vehicle info not found")
    return data