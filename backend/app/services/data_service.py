from pathlib import Path
import json
from typing import Optional, Dict, Any

from ..models import DiagnosticCode, VehicleInfo


class DataService:
    def __init__(self) -> None:
        base_dir = Path(__file__).resolve().parent.parent
        data_dir = base_dir / "data"
        # Fallback if running from root
        if not data_dir.exists():
            data_dir = Path("backend/data")
        self.diagnostic_codes_path = data_dir / "diagnostic_codes.json"
        self.vehicle_specs_path = data_dir / "vehicle_specs.json"
        self._diagnostic_by_code = self._load_json_index(self.diagnostic_codes_path, key="code")
        self._vehicle_specs = self._load_vehicle_specs(self.vehicle_specs_path)

    def _load_json_index(self, path: Path, key: str) -> Dict[str, Dict[str, Any]]:
        if not path.exists():
            return {}
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        index = {}
        for item in data:
            if key in item:
                index[str(item[key]).upper()] = item
        return index

    def _load_vehicle_specs(self, path: Path) -> Dict[str, Dict[str, Dict[int, Dict[str, Any]]]]:
        # Structure: make -> model -> year -> info
        if not path.exists():
            return {}
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        by_make: Dict[str, Dict[str, Dict[int, Dict[str, Any]]]] = {}
        for item in data:
            make = item.get("make", "").lower()
            model = item.get("model", "").lower()
            year = int(item.get("year"))
            by_make.setdefault(make, {}).setdefault(model, {})[year] = item
        return by_make

    def get_diagnostic_code(self, code: str) -> Optional[DiagnosticCode]:
        if not code:
            return None
        raw = self._diagnostic_by_code.get(code.upper())
        if not raw:
            return None
        return DiagnosticCode(**raw)

    def get_vehicle_info(self, make: str, model: str, year: int) -> Optional[VehicleInfo]:
        make_k = (make or "").lower()
        model_k = (model or "").lower()
        year_i = int(year)
        raw = self._vehicle_specs.get(make_k, {}).get(model_k, {}).get(year_i)
        if not raw:
            return None
        return VehicleInfo(**raw)