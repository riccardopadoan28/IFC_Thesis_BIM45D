"""
Helper per Pagina 4 — IFC Model Health Checker

Uso: pages/4_ IFC Model Health Checker.py
Funzioni:
- run_health_checks(model): esegue controlli di qualità usando official validators
- build_health_report(results): ritorna un DataFrame/HTML/bytes (qui: JSON bytes)
"""

from __future__ import annotations
from typing import Any, Dict, List
import json

# Import official validation functions
try:
    from tools import validate_ifc as v_ifc
    VALIDATION_AVAILABLE = True
except ImportError:
    VALIDATION_AVAILABLE = False
    v_ifc = None


def run_health_checks(model: Any) -> Dict[str, Any]:
    """Esegue controlli usando official buildingSMART validators."""
    if not VALIDATION_AVAILABLE or v_ifc is None:
        return {
            "error": "Official validation tools not available",
            "results": []
        }
    
    # Run official validations
    results = v_ifc.validate_ifc_from_model(model)
    return results


def build_health_report(results: Dict[str, Any]) -> bytes:
    """Esporta i risultati dei controlli in JSON bytes."""
    return json.dumps(results or {}, ensure_ascii=False, indent=2).encode("utf-8")
