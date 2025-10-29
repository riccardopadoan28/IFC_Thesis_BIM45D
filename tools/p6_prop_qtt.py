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
import ifcopenshell.util.element as util

# Third-party helpers from shared utilities
try:
    from .p_shared import get_objects_data_by_class, create_pandas_dataframe
except ImportError:
    try:
        from tools.p_shared import get_objects_data_by_class, create_pandas_dataframe
    except Exception as e:
        def _missing(*args, **kwargs):
            raise ImportError("p_shared module not found. Ensure tools/p_shared.py exists in your project.") from e
        get_objects_data_by_class = _missing
        create_pandas_dataframe = _missing

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

# def get_ifc_quantities(model):
#     """
#     Extract quantities (Qto) from the entire model and return a DataFrame with rows:
#     [ExpressId, GlobalId, Class, PredefinedType, Name, Level, Type, QuantitySet, QuantityName, QuantityValue]
#     """
#     all_data = []
#     if model is None:
#         return pd.DataFrame(columns=['ExpressId', 'GlobalId', 'Class', 'PredefinedType', 'Name', 'Level', 'Type', 'QuantitySet', 'QuantityName', 'QuantityValue'])

#     classes = get_types(model)
#     for cls in classes:
#         try:
#             objs_data, _ = get_objects_data_by_class(model, cls)
#             for od in objs_data:
#                 for qset_name, qprops in (od.get('QuantitySets') or {}).items():
#                     for pname, pval in qprops.items():
#                         if pname == 'id':
#                             continue
#                         all_data.append({
#                             'ExpressId': od.get('ExpressId'),
#                             'GlobalId': od.get('GlobalId'),
#                             'Class': od.get('Class'),
#                             'PredefinedType': od.get('PredefinedType'),
#                             'Name': od.get('Name'),
#                             'Level': od.get('Level'),
#                             'Type': od.get('Type'),
#                             'QuantitySet': qset_name,
#                             'QuantityName': pname,
#                             'QuantityValue': pval
#                         })
#         except Exception:
#             continue

#     if not all_data:
#         return pd.DataFrame(columns=['ExpressId', 'GlobalId', 'Class', 'PredefinedType', 'Name', 'Level', 'Type', 'QuantitySet', 'QuantityName', 'QuantityValue'])

#     return pd.DataFrame(all_data)

def get_ifc_quantities(model):
    """
    Extract IFC quantity takeoffs (Qto) using util.get_psets by detecting Qto sets.
    Returns a DataFrame with columns:
    [ExpressId, GlobalId, Class, PredefinedType, Name, Level, Type, QuantitySet, QuantityName, QuantityValue]
    """
    columns = [
        'ExpressId', 'GlobalId', 'Class', 'PredefinedType', 'Name',
        'Level', 'Type', 'QuantitySet', 'QuantityName', 'QuantityValue'
    ]

    if model is None:
        return pd.DataFrame(columns=columns)

    all_data = []

    for e in model.by_type("IfcElement"):
        try:
            psets_all = util.get_psets(e)
        except Exception:
            psets_all = {}
        if not psets_all:
            continue

        try:
            eid = e.id()
        except Exception:
            eid = None

        gid = getattr(e, "GlobalId", None)
        name = getattr(e, "Name", None)
        ptype = getattr(e, "PredefinedType", None)
        otype = getattr(e, "ObjectType", None)
        cls = e.is_a()

        # Attempt to determine level (IfcBuildingStorey)
        level = None
        try:
            if hasattr(e, "ContainedInStructure") and e.ContainedInStructure:
                lvl = e.ContainedInStructure[0]
                level = getattr(lvl, "Name", None)
        except Exception:
            pass

        for set_name, props in (psets_all or {}).items():
            # Detect Qto sets by name
            set_lower = (set_name or "").lower()
            is_qto = set_lower.startswith("qto") or ("quantit" in set_lower) or set_lower.endswith("quantities")
            if not is_qto or not isinstance(props, dict):
                continue
            for pname, pval in props.items():
                if isinstance(pname, str) and pname.lower() == "id":
                    continue
                all_data.append({
                    'ExpressId': eid,
                    'GlobalId': gid,
                    'Class': cls,
                    'PredefinedType': ptype,
                    'Name': name,
                    'Level': level,
                    'Type': otype,
                    'QuantitySet': set_name,
                    'QuantityName': pname,
                    'QuantityValue': pval
                })

    return pd.DataFrame(all_data, columns=columns)

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
    Build a DataFrame of properties/quantities for IFC4X3 models only.
    Classes are discovered dynamically from the model content (no hardcoded lists).
    """
    if model is None:
        return pd.DataFrame()

    # Determine schema from model or argument and enforce IFC4X3 only
    schema_from_model = getattr(model, 'schema', None)
    schema_name = (schema_from_model or schema or '').upper()
    if not schema_name.startswith('IFC4X3'):
        return pd.DataFrame()

    # Discover classes dynamically from the file
    classes = sorted(list(get_types(model)))

    # Filter out non-product/auxiliary classes to avoid noise
    EXCLUDE_PREFIXES = (
        'IfcRel', 'IfcProperty', 'IfcProfile', 'IfcRepresentation', 'IfcGeometric',
        'IfcPresentation', 'IfcMaterial', 'IfcConstraint', 'IfcDocument', 'IfcUnit',
        'IfcOwnerHistory', 'IfcQuantity', 'IfcClassification', 'IfcExternal', 'IfcLibrary'
    )
    target_classes = [c for c in classes if not any(c.startswith(p) for p in EXCLUDE_PREFIXES)]

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

# ------------------------------
# Unified long-form DataFrame (entities + Psets + Qtos + Attributes)
# ------------------------------

def get_ifc_full_dataframe(model):
    """
    Create a single long-form DataFrame aggregating all available data:
    - All entities/classes
    - All properties (Psets)
    - All quantities (Qtos)
    - Selected direct native attributes
    Each row represents a property or quantity associated to an entity.
    """
    columns = [
        'ExpressId', 'GlobalId', 'Class', 'PredefinedType', 'Name',
        'Level', 'Type', 'Source', 'SetName', 'AttributeName', 'Value'
    ]

    if model is None:
        return pd.DataFrame(columns=columns)

    records = []

    for e in model:
        try:
            eid = e.id()
        except Exception:
            eid = None

        cls = e.is_a()
        gid = getattr(e, 'GlobalId', None)
        name = getattr(e, 'Name', None)
        ptype = getattr(e, 'PredefinedType', None)
        otype = getattr(e, 'ObjectType', None)

        # Attempt to determine Level (e.g., IfcBuildingStorey)
        level = None
        try:
            if hasattr(e, 'ContainedInStructure') and e.ContainedInStructure:
                lvl = e.ContainedInStructure[0]
                level = getattr(lvl, 'Name', None)
        except Exception:
            pass

        # Pull all sets once
        try:
            sets = util.get_psets(e)
        except Exception:
            sets = {}

        for set_name, props in (sets or {}).items():
            if not isinstance(props, dict):
                continue
            set_lower = (set_name or '').lower()
            source = 'Qto' if (set_lower.startswith('qto') or 'quantit' in set_lower or set_lower.endswith('quantities')) else 'Pset'
            for pname, pval in (props or {}).items():
                if isinstance(pname, str) and pname.lower() == 'id':
                    continue
                records.append({
                    'ExpressId': eid,
                    'GlobalId': gid,
                    'Class': cls,
                    'PredefinedType': ptype,
                    'Name': name,
                    'Level': level,
                    'Type': otype,
                    'Source': source,
                    'SetName': set_name,
                    'AttributeName': pname,
                    'Value': pval
                })

        # Direct native attributes (filtered)
        for attr_name in dir(e):
            if attr_name.startswith('_'):
                continue
            try:
                attr_val = getattr(e, attr_name)
                if callable(attr_val) or isinstance(attr_val, (list, dict, set, tuple)):
                    continue
                if attr_val in (None, ''):
                    continue
                # Skip already captured core attributes to reduce noise
                if attr_name in ('GlobalId', 'Name', 'Description', 'ObjectType', 'PredefinedType'):
                    continue
                records.append({
                    'ExpressId': eid,
                    'GlobalId': gid,
                    'Class': cls,
                    'PredefinedType': ptype,
                    'Name': name,
                    'Level': level,
                    'Type': otype,
                    'Source': 'Attribute',
                    'SetName': None,
                    'AttributeName': attr_name,
                    'Value': attr_val
                })
            except Exception:
                continue

    return pd.DataFrame(records, columns=columns)
