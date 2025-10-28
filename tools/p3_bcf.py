"""
Helper per Pagina 3 — BCF (BIM Collaboration Format)

Uso: pages/3_BCF - BIM Collaboration Format.py
Funzioni:
- create_issue(summary, description): ritorna un dict issue
- export_bcf_zip(issues): ritorna bytes di uno zip BCF semplificato (placeholder)
"""

from __future__ import annotations
from typing import Dict, List
from io import BytesIO
import zipfile
import json


def create_issue(summary: str, description: str = "") -> Dict[str, str]:
    """Crea un oggetto issue semplificato."""
    return {"summary": summary, "description": description}


def export_bcf_zip(issues: List[Dict[str, str]]) -> bytes:
    """Crea un archivio ZIP BCF semplificato contenente un JSON di issues (placeholder)."""
    mem = BytesIO()
    with zipfile.ZipFile(mem, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("issues.json", json.dumps(issues or [], ensure_ascii=False, indent=2))
    return mem.getvalue()
