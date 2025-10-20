"""
Centralized IFC helpers (tools.ifchelper)

This module collects IFC-related helper functions used across the Streamlit app.
Functions are grouped and ordered by where they are used in the app pages.
Before each group there is a short note indicating the page(s) that call the functions.
Before each function there is a short explanation of what it does and its inputs/outputs.
"""

# Standard imports
from datetime import datetime
import importlib

# Third-party
import pandas as pd
import ifcopenshell
from ifcopenshell.util import element as ifc_element
import streamlit as st

# Module session alias for convenience in UI helpers
session = st.session_state

# Brief info: imports are centralized above; optional modules are detected once here.
# Try to import optional ifcopenshell CSV helpers at module import time to avoid in-function imports.
# Use dynamic importlib.import_module to prevent static analyzers from reporting missing imports.
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


# Central import policy and module organization note
# NOTE:
# - All third-party and standard library imports are declared at the top of this file.
#   Avoid adding new imports inside functions to keep dependencies centralized and
#   improve static analysis. Use the top-level `importlib` check for optional modules.
# - Functions are grouped and ordered by where they are used in the application
#   (GROUP A .. GROUP I). Each group header documents the intended usage pages.
# - Keep helpers small and focused; UI-specific functions that use Streamlit live in
#   the UI helpers groups and may reference st.session_state when needed.

# ==========================================================
# GROUP A — Shared helpers (used across multiple pages)
# Where used: pages 2 (IDS), 3 (BCF), 6 (Properties & Quantities), 4D (Project Timeline)
# These helpers provide common extraction and DataFrame conversion utilities.
# ==========================================================

def get_objects_data_by_class(model, class_type):
    """
    Extracts object data for all instances of `class_type` in the model.

    Returns:
      - objects_data: list of dicts with keys such as ExpressId, GlobalId, Class, Name,
        PredefinedType, Level, Type, QuantitySets, PropertySets
      - pset_attributes: list of discovered pset/quantity keys (e.g. 'Pset_WallCommon.FireRating')

    Usage: called by page 6 (Properties & Quantities) when building DataFrames.
    """
    objects = model.by_type(class_type) if hasattr(model, 'by_type') else []
    objects_data = []
    pset_attributes = set()

    for obj in objects:
        # get quantities and property sets using official util
        try:
            qtos = ifc_element.get_psets(obj, qtos_only=True) or {}
        except Exception:
            qtos = {}
        try:
            psets = ifc_element.get_psets(obj, psets_only=True) or {}
        except Exception:
            psets = {}

        # collect attribute names
        for pset_name, pset_data in qtos.items():
            for pname in pset_data.keys():
                if pname != 'id':
                    pset_attributes.add(f"{pset_name}.{pname}")
        for pset_name, pset_data in psets.items():
            for pname in pset_data.keys():
                if pname != 'id':
                    pset_attributes.add(f"{pset_name}.{pname}")

        # container (level) and type retrieval using util helpers
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
    """
    Read a simple attribute or a PropertySet/QuantitySet value from an object_data dict.
    - attribute can be 'Name' or 'Pset_WallCommon.FireRating' style.

    Returns the value or None if not found.

    Usage: used by create_pandas_dataframe and by validation helpers.
    """
    if object_data is None or attribute is None:
        return None

    if '.' not in attribute:
        return object_data.get(attribute)

    pset_name, prop_name = attribute.split('.', 1)
    psets = object_data.get('PropertySets', {}) or {}
    qtos = object_data.get('QuantitySets', {}) or {}

    # exact match
    if pset_name in psets:
        return psets[pset_name].get(prop_name)
    if pset_name in qtos:
        return qtos[pset_name].get(prop_name)

    # case-insensitive fallback
    for pn, props in psets.items():
        if pn.lower() == pset_name.lower():
            return props.get(prop_name)
    for pn, props in qtos.items():
        if pn.lower() == pset_name.lower():
            return props.get(prop_name)

    return None


def create_pandas_dataframe(objects_data, pset_attributes):
    """
    Build a pandas DataFrame from objects_data and the list of pset/quantity attribute names.

    columns will include base attributes (ExpressId, GlobalId, Class, PredefinedType, Name, Level, Type)
    followed by sorted pset_attributes.

    Usage: page 6 DataFrame creation.
    """
    base_attrs = [
        'ExpressId', 'GlobalId', 'Class', 'PredefinedType', 'Name', 'Level', 'Type'
    ]

    attrs = base_attrs + sorted(pset_attributes or [])
    records = []

    for od in objects_data:
        row = {k: get_attribute_value(od, k) for k in attrs}
        # ensure base attrs exist
        for b in base_attrs:
            if b not in row:
                row[b] = od.get(b)
        records.append(row)

    df = pd.DataFrame(records, columns=attrs)

    # expand QuantitySets columns if present in objects_data (numeric values)
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


# ==========================================================
# GROUP B — Properties & Quantities (Page 6)
# Where used: pages/6_Properties and Quantities.py
# Functions here extract QTOs and return DataFrames suitable for analysis.
# ==========================================================

def get_ifc_quantities(model):
    """
    Extract quantities (Qto) from the entire model and return a DataFrame with rows:
    [ExpressId, GlobalId, Class, PredefinedType, Name, Level, Type, QuantitySet, QuantityName, QuantityValue]

    Usage: called by pages/6 to build the Quantities DataFrame.
    """
    all_data = []

    # get classes present in the model
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
        except Exception as e:
            # non-fatal: continue with next class
            print(f"⚠️ Error extracting quantities for {cls}: {e}")

    if not all_data:
        return pd.DataFrame(columns=['ExpressId', 'GlobalId', 'Class', 'PredefinedType', 'Name', 'Level', 'Type', 'QuantitySet', 'QuantityName', 'QuantityValue'])

    return pd.DataFrame(all_data)


# ==========================================================
# GROUP C — IDS validation (Page 2)
# Where used: pages/2_IDS - Validation Results and Automatic IDS Test
# This group contains functions that validate IFC objects against IDS rules.
# ==========================================================

def validate_ifc_with_ids(ifc_file, ids_rules):
    """
    Validate an IFC model against IDS rules.

    Each rule is expected as {'ifc_class': 'IfcWall', 'properties': [{'property_set':'Pset_X','property_name':'Y','mandatory':True}, ...]}

    Returns a pandas DataFrame with columns:
      ElementID, ElementName, IFCClass, PropertySet, PropertyName, Value, Compliant

    Usage: pages/2 uses this function to produce validation tables and summaries.
    """
    results = []

    # Accept either an opened model or a file path
    try:
        model = ifc_file if hasattr(ifc_file, 'by_type') else ifcopenshell.open(ifc_file)
    except Exception:
        model = ifc_file

    for rule in ids_rules:
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
                        # case-insensitive fallback
                        for pn, props in psets.items():
                            if pn.lower() == pset_name.lower():
                                val = props if prop_name == 'ALL' else props.get(prop_name)
                                pset_name = pn
                                break
                else:
                    # search across psets
                    for pn, props in psets.items():
                        if prop_name == 'ALL':
                            val = props
                            pset_name = pn
                            break
                        if prop_name in props:
                            val = props.get(prop_name)
                            pset_name = pn
                            break

                # final fallback to direct attribute
                if val is None and prop_name and hasattr(obj, prop_name):
                    try:
                        val = getattr(obj, prop_name)
                    except Exception:
                        val = None

                is_valid = (val is not None) if mandatory else True

                # stable identifier
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


# ==========================================================
# GROUP D — Project Info & Types (used by Project Info and Model Properties)
# Where used: Project Info, Model Properties pages
# ==========================================================

def get_project(model):
    """Return the first IfcProject entity from the model."""
    projects = model.by_type('IfcProject') if hasattr(model, 'by_type') else []
    return projects[0] if projects else None


def get_stories(model):
    """Return building storeys present in the model as list of dicts {Storey, Elevation}."""
    return [{'Storey': s.Name, 'Elevation': getattr(s, 'Elevation', None)} for s in (model.by_type('IfcBuildingStorey') or [])]


def get_types(model, parent_class=None):
    """
    Return a set of IFC classes/types present in the model. Optionally filter by parent_class.
    """
    if parent_class:
        return set(i.is_a() for i in model if i.is_a(parent_class))
    return set(i.is_a() for i in model)


def get_type_occurence(model, types):
    """Count occurrences for each type in the provided list."""
    return {t: len(model.by_type(t)) for t in types}


# ==========================================================
# GROUP E — Schedules, Work Plans, Tasks (Project Timeline / 4D)
# Where used: Project Timeline page
# ==========================================================

def create_cost_schedule(model, name=None):
    """Create a cost schedule in the model (uses ifcopenshell.api)."""
    try:
        ifcopenshell.api.run('cost.add_cost_schedule', model, name=name)
    except Exception as e:
        print(f'Error creating cost schedule: {e}')


def create_work_schedule(model, name=None):
    """Create a work schedule in the model."""
    try:
        ifcopenshell.api.run('sequence.add_work_schedule', model, name=name)
    except Exception as e:
        print(f'Error creating work schedule: {e}')


def get_root_tasks(work_schedule):
    """Return root IfcTask objects referenced by a work schedule."""
    tasks = []
    if getattr(work_schedule, 'Controls', None):
        for rel in work_schedule.Controls:
            for obj in getattr(rel, 'RelatedObjects', []) or []:
                if obj.is_a('IfcTask'):
                    tasks.append(obj)
    return tasks


def get_nested_tasks(task):
    """Return 1-level nested tasks for a given task."""
    tasks = []
    for rel in getattr(task, 'IsNestedBy', []) or []:
        for obj in getattr(rel, 'RelatedObjects', []) or []:
            if obj.is_a('IfcTask'):
                tasks.append(obj)
    return tasks


def get_nested_tasks2(task):
    """Alternate method to get nested tasks (not recommended)."""
    return [obj for rel in getattr(task, 'IsNestedBy', []) or [] for obj in getattr(rel, 'RelatedObjects', []) or [] if obj.is_a('IfcTask')]


def get_schedule_tasks(work_schedule):
    """Return all tasks (root + nested recursively) for a schedule."""
    all_tasks = []
    def append_tasks(t):
        for nested in get_nested_tasks(t):
            all_tasks.append(nested)
            if getattr(nested, 'IsNestedBy', None):
                append_tasks(nested)
    for root in get_root_tasks(work_schedule):
        append_tasks(root)
    return all_tasks


def get_task_data(tasks):
    """Return dicts with Identification, Name, Start and Finish dates for tasks."""
    def fmt(d):
        try:
            return format_date_from_iso(d) if d else ''
        except Exception:
            return ''
    return [
        {
            'Identification': getattr(task, 'Identification', None),
            'Name': getattr(task, 'Name', None),
            'ScheduleStart': fmt(getattr(getattr(task, 'TaskTime', None), 'ScheduleStart', None)),
            'ScheduleFinish': fmt(getattr(getattr(task, 'TaskTime', None), 'ScheduleFinish', None)),
        }
        for task in tasks
    ]


# ==========================================================
# GROUP F — Utilities, plotting helpers and IFC.js parsing
# Where used: various pages
# ==========================================================

def get_x_and_y(values, higher_then=None):
    """Convert a dict to ordered (x, y) lists; filter by threshold if provided."""
    sorted_items = sorted(values.items(), key=lambda kv: kv[1], reverse=True)
    if higher_then is not None:
        sorted_items = [item for item in sorted_items if item[1] > higher_then]
    x_values = [item[0] for item in sorted_items]
    y_values = [item[1] for item in sorted_items]
    return x_values, y_values


def format_date_from_iso(iso_date=None):
    """Format an ISO date string to '15 Sep 25' or return empty string."""
    try:
        return datetime.fromisoformat(iso_date).strftime('%d %b %y') if iso_date else ''
    except Exception:
        return ''


def format_ifcjs_psets(ifcJSON):
    """Normalize Property/Quantity Sets coming from IFC.js (web-ifc) into a dictionary keyed by expressID."""
    result = {}
    for pset in ifcJSON:
        pset_name = pset.get('Name', {}).get('value')
        expressID = pset.get('expressID')
        is_quantity = 'Qto' in (pset_name or '')
        is_property = 'Pset' in (pset_name or '')
        if expressID is None:
            continue
        for container_key in ('Quantities', 'HasProperties'):
            items = pset.get(container_key, [])
            for prop in items:
                prop_name = prop.get('Name', {}).get('value')
                prop_value = ''
                for k, v in prop.items():
                    if 'Value' in k and isinstance(v, dict):
                        prop_value = v.get('value')
                        break
                result.setdefault(expressID, {'Name': pset_name, 'Data': []})['Data'].append({'Name': prop_name, 'Value': prop_value})
    return result


def get_ifc_structure(ifc_file):
    """Return a mapping {IFCClass: {PropertySet: [PropertyName, ...], ...}} for classes present in the file."""
    official_schemas = ['IFC2X3', 'IFC4', 'IFC4X3']
    schema_name = getattr(ifc_file.schema, 'schema_identifier', str(ifc_file.schema))
    if schema_name not in official_schemas:
        return {}
    result = {}
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
# GROUP G — UI helpers for Project Timeline (Streamlit interactive helpers)
# Where used: Project Timeline page (these functions directly use st)
# ==========================================================

def get_selectable_elements(filter_type='IfcProduct'):
    """Return list of elements filtered by type from current session.ifc_file."""
    if not getattr(session, 'ifc_file', None):
        return []
    try:
        return session.ifc_file.by_type(filter_type)
    except Exception:
        return []


def draw_filter_selector():
    """Streamlit UI: show filter options (By Type / By Property) and return filtered elements list."""
    st.markdown('**Filter elements**')
    filter_mode = st.selectbox('Filter mode', ['By Type', 'By Property', 'By Level'], key='filter_mode_4d')
    filtered = []
    if filter_mode == 'By Type':
        type_options = ['IfcProduct', 'IfcElement', 'IfcBuildingElement', 'IfcWall', 'IfcWindow', 'IfcDoor']
        sel_type = st.selectbox('Element type', type_options, key='filter_type_selector')
        if getattr(session, 'ifc_file', None):
            try:
                filtered = session.ifc_file.by_type(sel_type)
            except Exception:
                filtered = []
    elif filter_mode == 'By Level':
        levels = []
        if getattr(session, 'ifc_file', None):
            for lt in ('IfcBuildingStorey', 'IfcLevel'):
                try:
                    levels.extend(session.ifc_file.by_type(lt) or [])
                except Exception:
                    continue
        level_options = [f"{l.id()} - {getattr(l, 'Name', str(l))}" for l in levels]
        selected_level = st.selectbox('Select Level (Building Storey)', [''] + level_options, key='filter_level_selector')
        if selected_level:
            level_id = int(selected_level.split(' - ', 1)[0])
            level = session.ifc_file.by_id(level_id)
            elems = []
            try:
                for inv in session.ifc_file.get_inverse(level) or []:
                    related = getattr(inv, 'RelatedElements', None)
                    if related:
                        for el in related:
                            elems.append(el)
                seen = set(); result = []
                for e in elems:
                    eid = e.id() if hasattr(e, 'id') else None
                    if eid and eid not in seen:
                        result.append(e); seen.add(eid)
                filtered = result
            except Exception:
                filtered = []
    else:
        # By Property
        prop_options = ['Name', 'GlobalId', 'Tag', 'PredefinedType', 'ObjectType']
        prop = st.selectbox('Property', prop_options, key='filter_prop_selector')
        op = st.selectbox('Operator', ['contains', 'equals', 'startswith', 'endswith'], key='filter_op_selector')
        val = st.text_input('Value', key='filter_value_4d')
        elems = []
        if getattr(session, 'ifc_file', None):
            for t in ['IfcProduct', 'IfcElement']:
                try:
                    elems.extend(session.ifc_file.by_type(t) or [])
                except Exception:
                    continue
        for el in elems:
            try:
                attr = getattr(el, prop) if hasattr(el, prop) else el.get_info().get(prop)
            except Exception:
                attr = None
            if attr is None:
                continue
            s = str(attr)
            match = False
            if op == 'contains' and val.lower() in s.lower():
                match = True
            elif op == 'equals' and s.lower() == val.lower():
                match = True
            elif op == 'startswith' and s.lower().startswith(val.lower()):
                match = True
            elif op == 'endswith' and s.lower().endswith(val.lower()):
                match = True
            if match:
                filtered.append(el)
    st.caption(f"Filtered elements: {len(filtered)}")
    return filtered


def draw_schedule_manager():
    """Streamlit UI for schedule manager: compose workplans, assign schedules and create tasks."""
    st.subheader('WorkPlan / Schedule / Task Manager')
    elements = draw_filter_selector()
    options = [f"{el.id()} - {getattr(el, 'Name', str(el))}" for el in elements]
    selected_options = st.multiselect('Select elements', options, key='selected_elements_list')
    selected_ids = [int(s.split(' - ', 1)[0]) for s in selected_options]

    st.text_input('WorkPlan name', key='workplan_name')
    if st.button('Create IfcWorkPlan for selected elements', key='create_workplan_button'):
        create_work_plan_for_selected(getattr(session, 'workplan_name', None), selected_ids)

    workplans = session.ifc_file.by_type('IfcWorkPlan') if getattr(session, 'ifc_file', None) else []
    wp_options = [f"{wp.id()} - {getattr(wp, 'Name', str(wp))}" for wp in workplans]
    selected_wp = st.selectbox('Select existing WorkPlan', [''] + wp_options, key='select_workplan')
    wp_id = int(selected_wp.split(' - ', 1)[0]) if selected_wp else None

    schedules = session.ifc_file.by_type('IfcWorkSchedule') if getattr(session, 'ifc_file', None) else []
    sched_options = [f"{s.id()} - {getattr(s, 'Name', str(s))}" for s in schedules]
    selected_sched = st.selectbox('Select Schedule to assign', [''] + sched_options, key='select_schedule_to_assign')
    sched_id = int(selected_sched.split(' - ', 1)[0]) if selected_sched else None

    if st.button('Assign Schedule to WorkPlan', key='assign_schedule_button'):
        if wp_id and sched_id:
            assign_schedule_to_workplan(wp_id, sched_id)
        else:
            st.error('Please select valid WorkPlan and Schedule')

    st.text_input('Task name prefix', key='task_name_prefix', value='Task')
    if st.button('Create IfcTask for selected elements', key='create_tasks_button'):
        create_task_for_selected(sched_id, selected_ids, getattr(session, 'task_name_prefix', 'Task'))


# ==========================================================
# GROUP H — Small helpers used by UI functions above
# ==========================================================

def create_work_plan_for_selected(name, selected_ids):
    """Create a basic IfcWorkPlan entity in the model. Associations to elements are not automatically created."""
    if not name:
        st.error('Please enter a name for the WorkPlan')
        return None
    if not getattr(session, 'ifc_file', None):
        st.error('No IFC file loaded in session')
        return None
    try:
        wp = session.ifc_file.create_entity('IfcWorkPlan', Name=name)
        st.success('IfcWorkPlan created')
        st.info('Note: associations with selected elements are not automatically created.')
        return wp
    except Exception as e:
        st.error(f'Error creating WorkPlan: {e}')
        return None


def assign_schedule_to_workplan(workplan_id, schedule_id):
    """Attempt to assign a schedule to a workplan (best-effort, non-destructive)."""
    if not getattr(session, 'ifc_file', None):
        st.error('No IFC file loaded in session')
        return
    try:
        wp = session.ifc_file.by_id(int(workplan_id))
        sched = session.ifc_file.by_id(int(schedule_id))
        if not wp or not sched:
            st.error('WorkPlan or Schedule not found in the IFC file')
            return
        st.success('Schedule assignment noted. Implement relational linking as needed.')
    except Exception as e:
        st.error(f'Error assigning schedule: {e}')


def create_task_for_selected(schedule_id, selected_ids, task_name_prefix='Task'):
    """Create simple IfcTask entities for each selected element id (no schedule relations created)."""
    if not getattr(session, 'ifc_file', None):
        st.error('No IFC file loaded in session')
        return
    if not selected_ids:
        st.error('No elements selected to create tasks for')
        return
    created = 0
    try:
        for eid in selected_ids:
            name = f"{task_name_prefix}_{eid}"
            session.ifc_file.create_entity('IfcTask', Name=name)
            created += 1
        st.success(f'Created {created} tasks (associations to schedules not created automatically)')
    except Exception as e:
        st.error(f'Error creating tasks: {e}')


# ==========================================================
# GROUP I — CSV export helper (ifcopenshell CSV) used by Properties page
# Where used: pages/6_Properties and Quantities.py
# ==========================================================

def export_ifc_as_csv_bytes(model=None, df=None):
    """
    Produce CSV bytes. Prefer ifcopenshell CSV exporter if available (imported at module level),
    otherwise fall back to using a pandas DataFrame if provided.

    Returns bytes or None.
    """
    try:
        # Use pre-imported optional modules if available
        if ifc_csv is not None and hasattr(ifc_csv, 'to_csv'):
            out = ifc_csv.to_csv(model)
            return out if isinstance(out, (bytes, bytearray)) else str(out).encode('utf-8')
        if ifc_ifccsv is not None and hasattr(ifc_ifccsv, 'to_csv'):
            out = ifc_ifccsv.to_csv(model)
            return out if isinstance(out, (bytes, bytearray)) else str(out).encode('utf-8')
    except Exception:
        pass

    # Fallback to pandas DataFrame
    try:
        if df is not None:
            return df.to_csv(index=False).encode('utf-8')
    except Exception:
        pass

    return None


# ==========================================================
# Additional helper: full properties DataFrame extraction (used by Page 6)
# Where used: pages/6_Properties and Quantities.py
# This function orchestrates extraction for a set of structural classes based on schema.
# ==========================================================

def get_ifc_pandas(model, schema=None):
    """
    Orchestrates extraction of IFC objects for a set of target classes and returns a
    concatenated pandas DataFrame with properties and quantities expanded.

    - model: opened ifcopenshell model
    - schema: optional string like 'IFC4X3' to select class list

    Usage: called by pages/6 to populate session DataFrame.
    """
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
            # non-fatal: continue with other classes
            continue

    if not dfs:
        return pd.DataFrame()

    df_all = pd.concat(dfs, ignore_index=True)
    return df_all

# End of module
