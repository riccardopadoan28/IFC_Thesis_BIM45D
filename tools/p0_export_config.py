"""
Helper per Pagina 0 — IFC 4x3 Export Configuration

Uso: funzioni chiamate da pages/0_IFC 4x3 Export Configuration.py
Funzioni previste:
- load_export_config(): carica configurazione di export
- save_export_config(cfg): salva configurazione di export
- export_config_as_json(cfg): restituisce bytes JSON della configurazione

Nota: Questo modulo è indipendente; se altre pagine necessitano funzioni simili, copiarle qui per mantenere un per-pagina unico.
"""

# Tutto l'output visibile all'utente dovrebbe restare in inglese.

from __future__ import annotations
from typing import Any, Dict, Optional
import json

# ─────────────────────────────────────────────────────────
# API principali (safe defaults)
# ─────────────────────────────────────────────────────────

def load_export_config(default: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Carica la configurazione di export (placeholder). Ritorna un dict.
    Se non esiste una sorgente persistente, usa `default` o un dizionario vuoto."""
    return dict(default or {})


def save_export_config(cfg: Dict[str, Any]) -> bool:
    """Salva la configurazione di export (placeholder). Ritorna True se l'operazione è andata a buon fine."""
    # Implementare persistenza se necessario (file/DB). Qui ritorniamo True per compatibilità.
    return True


def export_config_as_json(cfg: Dict[str, Any]) -> bytes:
    """Esporta la configurazione come JSON bytes (UTF-8)."""
    return json.dumps(cfg or {}, ensure_ascii=False, indent=2).encode("utf-8")
