"""
Helper condiviso — Model info helpers (Project Info / Model Properties)

Uso:
- Project Info page: get_project, get_stories, get_ifc_structure
- Model Properties pages: get_types, get_type_occurence, get_ifc_structure
- Utilities generali: get_x_and_y per grafici/ordinamenti

Nota: Commenti in italiano. Output/ritorni pensati per UI in inglese.
"""

from __future__ import annotations
from typing import Iterable, Dict, List, Any
import os
from ifcopenshell.util import element as ifc_element
import pandas as pd

# ==========================================================
# SHARED — Model info helpers
# Dove usate: Project Info, Model Properties
# ==========================================================

def get_project(model):
    """Return the first IfcProject entity from the model."""
    projects = model.by_type('IfcProject') if hasattr(model, 'by_type') else []
    return projects[0] if projects else None


def get_stories(model) -> List[Dict[str, Any]]:
    """Return building storeys as list of dicts {Storey, Elevation}."""
    return [{'Storey': s.Name, 'Elevation': getattr(s, 'Elevation', None)} for s in (model.by_type('IfcBuildingStorey') or [])]


def get_types(model, parent_class=None):
    """Return a set of IFC classes/types present in the model. Optionally filter by parent_class."""
    if parent_class:
        return set(i.is_a() for i in model if i.is_a(parent_class))
    return set(i.is_a() for i in model)


def get_type_occurence(model, types: Iterable[str]):
    """Count occurrences for each type in the provided iterable."""
    return {t: len(model.by_type(t)) for t in types}


def get_ifc_structure(ifc_file) -> Dict[str, Dict[str, List[str]]]:
    """Return a mapping {IFCClass: {PropertySet: [PropertyName, ...], ...}} for classes present in the file."""
    official_schemas = ['IFC2X3', 'IFC4', 'IFC4X3']
    schema_name = getattr(ifc_file.schema, 'schema_identifier', str(ifc_file.schema))
    if schema_name not in official_schemas:
        return {}
    result: Dict[str, Dict[str, List[str]]] = {}
    classes_in_file = sorted(set(obj.is_a() for obj in ifc_file))
    for cls in classes_in_file:
        result[cls] = {}
        elements = ifc_file.by_type(cls)
        for el in elements[:1]:
            for rel in getattr(el, 'IsDefinedBy', []) or []:
                if rel.is_a('IfcRelDefinesByProperties'):
                    pset = rel.RelatingPropertyDefinition
                    pset_name = getattr(pset, 'Name', None)
                    if pset_name:
                        result[cls].setdefault(pset_name, [])
                        for prop in getattr(pset, 'HasProperties', []) or []:
                            prop_name = getattr(prop, 'Name', None)
                            if prop_name:
                                result[cls][pset_name].append(prop_name)
    return result

# ==========================================================
# SHARED — Data extraction & DataFrame helpers
# Dove usate: IDS (pag. 2), BCF (pag. 3), Properties & Quantities (pag. 6), 4D (Timeline)
# ==========================================================


def save_ifc_to_public(ifc_file):
    """Copia un IFC sotto frontend-viewer/public e ritorna l'URL relativo."""
    public_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend-viewer", "public"))
    os.makedirs(public_dir, exist_ok=True)
    dest_path = os.path.join(public_dir, "temp_model.ifc")
    if hasattr(ifc_file, "getbuffer"):
        data = ifc_file.getbuffer()
    elif isinstance(ifc_file, bytes):
        data = ifc_file
    else:
        raise TypeError("Il file IFC deve essere un file-like con getbuffer() o bytes.")
    with open(dest_path, "wb") as f:
        f.write(data)
    return "/temp_model.ifc"


def get_objects_data_by_class(model, class_type):
    """Estrae dati oggetto per tutte le istanze di class_type, includendo Pset/Qto e meta base."""
    objects = model.by_type(class_type) if hasattr(model, 'by_type') else []
    objects_data = []
    pset_attributes = set()
    for obj in objects:
        try:
            qtos = ifc_element.get_psets(obj, qtos_only=True) or {}
        except Exception:
            qtos = {}
        try:
            psets = ifc_element.get_psets(obj, psets_only=True) or {}
        except Exception:
            psets = {}
        for pset_name, pset_data in qtos.items():
            for pname in pset_data.keys():
                if pname != 'id':
                    pset_attributes.add(f"{pset_name}.{pname}")
        for pset_name, pset_data in psets.items():
            for pname in pset_data.keys():
                if pname != 'id':
                    pset_attributes.add(f"{pset_name}.{pname}")
        try:
            container = ifc_element.get_container(obj)
            level_name = container.Name if container is not None else None
        except Exception:
            level_name = None
        try:
            itype = ifc_element.get_type(obj)
            type_name = itype.Name if itype is not None else None
        except Exception:
            type_name = None
        objects_data.append({
            'ExpressId': obj.id() if hasattr(obj, 'id') else None,
            'GlobalId': getattr(obj, 'GlobalId', None),
            'Class': obj.is_a() if hasattr(obj, 'is_a') else None,
            'PredefinedType': ifc_element.get_predefined_type(obj) if hasattr(ifc_element, 'get_predefined_type') else None,
            'Name': getattr(obj, 'Name', None),
            'Level': level_name,
            'Type': type_name,
            'QuantitySets': qtos,
            'PropertySets': psets,
        })
    return objects_data, sorted(list(pset_attributes))


def get_attribute_value(object_data, attribute):
    """Legge un attributo semplice o Pset/Qto dal dict object_data (es. 'Pset.Name')."""
    if object_data is None or attribute is None:
        return None
    if '.' not in attribute:
        return object_data.get(attribute)
    pset_name, prop_name = attribute.split('.', 1)
    psets = object_data.get('PropertySets', {}) or {}
    qtos = object_data.get('QuantitySets', {}) or {}
    if pset_name in psets:
        return psets[pset_name].get(prop_name)
    if pset_name in qtos:
        return qtos[pset_name].get(prop_name)
    for pn, props in psets.items():
        if pn.lower() == pset_name.lower():
            return props.get(prop_name)
    for pn, props in qtos.items():
        if pn.lower() == pset_name.lower():
            return props.get(prop_name)
    return None


def create_pandas_dataframe(objects_data, pset_attributes):
    """Costruisce un DataFrame a partire da objects_data e lista attributi Pset/Qto."""
    base_attrs = ['ExpressId', 'GlobalId', 'Class', 'PredefinedType', 'Name', 'Level', 'Type']
    attrs = base_attrs + sorted(pset_attributes or [])
    records = []
    for od in objects_data:
        row = {k: get_attribute_value(od, k) for k in attrs}
        for b in base_attrs:
            if b not in row:
                row[b] = od.get(b)
        records.append(row)
    df = pd.DataFrame(records, columns=attrs)
    if objects_data:
        for od in objects_data:
            for qname, qdict in (od.get('QuantitySets') or {}).items():
                for k, v in qdict.items():
                    if k == 'id':
                        continue
                    col = f"{qname}.{k}"
                    if col not in df.columns:
                        df[col] = None
                    df.loc[df['ExpressId'] == od.get('ExpressId'), col] = v
    return df


def get_x_and_y(values: Dict[Any, float], higher_then: float | None = None):
    """Convert a dict to ordered (x, y) lists; optionally filter by threshold."""
    sorted_items = sorted(values.items(), key=lambda kv: kv[1], reverse=True)
    if higher_then is not None:
        sorted_items = [item for item in sorted_items if item[1] > higher_then]
    x_values = [item[0] for item in sorted_items]
    y_values = [item[1] for item in sorted_items]
    return x_values, y_values
