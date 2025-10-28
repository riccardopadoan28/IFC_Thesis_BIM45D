"""
Helper per Pagina 2 — IDS (Information Delivery Specification)

Uso: pages/2_IDS - Information Delivery Specification.py
Funzioni:
- validate_ifc_with_ids(model, ids_rules): esegue la validazione IDS
- export_ids_report(results): produce bytes di report (CSV/JSON)
"""

# Commenti in italiano, output per l'utente in inglese

from __future__ import annotations
from typing import Any, Dict, List
import json
import ifcopenshell
import pandas as pd
from ifcopenshell.util import element as ifc_element


def validate_ifc_with_ids(ifc_file: Any, ids_rules: List[Dict[str, Any]]):
    """Valida un modello IFC rispetto a regole IDS semplificate e ritorna un DataFrame."""
    results = []
    try:
        model = ifc_file if hasattr(ifc_file, 'by_type') else ifcopenshell.open(ifc_file)
    except Exception:
        model = ifc_file

    for rule in ids_rules or []:
        class_name = rule.get('ifc_class')
        if not class_name:
            continue
        try:
            elements = model.by_type(class_name) or []
        except Exception:
            elements = []
        if not elements:
            continue
        for obj in elements:
            try:
                psets = ifc_element.get_psets(obj) or {}
            except Exception:
                psets = {}
            for prop_rule in rule.get('properties', []):
                pset_name = prop_rule.get('property_set', '')
                prop_name = prop_rule.get('property_name', '')
                mandatory = prop_rule.get('mandatory', False)
                val = None
                if pset_name:
                    pset_props = psets.get(pset_name)
                    if pset_props is not None:
                        val = pset_props if prop_name == 'ALL' else pset_props.get(prop_name)
                    else:
                        for pn, props in psets.items():
                            if pn.lower() == pset_name.lower():
                                val = props if prop_name == 'ALL' else props.get(prop_name)
                                pset_name = pn
                                break
                else:
                    for pn, props in psets.items():
                        if prop_name == 'ALL':
                            val = props; pset_name = pn; break
                        if prop_name in props:
                            val = props.get(prop_name); pset_name = pn; break
                if val is None and prop_name and hasattr(obj, prop_name):
                    try:
                        val = getattr(obj, prop_name)
                    except Exception:
                        val = None
                is_valid = (val is not None) if mandatory else True
                element_id = getattr(obj, 'GlobalId', None) or getattr(obj, 'GlobalID', None)
                if element_id is None:
                    try:
                        element_id = obj.id()
                    except Exception:
                        element_id = None
                results.append({
                    'ElementID': element_id,
                    'ElementName': getattr(obj, 'Name', None) or '(Unnamed)',
                    'IFCClass': class_name,
                    'PropertySet': pset_name,
                    'PropertyName': prop_name,
                    'Value': val,
                    'Compliant': is_valid
                })
    return pd.DataFrame(results)


def export_ids_report(results: List[Dict[str, Any]], as_json: bool = True) -> bytes:
    """Esporta il risultato della validazione IDS (JSON o CSV semplificato)."""
    if as_json:
        return json.dumps(results or [], ensure_ascii=False, indent=2).encode("utf-8")
    if not results:
        return b""
    headers = sorted({k for r in results for k in r.keys()})
    rows = [",".join(headers)]
    for r in results:
        rows.append(
            ",".join(str(r.get(h, "")) for h in headers)
        )
    return ("\n".join(rows)).encode("utf-8")
