"""
Helper per Pagina 4 — IFC Model Health Checker

Uso: pages/4_ IFC Model Health Checker.py
Funzioni:
- run_health_checks(model): esegue controlli di qualità base (placeholder)
- build_health_report(results): ritorna un DataFrame/HTML/bytes (qui: JSON bytes)
"""

from __future__ import annotations
from typing import Any, Dict, List
import json


def run_health_checks(model: Any) -> List[Dict[str, Any]]:
    """Esegue controlli basilari (placeholder)."""
    return []


def build_health_report(results: List[Dict[str, Any]]) -> bytes:
    """Esporta i risultati dei controlli in JSON bytes."""
    return json.dumps(results or [], ensure_ascii=False, indent=2).encode("utf-8")
