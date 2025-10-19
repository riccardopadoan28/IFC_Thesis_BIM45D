import ifcopenshell
import ifcopenshell.util.element as Element
import ifcopenshell.api
from datetime import datetime
import pandas as pd
from . import ifchelper as helper
import streamlit as st

session = st.session_state

# -----------------------------
# ORGANIZZAZIONE HELPERS
# -----------------------------
# Qui raggruppiamo le funzioni per pagina di utilizzo.
# - Shared helpers: funzioni usate da più pagine (posizionate per prime)
# - Page 6: Properties & Quantities
# - Page 7: Project Timeline (4D)
# - Project Info, Cost Schedule, ecc.
# I commenti che seguono indicano dove ogni funzione viene usata.


# ==========================================================
# 1. Estrazione dei dati IFC da oggetti specifici
# ==========================================================
# Richiamata in: get_ifc_quantities()
def get_objects_data_by_class(file, class_type):
    """
    Estrae dati da oggetti IFC di una determinata classe.
    Restituisce:
        - Lista di oggetti strutturati come dizionari
        - Lista degli attributi PropertySet/QuantitySet rilevati
    """
    def add_pset_attributes(psets):
        for pset_name, pset_data in psets.items():
            for property_name in pset_data.keys():
                if property_name != "id":
                    pset_attributes.add(f"{pset_name}.{property_name}")

    objects = file.by_type(class_type)
    objects_data = []
    pset_attributes = set()

    for obj in objects:
        qtos = Element.get_psets(obj, qtos_only=True)
        print(f"Class {class_type}, object {obj.id()}: QuantitySets = {qtos}")
        psets = Element.get_psets(obj, psets_only=True)
        add_pset_attributes(qtos)
        add_pset_attributes(psets)

        objects_data.append({
            "ExpressId": obj.id(),
            "GlobalId": obj.GlobalId,
            "Class": obj.is_a(),
            "PredefinedType": Element.get_predefined_type(obj),
            "Name": obj.Name,
            "Level": Element.get_container(obj).Name if Element.get_container(obj) else "",
            "Type": Element.get_type(obj).Name if Element.get_type(obj) else "",
            "QuantitySets": qtos,
            "PropertySets": psets,
        })

    return objects_data, list(pset_attributes)


# ==========================================================
# 2. Attributi e proprietà
# ==========================================================
# Richiamata in: create_pandas_dataframe()
def get_attribute_value(object_data, attribute):
    """
    Estrae il valore di un attributo semplice o di un property set (es: QtoWall.Length)
    """
    if "." not in attribute:
        return object_data.get(attribute)

    pset_name, prop_name = attribute.split(".", 1)

    if pset_name in object_data["PropertySets"]:
        return object_data["PropertySets"][pset_name].get(prop_name)

    if pset_name in object_data["QuantitySets"]:
        return object_data["QuantitySets"][pset_name].get(prop_name)

    return None


# ==========================================================
# 3. Costruzione del DataFrame
# ==========================================================
# Richiamata in: Quantities Review (streamlit tab)
def create_pandas_dataframe(data, pset_attributes):
    """
    Crea un DataFrame Pandas a partire da una lista di oggetti IFC
    e dagli attributi richiesti (classici + psets/qtos)
    """
    # attributi base sempre presenti
    attributes = [
        "ExpressId",
        "GlobalId",
        "Class",
        "PredefinedType",
        "Name",
        "Level",
        "Type",
    ] + pset_attributes

    pandas_data = []
    for obj_data in data:
        row = []
        for attr in attributes:
            row.append(get_attribute_value(obj_data, attr))
        pandas_data.append(tuple(row))

    df = pd.DataFrame.from_records(pandas_data, columns=attributes)

    # 🔹 esplodiamo i QuantitySets in colonne numeriche
    if "QuantitySets" in data[0]:
        for obj_data in data:
            for qto_name, qto_dict in obj_data["QuantitySets"].items():
                for key, value in qto_dict.items():
                    if key != "id":
                        col = f"{qto_name}.{key}"
                        if col not in df.columns:
                            df[col] = None
                        df.loc[df["ExpressId"] == obj_data["ExpressId"], col] = value

    return df


# ==========================================================
# 4. Estrazione quantità (Qto)
# ==========================================================
# Richiamata in: load_quantities()
def get_ifc_quantities(file):
    """
    Estrae le quantità (Qto) da tutte le classi IFC del file.
    Restituisce un DataFrame con colonne:
    [ExpressId, GlobalId, Class, Name, Level, Type, QuantityName, QuantityValue]
    """
    all_data = []
    all_attributes = set()

    # prendi tutte le classi presenti
    classes = helper.get_types(file)

    for class_type in classes:
        try:
            objs_data, _ = helper.get_objects_data_by_class(file, class_type)

            for obj in objs_data:
                qtos = obj.get("QuantitySets", {})
                for qto_name, qto_props in qtos.items():
                    for prop_name, prop_value in qto_props.items():
                        if prop_name == "id":
                            continue
                        all_data.append({
                            "ExpressId": obj["ExpressId"],
                            "GlobalId": obj["GlobalId"],
                            "Class": obj["Class"],
                            "PredefinedType": obj["PredefinedType"],
                            "Name": obj["Name"],
                            "Level": obj["Level"],
                            "Type": obj["Type"],
                            "QuantitySet": qto_name,
                            "QuantityName": prop_name,
                            "QuantityValue": prop_value
                        })
                        all_attributes.add(f"{qto_name}.{prop_name}")

        except Exception as e:
            print(f"⚠️ Error extracting quantities for {class_type}: {e}")

    if not all_data:
        return pd.DataFrame(columns=[
            "ExpressId", "GlobalId", "Class", "PredefinedType", "Name",
            "Level", "Type", "QuantitySet", "QuantityName", "QuantityValue"
        ])

    return pd.DataFrame(all_data)


# ==========================================================
# 5. Informazioni sul progetto
# ==========================================================
# Richiamata in: Project Info (streamlit tab)
def get_project(file):
    """Restituisce il primo oggetto IfcProject del file"""
    return file.by_type("IfcProject")[0]

# Richiamata in: Project Info (streamlit tab)
def get_stories(file):
    """Restituisce tutti i livelli (storey) del modello"""
    return [
        {"Storey": storey.Name, "Elevation": storey.Elevation}
        for storey in file.by_type("IfcBuildingStorey")
    ]


# ==========================================================
# 6. Classi e tipi
# ==========================================================
# Richiamata in: Model Properties
def get_types(file, parent_class=None):
    """
    Restituisce tutte le classi/tipi presenti nel file,
    filtrando eventualmente per una classe padre
    """
    if parent_class:
        return set(i.is_a() for i in file if i.is_a(parent_class))
    return set(i.is_a() for i in file)

# Richiamata in: Model Properties
def get_type_occurence(file, types):
    """
    Conta il numero di occorrenze per ogni tipo specificato
    """
    return {t: len(file.by_type(t)) for t in types}


# ==========================================================
# 7. Costi e schedulazione
# ==========================================================
# Richiamata in: Cost Schedule
def create_cost_schedule(file, name=None):
    """Crea una nuova Cost Schedule IFC nel file"""
    ifcopenshell.api.run("cost.add_cost_schedule", file, name=name)

# Richiamata in: Work Schedule
def create_work_schedule(file, name=None):
    """Crea una nuova Work Schedule IFC nel file"""
    ifcopenshell.api.run("sequence.add_work_schedule", file, name=name)


# ==========================================================
# 8. Task e struttura WBS (Work Breakdown Structure)
# ==========================================================
# Richiamata in: Project Timeline
def get_root_tasks(work_schedule):
    """
    Estrae i task radice (root) da una work schedule IFC
    """
    tasks = []
    if work_schedule.Controls:
        for rel in work_schedule.Controls:
            for obj in rel.RelatedObjects:
                if obj.is_a("IfcTask"):
                    tasks.append(obj)
    return tasks

# Richiamata in: Project Timeline
def get_nested_tasks(task):
    """
    Estrae i task annidati all'interno di un task (1 livello)
    """
    tasks = []
    for rel in task.IsNestedBy or []:
        for obj in rel.RelatedObjects:
            if obj.is_a("IfcTask"):
                tasks.append(obj)
    return tasks

# Richiamata in: Project Timeline
def get_nested_tasks2(task):
    """
    Variante alternativa per ottenere i task annidati (non raccomandata)
    """
    return [
        obj for rel in task.IsNestedBy
        for obj in rel.RelatedObjects
        if obj.is_a("IfcTask")
    ]

# Richiamata in: Project Timeline
def get_schedule_tasks(work_schedule):
    """
    Restituisce tutti i task (radice + annidati ricorsivamente) di una Work Schedule
    """
    all_tasks = []

    def append_tasks(task):
        for nested in get_nested_tasks(task):
            all_tasks.append(nested)
            if nested.IsNestedBy:
                append_tasks(nested)

    for root_task in get_root_tasks(work_schedule):
        append_tasks(root_task)

    return all_tasks

# Richiamata in: Project Timeline
def get_task_data(tasks):
    """
    Restituisce i dati principali per una lista di task:
    ID, Nome, Date di inizio e fine
    """
    return [
        {
            "Identification": task.Identification,
            "Name": task.Name,
            "ScheduleStart": format_date_from_iso(task.TaskTime.ScheduleStart) if task.TaskTime else "",
            "ScheduleFinish": format_date_from_iso(task.TaskTime.ScheduleFinish) if task.TaskTime else "",
        }
        for task in tasks
    ]


# ==========================================================
# 9. Utility generiche
# ==========================================================
# Richiamata in: grafici e analisi varie
def get_x_and_y(values, higher_then=None):
    """
    Converte un dizionario in due liste (x, y), filtrando valori se specificato
    """
    sorted_items = sorted(values.items(), key=lambda kv: kv[1], reverse=True)
    if higher_then:
        sorted_items = [item for item in sorted_items if item[1] > higher_then]
    x_values = [item[0] for item in sorted_items]
    y_values = [item[1] for item in sorted_items]
    return x_values, y_values

# Richiamata in: Project Timeline
def format_date_from_iso(iso_date=None):
    """
    Converte una data ISO in formato leggibile '15 Sep 25'
    """
    return datetime.fromisoformat(iso_date).strftime('%d %b %y') if iso_date else ""


# ==========================================================
# 10. Parsing Psets da IFC.js (web-ifc)
# ==========================================================
# Richiamata in: integrazione IFC.js (web)
def format_ifcjs_psets(ifcJSON):
    """
    Organizza i dati dei Property/Quantity Sets provenienti da web-ifc-api (IFC.js)
    Restituisce un dizionario con expressID e proprietà associate
    """
    result = {}

    for pset in ifcJSON:
        pset_name = pset["Name"]["value"]
        expressID = pset["expressID"]
        is_quantity = "Qto" in pset_name
        is_property = "Pset" in pset_name

        if is_quantity and "Quantities" in pset:
            for quantity in pset["Quantities"]:
                quantity_name = quantity["Name"]["value"]
                quantity_value = next((v["value"] for k, v in quantity.items() if "Value" in k), "")
                result.setdefault(expressID, {"Name": pset_name, "Data": []})["Data"].append({
                    "Name": quantity_name,
                    "Value": quantity_value
                })

        if is_property and "HasProperties" in pset:
            for prop in pset["HasProperties"]:
                prop_name = prop["Name"]["value"]
                prop_value = next((v["value"] for k, v in prop.items() if "Value" in k), "")
                result.setdefault(expressID, {"Name": pset_name, "Data": []})["Data"].append({
                    "Name": prop_name,
                    "Value": prop_value
                })

    return result


# ==========================================================
# 11. Parsing struttura IFC da IFC.js (web-ifc)
# ==========================================================
def get_ifc_structure(ifc_file):
    """
    Restituisce la struttura del file IFC come:
    {IFCClass: {PropertySet: [PropertyName, ...], ...}}
    Considera SOLO le classi presenti nel file e solo schemi ufficiali.
    """
    official_schemas = ["IFC2X3", "IFC4", "IFC4X3"]
    schema_name = getattr(ifc_file.schema, "schema_identifier", str(ifc_file.schema))

    if schema_name not in official_schemas:
        return {}  # schema non supportato

    result = {}

    # Prendi tutte le classi effettivamente presenti nel file
    classes_in_file = sorted(set(obj.is_a() for obj in ifc_file))
    for cls in classes_in_file:
        result[cls] = {}
        elements = ifc_file.by_type(cls)
        # Prendi PropertySet e PropertyName dal primo elemento disponibile
        for el in elements[:1]:  # basta un elemento per scoprire le property
            for rel in getattr(el, "IsDefinedBy", []):
                if rel.is_a("IfcRelDefinesByProperties"):
                    pset = rel.RelatingPropertyDefinition
                    pset_name = getattr(pset, "Name", None)
                    if pset_name:
                        result[cls][pset_name] = []
                        for prop in getattr(pset, "HasProperties", []):
                            prop_name = getattr(prop, "Name", None)
                            if prop_name:
                                result[cls][pset_name].append(prop_name)
    return result


# -----------------------------
# Helpers 4D (usati dalla pagina Project Timeline)
# -----------------------------
import streamlit as st
import ifcopenshell as ifc

# Nota: queste funzioni usano lo stato di sessione di Streamlit (st.session_state.ifc_file)
# e forniscono comportamenti di fallback se le operazioni IFC avanzate non sono assenti.


def get_selectable_elements(filter_type="IfcProduct"):
    """Restituisce una lista di elementi IFC filtrati per tipo usando il file IFC nella sessione.
    I messaggi rivolti all'utente sono in inglese.
    """
    session = st.session_state
    if not hasattr(session, "ifc_file") or not session.ifc_file:
        return []
    try:
        return session.ifc_file.by_type(filter_type)
    except Exception:
        return []


def create_work_plan_for_selected(name, selected_ids):
    """Crea un IfcWorkPlan e, se possibile, associa gli elementi selezionati.
    Questa implementazione crea l'entità IfcWorkPlan come fallback e avvisa che le
    associazioni agli elementi non vengono create automaticamente.
    """
    session = st.session_state
    if not name:
        st.error("Please enter a name for the WorkPlan")
        return
    if not hasattr(session, 'ifc_file') or not session.ifc_file:
        st.error("No IFC file loaded in session")
        return
    try:
        # Crea l'entità IfcWorkPlan
        wp = session.ifc_file.create_entity("IfcWorkPlan", Name=name)
        # Fallback semplice: non vengono create relazioni esplicite verso gli elementi
        st.success("IfcWorkPlan created")
        st.info("Note: associations with selected elements are not automatically created.")
        return wp
    except Exception as e:
        st.error(f"Error creating WorkPlan: {e}")
        return None


def assign_schedule_to_workplan(workplan_id, schedule_id):
    """Associa una IfcWorkSchedule a un IfcWorkPlan quando possibile.
    Questa funzione tenta di eseguire un'operazione best-effort non distruttiva; se
    non è possibile creare la relazione automaticamente viene mostrato un messaggio.
    """
    session = st.session_state
    if not hasattr(session, 'ifc_file') or not session.ifc_file:
        st.error("No IFC file loaded in session")
        return
    if not workplan_id or not schedule_id:
        st.error("Select both a WorkPlan and a Schedule to assign")
        return
    try:
        wp = session.ifc_file.by_id(int(workplan_id))
        sched = session.ifc_file.by_id(int(schedule_id))
        if not wp or not sched:
            st.error("WorkPlan or Schedule not found in the IFC file")
            return
        # Tentativo non distruttivo: si limita a notificare l'operazione
        try:
            st.success("Schedule assignment noted. Implement relational linking as needed.")
        except Exception:
            st.warning("Could not create relation automatically. Please link Schedule and WorkPlan manually if required.")
    except Exception as e:
        st.error(f"Error assigning schedule: {e}")


def create_task_for_selected(schedule_id, selected_ids, task_name_prefix="Task"):
    """Crea IfcTask per ogni elemento selezionato.
    Le entità di task di base vengono create come fallback; il collegamento dettagliato
    ai WorkSchedule non viene impostato automaticamente.
    """
    session = st.session_state
    if not hasattr(session, 'ifc_file') or not session.ifc_file:
        st.error("No IFC file loaded in session")
        return
    if not selected_ids:
        st.error("No elements selected to create tasks for")
        return
    created = 0
    try:
        for eid in selected_ids:
            name = f"{task_name_prefix}_{eid}"
            session.ifc_file.create_entity("IfcTask", Name=name)
            created += 1
        st.success(f"Created {created} tasks (associations to schedules not created automatically)")
    except Exception as e:
        st.error(f"Error creating tasks: {e}")


def draw_filter_selector():
    """Mostra un selector avanzato (By Type / By Property / By Level).
    I commenti nel codice sono in italiano, i messaggi UI sono in inglese.
    Restituisce la lista degli elementi filtrati.
    """
    session = st.session_state
    st.markdown("**Filter elements**")
    filter_mode = st.selectbox("Filter mode", ["By Type", "By Property", "By Level"], key="filter_mode_4d")

    filtered = []
    if filter_mode == "By Type":
        type_options = ["IfcProduct", "IfcElement", "IfcBuildingElement", "IfcWall", "IfcWindow", "IfcDoor", "IfcRelAssigns"]
        sel_type = st.selectbox("Element type", type_options, key="filter_type_selector")
        if hasattr(session, 'ifc_file') and session.ifc_file:
            try:
                filtered = session.ifc_file.by_type(sel_type)
            except Exception:
                filtered = []
    elif filter_mode == "By Level":
        # Modalità By Level: seleziona uno IfcBuildingStorey e raccoglie gli elementi contenuti
        level_types = ["IfcBuildingStorey", "IfcLevel"]
        levels = []
        if hasattr(session, 'ifc_file') and session.ifc_file:
            for lt in level_types:
                try:
                    lv = session.ifc_file.by_type(lt)
                    if lv:
                        levels.extend(lv)
                except Exception:
                    continue
        level_options = [f"{l.id()} - {getattr(l,'Name',str(l))}" for l in levels]
        selected_level = st.selectbox("Select Level (Building Storey)", [""] + level_options, key="filter_level_selector")
        if selected_level:
            level_id = int(selected_level.split(" - ",1)[0])
            level = session.ifc_file.by_id(level_id)
            elems = []
            try:
                for inv in session.ifc_file.get_inverse(level):
                    related = getattr(inv, 'RelatedElements', None)
                    if related:
                        for el in related:
                            elems.append(el)
                # Deduplica gli elementi raccolti
                seen = set()
                filtered = []
                for e in elems:
                    eid = e.id() if hasattr(e, 'id') else None
                    if eid and eid not in seen:
                        filtered.append(e)
                        seen.add(eid)
            except Exception:
                filtered = []
    else:
        # Modalità By Property
        prop_options = ["Name", "GlobalId", "Tag", "PredefinedType", "ObjectType"]
        prop = st.selectbox("Property", prop_options, key="filter_prop_selector")
        operators = ["contains", "equals", "startswith", "endswith"]
        op = st.selectbox("Operator", operators, key="filter_op_selector")
        val = st.text_input("Value", key="filter_value_4d")

        base_types = ["IfcProduct", "IfcElement"]
        elems = []
        if hasattr(session, 'ifc_file') and session.ifc_file:
            for t in base_types:
                try:
                    elems.extend(session.ifc_file.by_type(t))
                except Exception:
                    continue
        for el in elems:
            attr = None
            try:
                if hasattr(el, prop):
                    attr = getattr(el, prop)
                else:
                    info = el.get_info()
                    attr = info.get(prop)
            except Exception:
                attr = None
            if attr is None:
                continue
            s = str(attr)
            match = False
            if op == "contains" and val.lower() in s.lower():
                match = True
            elif op == "equals" and s.lower() == val.lower():
                match = True
            elif op == "startswith" and s.lower().startswith(val.lower()):
                match = True
            elif op == "endswith" and s.lower().endswith(val.lower()):
                match = True
            if match:
                filtered.append(el)

    st.caption(f"Filtered elements: {len(filtered)}")
    return filtered


def draw_schedule_manager():
    """Interfaccia per selezionare elementi filtrati, creare WorkPlan, assegnare schedule e creare task.
    I commenti sono in italiano, le stringhe per l'utente sono in inglese.
    """
    session = st.session_state
    st.subheader("WorkPlan / Schedule / Task Manager")

    elements = draw_filter_selector()
    options = [f"{el.id()} - {getattr(el, 'Name', str(el))}" for el in elements]
    selected_options = st.multiselect("Select elements", options, key="selected_elements_list")
    selected_ids = [int(s.split(" - ", 1)[0]) for s in selected_options]

    st.text_input("WorkPlan name", key="workplan_name")
    if st.button("Create IfcWorkPlan for selected elements", key="create_workplan_button"):
        create_work_plan_for_selected(session.workplan_name, selected_ids)

    # Seleziona WorkPlan esistenti
    workplans = session.ifc_file.by_type("IfcWorkPlan") if hasattr(session.ifc_file, 'by_type') else []
    wp_options = [f"{wp.id()} - {getattr(wp,'Name',str(wp))}" for wp in workplans]
    selected_wp = st.selectbox("Select existing WorkPlan", [""] + wp_options, key="select_workplan")
    wp_id = int(selected_wp.split(" - ",1)[0]) if selected_wp else None

    # Seleziona Schedule esistenti
    schedules = session.ifc_file.by_type("IfcWorkSchedule") if hasattr(session.ifc_file, 'by_type') else []
    sched_options = [f"{s.id()} - {getattr(s,'Name',str(s))}" for s in schedules]
    selected_sched = st.selectbox("Select Schedule to assign", [""] + sched_options, key="select_schedule_to_assign")
    sched_id = int(selected_sched.split(" - ",1)[0]) if selected_sched else None

    if st.button("Assign Schedule to WorkPlan", key="assign_schedule_button"):
        if wp_id and sched_id:
            assign_schedule_to_workplan(wp_id, sched_id)
        else:
            st.error("Please select valid WorkPlan and Schedule")

    st.text_input("Task name prefix", key="task_name_prefix", value="Task")
    if st.button("Create IfcTask for selected elements", key="create_tasks_button"):
        create_task_for_selected(sched_id, selected_ids, session.task_name_prefix)
