# ─────────────────────────────────────────────
# 📦 Importazioni (solo quelle necessarie)
# ─────────────────────────────────────────────
import ifcopenshell as ifc
import streamlit as st
from tools import ifchelper

# ─────────────────────────────────────────────
# 🧠 Alias per lo stato della sessione Streamlit
# ─────────────────────────────────────────────
session = st.session_state 

# -----------------------------
# ORGANIZZAZIONE DELLA PAGINA
# -----------------------------
# Elenco funzioni/aree (in italiano):
# 1) initialize_session_state -> USATA: esecuzione pagina; SCOPO: inizializza lo stato di sessione
# 2) load_work_schedules -> USATA: Tab 'Schedules'; SCOPO: carica IfcWorkSchedule e IfcTask dal file IFC
# 3) add_work_schedule -> USATA: Sidebar (Work Scheduler); SCOPO: crea una IfcWorkSchedule
# 4) draw_schedules -> USATA: Tab 'Schedules'; SCOPO: mostra le schedule caricate e le attività correlate
# 5) Funzioni di debug (initialise_debug_props, get_object_data, edit_object_data) -> USATE: Tab 'Debug'; SCOPO: ispezione e debug oggetti IFC
# 6) execute -> ENTRY POINT: costruisce UI, tab e sidebar (output in inglese)

def initialize_session_state():
    """Inizializza lo stato di sessione usando chiavi note al resto della pagina."""
    session["isHealthDataLoaded"] = False
    session["HealthData"] = {}
    session["Graphs"] = {}
    session["SequenceData"] = {
        "schedules": [],
        "tasks": [],
        "ScheduleData": []
    }
    session["CostScheduleData"] = {}


def load_work_schedules():
    """Carica le WorkSchedule e le Task dal file IFC nello stato di sessione."""
    session["SequenceData"]["schedules"] = session.ifc_file.by_type("IfcWorkSchedule")
    session["SequenceData"]["tasks"] = session.ifc_file.by_type("IfcTask")
    session["SequenceData"]["ScheduleData"] = [
        {"Id": schedule.id(), "Data": ifchelper.get_schedule_tasks(schedule)}
        for schedule in session.ifc_file.by_type("IfcWorkSchedule")
    ]


def add_work_schedule():
    """Crea una nuova WorkSchedule con il nome inserito nella sidebar e ricarica i dati."""
    ifchelper.create_work_schedule(session.ifc_file, session["schedule_input"])
    load_work_schedules()
    

def draw_schedules():
    """Disegna la tabella delle schedule e delle task associate."""
    # Evita errori se SequenceData o schedules non sono presenti
    if "SequenceData" not in session or "schedules" not in session["SequenceData"]:
        st.warning("No schedule data available. Please load or create a schedule.")
        return
    
    number_of_schedules = len(session["SequenceData"]["schedules"])
    st.subheader(f'Work Schedules: {number_of_schedules}')
    schedules = [f'{work_schedule.Name} / {work_schedule.id()}'  for work_schedule in session["SequenceData"]["schedules"] or []]
    st.selectbox("Schedules", schedules, key="schedule_selector" )
    schedule_id = int(session.schedule_selector.split("/",1)[1]) if session.schedule_selector else None
    schedule = session.ifc_file.by_id(schedule_id) if schedule_id else None
    if schedule:
        tasks = ifchelper.get_schedule_tasks(schedule) if schedule else None
        if tasks:
            st.info(f'Number of Tasks : {len(tasks)}')
            task_data = ifchelper.get_task_data(tasks)
            st.table(task_data)
        else:
            st.warning("No tasks loaded for this schedule")
    else:
        st.warning("No schedules loaded")


# ─────────────────────────────────────────────
# 🔧 Funzioni di supporto al debug IFC
# ─────────────────────────────────────────────

def initialise_debug_props(force=False):
    """Inizializza (o reimposta se force=True) le proprietà di debug IFC."""
    if not "BIMDebugProperties" in session:
        session.BIMDebugProperties = {
            "step_id": 0,
            "number_of_polygons": 0,
            "percentile_of_polygons": 0,
            "active_step_id": 0,
            "step_id_breadcrumb": [],
            "attributes": [],
            "inverse_attributes": [],
            "inverse_references": [],
            "express_file": None,
        }
    if force:
        session.BIMDebugProperties = {
            "step_id": 0,
            "number_of_polygons": 0,
            "percentile_of_polygons": 0,
            "active_step_id": 0,
            "step_id_breadcrumb": [],
            "attributes": [],
            "inverse_attributes": [],
            "inverse_references": [],
            "express_file": None,
        }


def get_object_data(fromId=None):
    """Popola le proprietà di debug a partire da uno STEP id IFC."""
    def add_attribute(prop, key, value):
        # Gestione tuple lunghe/corte per una migliore visualizzazione
        if isinstance(value, tuple) and len(value) < 10:
            for i, item in enumerate(value):
                add_attribute(prop, key + f"[{i}]", item)
            return
        elif isinstance(value, tuple) and len(value) >= 10:
            key = key + "({})".format(len(value))
        
        propy = {
            "name": key,
            "string_value": str(value),
            "int_value": int(value.id()) if isinstance(value, ifc.entity_instance) else None,
        }
        prop.append(propy)
            
    if session.BIMDebugProperties:
        initialise_debug_props(force=True)
        step_id = 0
        if fromId:
            step_id = fromId
        else:
            step_id = int(session.object_id) if session.object_id else 0
        debug_props = st.session_state.BIMDebugProperties
        debug_props["active_step_id"] = step_id
        crumb = {"name": str(step_id)}
        debug_props["step_id_breadcrumb"].append(crumb)
        element = session.ifc_file.by_id(step_id)
        debug_props["inverse_attributes"] = []
        debug_props["inverse_references"] = []
        
        for key, value in element.get_info().items():
            add_attribute(debug_props["attributes"], key, value)

        for key in dir(element):
            if (
                not key[0].isalpha()
                or key[0] != key[0].upper()
                or key in element.get_info()
                or not getattr(element, key)
            ):
                continue
            add_attribute(debug_props["inverse_attributes"], key, getattr(element, key))
        
        for inverse in session.ifc_file.get_inverse(element):
            propy = {
                "string_value": str(inverse),
                "int_value": inverse.id(),
            }
            debug_props["inverse_references"].append(propy)
            
        print(debug_props["attributes"])


def edit_object_data(object_id, attribute):
    """Esempio di funzione per modificare un attributo (placeholder)."""
    entity = session.ifc_file.by_id(object_id)
    print(getattr(entity, attribute))
    

# ─────────────────────────────────────────────
# 🚀 Entry point della pagina
# ─────────────────────────────────────────────

def execute():
    """Costruisce UI, tab e sidebar della pagina 4D (output in inglese)."""
    
    # Inizializza proprieta' di debug
    initialise_debug_props()

    # Intestazione e descrizione (output in inglese)
    st.header(" 📅 Project Timeline")
    # Brief: gestione timeline 4D con IFC WorkSchedules/WorkPlans/Tasks
    st.markdown(
        """
        This page manages the project timeline (4D) using IFC WorkSchedules, WorkPlans and IfcTasks. 
        Use the selector and Schedule Manager to create, assign and review schedules and tasks linked to model elements.
        """
    )
    st.markdown("Reference: [IFC4x3 Construction Scheduling - buildingSMART](https://ifc43-docs.standards.buildingsmart.org/IFC/RELEASE/IFC4x3/HTML/annex_e/construction-scheduling/construction-scheduling-task.html)")

    # Garantisce che lo stato sia inizializzato
    if "isHealthDataLoaded" not in session or "SequenceData" not in session:
        initialize_session_state()

    if session.isHealthDataLoaded:
        # Tabs principali (Debug e Schedules)
        tab1, tab2 = st.tabs(["🔎 Debug", "📝 Schedules"])
        
        # Replica pannello di debug IFC
        with tab1:
            row1_col1, row1_col2 = st.columns([1,5])
            with row1_col1:
                st.text_input("Object ID", key="object_id")
                st.button("Inspect from Object Id", key="get_object_button", on_click=get_object_data, args=(session.object_id,))
            if "BIMDebugProperties" in session and session.BIMDebugProperties:
                props = session.BIMDebugProperties
                # Attributi diretti
                if props["attributes"]:
                    st.subheader("Attributes")
                    for prop in props["attributes"]:
                        col2, col3 = st.columns([3,3])
                        if prop["int_value"]:
                            col2.text(f'🔗 {prop["name"]}')
                            col2.info(prop["string_value"])
                            col3.text("🔗")
                            col3.button("Get Object", key=f'get_object_pop_button_{prop["int_value"]}', on_click=get_object_data, args=(prop["int_value"],))
                        else:
                            col2.text_input(label=prop["name"], key=prop["name"], value=prop["string_value"])
                
                # Attributi inversi          
                if props["inverse_attributes"]:
                    st.subheader("Inverse Attributes")
                    for inverse in props["inverse_attributes"]:
                        col1, col2, col3 = st.columns([3,5,8])
                        col1.text(inverse["name"])
                        col2.text(inverse["string_value"])
                        if inverse["int_value"]:
                            col3.button("Get Object", key=f'get_object_pop_button_{inverse["int_value"]}', on_click=get_object_data, args=(inverse["int_value"],))

                # Riferimenti inversi   
                if props["inverse_references"]:
                    st.subheader("Inverse References")
                    for inverse in props["inverse_references"]:
                        col1, col3 = st.columns([3,3])
                        col1.text(inverse["string_value"])
                        if inverse["int_value"]:
                            col3.button("Get Object", key=f'get_object_pop_button_inverse_{inverse["int_value"]}', on_click=get_object_data, args=(inverse["int_value"],))
        
        # Tab Schedules
        with tab2:
            draw_schedules()

        # Sidebar integrata: Work Scheduler e salvataggio (output in inglese)
        def save_file():
            """Salva il file IFC corrente sul percorso noto in sessione."""
            session.ifc_file.write(session.file_name)
        
        st.sidebar.header("📅 Work Scheduler")
        st.sidebar.text_input("✏️ Schedule Name", key="schedule_input")
        st.sidebar.button("➕ Add Schedule", key="add_work_schedule_button", on_click=add_work_schedule)
        st.sidebar.button("💾 Save File", key="save_file", on_click=save_file)
    else:
        # Istruzione iniziale quando nessun file è caricato (output in inglese)
        st.header("Step 1: Load a file from the Home Page")


# Esegue la pagina
execute()