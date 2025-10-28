"""
Helper per Pagina 8 — 5D Cost Estimation

Uso: pages/8_5D - Cost Estimation.py
Funzioni:
- summarize_quantities(df): calcola un riepilogo per il BOQ
- export_boq_csv(df): esporta il BOQ in CSV bytes
"""

from __future__ import annotations
import pandas as pd


def summarize_quantities(df: pd.DataFrame) -> pd.DataFrame:
    """Esegue un raggruppamento semplice per la stima costi (placeholder)."""
    if df is None or df.empty:
        return pd.DataFrame()
    return df


def export_boq_csv(df: pd.DataFrame) -> bytes:
    """Esporta il BOQ in CSV bytes."""
    return (df or pd.DataFrame()).to_csv(index=False).encode("utf-8")
