
"""
IFC Properties & Quantities helpers (page 6)

This module contains only the functions used by the Properties & Quantities page:
- get_types
- get_ifc_quantities
- export_ifc_as_csv_bytes
- get_ifc_pandas
"""

from datetime import datetime
import importlib
import pandas as pd
import ifcopenshell

# Third-party helpers from shared utilities
from ifc_shared import get_objects_data_by_class, create_pandas_dataframe

# Optional ifcopenshell CSV helpers (imported once)
if importlib.util.find_spec('ifcopenshell.csv') is not None:
    try:
        ifc_csv = importlib.import_module('ifcopenshell.csv')
    except Exception:
        ifc_csv = None
else:
    ifc_csv = None

if importlib.util.find_spec('ifcopenshell.ifccsv') is not None:
    try:
        ifc_ifccsv = importlib.import_module('ifcopenshell.ifccsv')
    except Exception:
        ifc_ifccsv = None
else:
    ifc_ifccsv = None


# ------------------------------
# Shared type utilities (used by page 6)
# ------------------------------

def get_types(model, parent_class=None):
    """Return a set of IFC classes/types present in the model. Optionally filter by parent_class."""
    if parent_class:
        return set(i.is_a() for i in model if i.is_a(parent_class))
    return set(i.is_a() for i in model)


# ------------------------------
# Quantities extraction
# ------------------------------

def get_ifc_quantities(model):
    """
    Extract quantities (Qto) from the entire model and return a DataFrame with rows:
    [ExpressId, GlobalId, Class, PredefinedType, Name, Level, Type, QuantitySet, QuantityName, QuantityValue]
    """
    all_data = []
    if model is None:
        return pd.DataFrame(columns=['ExpressId', 'GlobalId', 'Class', 'PredefinedType', 'Name', 'Level', 'Type', 'QuantitySet', 'QuantityName', 'QuantityValue'])

    classes = get_types(model)
    for cls in classes:
        try:
            objs_data, _ = get_objects_data_by_class(model, cls)
            for od in objs_data:
                for qset_name, qprops in (od.get('QuantitySets') or {}).items():
                    for pname, pval in qprops.items():
                        if pname == 'id':
                            continue
                        all_data.append({
                            'ExpressId': od.get('ExpressId'),
                            'GlobalId': od.get('GlobalId'),
                            'Class': od.get('Class'),
                            'PredefinedType': od.get('PredefinedType'),
                            'Name': od.get('Name'),
                            'Level': od.get('Level'),
                            'Type': od.get('Type'),
                            'QuantitySet': qset_name,
                            'QuantityName': pname,
                            'QuantityValue': pval
                        })
        except Exception:
            continue

    if not all_data:
        return pd.DataFrame(columns=['ExpressId', 'GlobalId', 'Class', 'PredefinedType', 'Name', 'Level', 'Type', 'QuantitySet', 'QuantityName', 'QuantityValue'])

    return pd.DataFrame(all_data)


# ------------------------------
# CSV export helper
# ------------------------------

def export_ifc_as_csv_bytes(model=None, df=None):
    """
    Produce CSV bytes. Prefer ifcopenshell CSV exporter if available (imported above),
    otherwise fall back to using a pandas DataFrame if provided.
    Returns bytes or None.
    """
    try:
        if ifc_csv is not None and hasattr(ifc_csv, 'to_csv'):
            out = ifc_csv.to_csv(model)
            return out if isinstance(out, (bytes, bytearray)) else str(out).encode('utf-8')
        if ifc_ifccsv is not None and hasattr(ifc_ifccsv, 'to_csv'):
            out = ifc_ifccsv.to_csv(model)
            return out if isinstance(out, (bytes, bytearray)) else str(out).encode('utf-8')
    except Exception:
        pass

    try:
        if df is not None:
            return df.to_csv(index=False).encode('utf-8')
    except Exception:
        pass

    return None


# ------------------------------
# DataFrame extraction for properties/quantities
# ------------------------------

def get_ifc_pandas(model, schema=None):
    """
    Orchestrates extraction of IFC objects for a set of target classes and returns a concatenated
    pandas DataFrame with properties and quantities expanded.
    """
    if model is None:
        return pd.DataFrame()

    schema_name = (schema or '').upper()

    classes_by_schema = {
        "IFC2X3": [
            "IfcBeam", "IfcColumn", "IfcSlab", "IfcWall", "IfcWallStandardCase",
            "IfcFooting", "IfcMember", "IfcReinforcingBar", "IfcReinforcingMesh",
            "IfcTendon", "IfcTendonAnchor", "IfcStructuralConnection",
            "IfcStructuralCurveMember", "IfcStructuralSurfaceMember",
            "IfcRamp", "IfcStair"
        ],
        "IFC4": [
            "IfcBeam", "IfcColumn", "IfcSlab", "IfcWall", "IfcWallStandardCase",
            "IfcFooting", "IfcMember", "IfcReinforcingBar", "IfcReinforcingMesh",
            "IfcTendon", "IfcTendonAnchor", "IfcStructuralConnection",
            "IfcStructuralCurveMember", "IfcStructuralSurfaceMember",
            "IfcRamp", "IfcStair"
        ],
        "IFC4X3": [
            "IfcBeam", "IfcColumn", "IfcSlab", "IfcWall", "IfcWallStandardCase",
            "IfcFooting", "IfcMember", "IfcReinforcingBar", "IfcReinforcingMesh",
            "IfcTendon", "IfcTendonAnchor", "IfcStructuralConnection",
            "IfcStructuralCurveMember", "IfcStructuralSurfaceMember",
            "IfcRamp", "IfcStair", "IfcBearing"
        ]
    }

    target_classes = classes_by_schema.get(schema_name, classes_by_schema['IFC4'])
    dfs = []

    for cls in target_classes:
        try:
            data, pset_attrs = get_objects_data_by_class(model, cls)
            df = create_pandas_dataframe(data, pset_attrs)
            if df is not None and not df.empty:
                df['Class'] = cls
                dfs.append(df)
        except Exception:
            continue

    if not dfs:
        return pd.DataFrame()

    df_all = pd.concat(dfs, ignore_index=True)
    return df_all
