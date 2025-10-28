"""
Helper per Pagina 1 — IFC Import

Uso: funzioni chiamate da pages/1_IFC Import.py
Funzioni previste:
- save_uploaded_file_to_temp(file, temp_dir): salva il file nel temp
- detect_schema(ifc_path): rileva lo schema IFC (stringa tipo 'IFC4X3')
- build_session_state(file_path): produce info utili per la sessione

Nota: modulo auto-contenuto. Copiare funzioni in altri helper se servono altrove.
"""

# L'output utente rimane in inglese; commenti in italiano

from __future__ import annotations
from pathlib import Path
from typing import Dict, Optional
import shutil
import ifcopenshell


def save_uploaded_file_to_temp(src_path: Path, temp_dir: Path) -> Path:
    """Salva/copia il file caricato nella cartella temporanea e ritorna il path di destinazione."""
    temp_dir.mkdir(parents=True, exist_ok=True)
    dst = temp_dir / src_path.name
    if src_path.resolve() != dst.resolve():
        shutil.copyfile(src_path, dst)
    return dst


def detect_schema(ifc_path: Path) -> str:
    """Apre il file IFC e ritorna lo schema (es. 'IFC2X3', 'IFC4', 'IFC4X3')."""
    try:
        m = ifcopenshell.open(str(ifc_path))
        return getattr(m.schema, 'schema_identifier', str(m.schema))
    except Exception:
        return ""


def build_session_state(file_path: Path) -> Dict[str, str]:
    """Costruisce il pacchetto base di informazioni da salvare in sessione."""
    return {
        "file_name": file_path.name,
        "file_path": str(file_path),
    }
