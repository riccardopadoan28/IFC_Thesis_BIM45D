"""
Helper per Pagina 2 — IDS (Information Delivery Specification)

Uso: pages/2_IDS - Information Delivery Specification.py
Funzioni:
- validate_ifc_with_ids(model, ids_rules): esegue la validazione IDS
- export_ids_report(results): produce bytes di report (CSV/JSON)
- audit_ids_xml(xml_bytes): valida l'IDS XML (IDS-Audit-tool se disponibile, altrimenti XSD)
- validate_ifc_with_ids_xml_official(ifc_file, ids_xml_bytes): prova a usare il validator ufficiale via CLI
"""

# Commenti in italiano, output per l'utente in inglese

from __future__ import annotations
from typing import Any, Dict, List, Tuple, Optional
import json
import io
import os
import tempfile
import subprocess
import xml.etree.ElementTree as ET

import ifcopenshell
import pandas as pd
from ifcopenshell.util import element as ifc_element


# ------------------------------
# Utility: genera un IDS XML minimo da regole semplificate
# ------------------------------
def ids_rules_to_xml(ids_rules: List[Dict[str, Any]], title: str = "Dynamic IDS", ifc_version: str = "IFC4X3") -> str:
    ns = {
        'xs': 'http://www.w3.org/2001/XMLSchema',
        'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
        'ids': 'http://standards.buildingsmart.org/IDS'
    }
    ET.register_namespace('xs', ns['xs'])
    ET.register_namespace('xsi', ns['xsi'])
    ET.register_namespace('ids', ns['ids'])

    root = ET.Element(f"{{{ns['ids']}}}ids", {
        f"{{{ns['xsi']}}}schemaLocation": "http://standards.buildingsmart.org/IDS http://standards.buildingsmart.org/IDS/1.0/ids.xsd"
    })
    info = ET.SubElement(root, f"{{{ns['ids']}}}info")
    ET.SubElement(info, f"{{{ns['ids']}}}title").text = title
    ET.SubElement(info, f"{{{ns['ids']}}}version").text = "1.0"

    specs = ET.SubElement(root, f"{{{ns['ids']}}}specifications")
    for idx, rule in enumerate(ids_rules or []):
        spec = ET.SubElement(specs, f"{{{ns['ids']}}}specification", {
            'ifcVersion': ifc_version,
            'name': f"Requirement for {rule.get('ifc_class', '')}",
            'identifier': f"S{idx+1}"
        })
        appl = ET.SubElement(spec, f"{{{ns['ids']}}}applicability", {'minOccurs': '0', 'maxOccurs': 'unbounded'})
        entity = ET.SubElement(appl, f"{{{ns['ids']}}}entity")
        name_el = ET.SubElement(entity, f"{{{ns['ids']}}}name")
        ET.SubElement(name_el, f"{{{ns['ids']}}}simpleValue").text = rule.get('ifc_class', '')

        reqs = ET.SubElement(spec, f"{{{ns['ids']}}}requirements")
        for prop in rule.get('properties', []):
            prop_name = prop.get('property_name', '')
            pset = prop.get('property_set', '')
            prop_el = ET.SubElement(reqs, f"{{{ns['ids']}}}property", {
                'dataType': 'IFCLABEL',
                'cardinality': 'required' if prop.get('mandatory', False) else 'optional'
            })
            pset_el = ET.SubElement(prop_el, f"{{{ns['ids']}}}propertySet")
            ET.SubElement(pset_el, f"{{{ns['ids']}}}simpleValue").text = pset
            base_el = ET.SubElement(prop_el, f"{{{ns['ids']}}}baseName")
            ET.SubElement(base_el, f"{{{ns['ids']}}}simpleValue").text = prop_name

            allowed = prop.get('allowed_values') or prop.get('values')
            if allowed:
                value_el = ET.SubElement(prop_el, f"{{{ns['ids']}}}value")
                restr = ET.SubElement(value_el, f"{{{ns['xs']}}}restriction", {'base': 'xs:string'})
                for v in allowed:
                    ET.SubElement(restr, f"{{{ns['xs']}}}enumeration", {'value': str(v)})

    return ET.tostring(root, encoding='utf-8').decode('utf-8')


# ------------------------------
# IDS Audit: usa IDS-Audit-tool se presente, altrimenti valida con XSD
# ------------------------------
def audit_ids_xml(xml_bytes: bytes) -> Tuple[bool, str]:
    """Valida un IDS XML. Ritorna (ok, report_text)."""
    # 1) Try IDS-Audit CLI tool (buildingSMART official .NET tool)
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".ids") as f:
            f.write(xml_bytes)
            f.flush()
            temp_ids = f.name
        try:
            proc = subprocess.run(
                ["ids-audit", temp_ids, "--format", "json"],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False
            )
            if proc.returncode == 0 and proc.stdout:
                return True, proc.stdout
            # if audit tool returns non-zero, still show its output
            if proc.stdout or proc.stderr:
                return False, proc.stdout or proc.stderr
        finally:
            try:
                os.unlink(temp_ids)
            except Exception:
                pass
    except FileNotFoundError:
        pass  # CLI non presente, continuiamo con XSD
    except Exception as e:
        # errore inaspettato nel CLI
        return False, f"IDS-Audit-tool error: {e}"

    # 2) Fallback: XSD validation
    try:
        import xmlschema
        schema = xmlschema.XMLSchema("http://standards.buildingsmart.org/IDS/1.0/ids.xsd")
        is_valid = schema.is_valid(io.BytesIO(xml_bytes))
        if is_valid:
            return True, "XML is valid against IDS XSD (fallback)."
        # collect errors
        errors = []
        for e in schema.iter_errors(io.BytesIO(xml_bytes)):
            errors.append(str(e))
        return False, "\n".join(errors[:50])
    except Exception as e:
        return False, f"XSD validation failed: {e}"


# ------------------------------
# Validator ufficiale via CLI 'validate' (buildingSMART/validate)
# ------------------------------

def _ensure_ifc_path(ifc_file: Any) -> str:
    if hasattr(ifc_file, 'by_type'):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".ifc") as f:
            path = f.name
        try:
            ifc_file.write(path)
        except Exception:
            # ultimo tentativo: serializzare come stringa
            try:
                with open(path, 'wb') as fw:
                    fw.write(str(ifc_file).encode('utf-8'))
            except Exception:
                raise
        return path
    if isinstance(ifc_file, str):
        return ifc_file
    raise ValueError("Unsupported IFC input. Provide an ifcopenshell model or file path.")


def _run_validate_cli(ids_path: str, ifc_path: str) -> Tuple[bool, Optional[str], Optional[str]]:
    candidates = [
        ["validate", "ids", "--format", "json", ids_path, ifc_path],
        ["validate", "--format", "json", "ids", ids_path, ifc_path],
        ["validate", "ids", ids_path, ifc_path, "--format", "json"],
    ]
    for cmd in candidates:
        try:
            proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False)
            if proc.returncode == 0 and proc.stdout:
                return True, proc.stdout, None
            # keep last stderr
            last_err = proc.stderr or proc.stdout
        except FileNotFoundError:
            return False, None, "validate CLI not found. Install buildingSMART/validate."
        except Exception as e:
            last_err = str(e)
    return False, None, last_err


def validate_ifc_with_ids_xml_official(ifc_file: Any, ids_xml_bytes: bytes, use_python_api: bool = True) -> Dict[str, Any]:
    """Esegue la validazione IFC vs IDS XML. NOTA: Non esiste un validator IDS ufficiale come package Python separato.
    buildingSMART/validate è un servizio web Django, non un validator IDS programmatico.
    Ritorna un dict con keys: ok, stdout, error.
    """
    # NOTE: There is no official Python API for IDS validation.
    # buildingSMART/validate is a Django web service for IFC validation (not IDS).
    # buildingSMART/IDS-Audit-tool is a .NET CLI for auditing IDS XML structure.
    # We use the existing custom validator as fallback.
    
    ids_tmp = None
    ifc_tmp = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".ids") as f:
            f.write(ids_xml_bytes)
            f.flush()
            ids_tmp = f.name
        ifc_tmp = _ensure_ifc_path(ifc_file)
        
        # Try CLI validate tool (though this may not be IDS-specific)
        ok, out, err = _run_validate_cli(ids_tmp, ifc_tmp)
        return {"ok": ok, "stdout": out, "error": err, "method": "cli"}
    finally:
        if ids_tmp and os.path.exists(ids_tmp):
            try:
                os.unlink(ids_tmp)
            except Exception:
                pass
        # if ifc_tmp was a temp file we created, it ends with tmp suffix
        try:
            if ifc_tmp and os.path.exists(ifc_tmp) and ifc_tmp.endswith('.ifc') and not isinstance(ifc_file, str):
                os.unlink(ifc_tmp)
        except Exception:
            pass


# ------------------------------
# VALIDATORE (fallback corrente) — mantiene l'output DataFrame per la UI
# ------------------------------

def validate_ifc_with_ids(ifc_file: Any, ids_rules: List[Dict[str, Any]]):
    """Valida un modello IFC rispetto a regole IDS semplificate e ritorna un DataFrame.
    Nota: questa è una logica di fallback per popolare la UI. Il percorso ufficiale via CLI è
    disponibile attraverso validate_ifc_with_ids_xml_official() usando un IDS XML.
    """
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
