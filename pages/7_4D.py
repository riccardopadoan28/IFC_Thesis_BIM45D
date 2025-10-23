# -----------------------------
# ORGANIZZAZIONE DELLA PAGINA
# -----------------------------
# Elenco funzioni/aree (in italiano):
# 1) initialize_session_state -> USATA: esecuzione pagina; SCOPO: inizializza lo stato di sessione
# 2) load_work_schedules -> USATA: Tab 'Schedules'; SCOPO: carica IfcWorkSchedule e IfcTask dal file IFC
# 3) add_work_schedule -> USATA: Sidebar (Work Scheduler); SCOPO: crea una IfcWorkSchedule
# 4) draw_schedules -> USATA: Tab 'Schedules'; SCOPO: mostra le schedule caricate e le attività correlate
# 5) Helper locali (format_date_from_iso, create_work_schedule, get_*_tasks, get_task_data) -> USATE: supporto dati e formattazione
# 6) execute -> ENTRY POINT: costruisce UI, tab e sidebar (output in inglese)

# ─────────────────────────────────────────────
# 📦 Importazioni (solo quelle necessarie)
# ─────────────────────────────────────────────
import ifcopenshell as ifc
import streamlit as st
from datetime import datetime
import pandas as pd
from ifcopenshell.util import element as ifc_element
from ifcopenshell.guid import new as new_guid

# ─────────────────────────────────────────────
# 🔁 Funzioni spostate da tools.ifchelper e rese locali a questa pagina
# Nota: commenti in italiano, output UI in inglese
# ─────────────────────────────────────────────

def format_date_from_iso(iso_date=None):
    """Formatta una stringa ISO in '15 Sep 25'; ritorna stringa vuota se non valida."""
    try:
        return datetime.fromisoformat(iso_date).strftime('%d %b %y') if iso_date else ''
    except Exception:
        return ''


def create_work_schedule(model, name=None):
    """Crea una IfcWorkSchedule nel modello IFC utilizzando ifcopenshell.api."""
    try:
        ifc.api.run('sequence.add_work_schedule', model, name=name)
    except Exception as e:
        print(f'Error creating work schedule: {e}')


def get_root_tasks(work_schedule):
    """Ritorna le task radice (IfcTask) referenziate direttamente dalla IfcWorkSchedule."""
    tasks = []
    if getattr(work_schedule, 'Controls', None):
        for rel in work_schedule.Controls:
            for obj in getattr(rel, 'RelatedObjects', []) or []:
                if obj.is_a('IfcTask'):
                    tasks.append(obj)
    return tasks


def get_nested_tasks(task):
    """Ritorna le task annidate di primo livello per una IfcTask fornita."""
    tasks = []
    for rel in getattr(task, 'IsNestedBy', []) or []:
        for obj in getattr(rel, 'RelatedObjects', []) or []:
            if obj.is_a('IfcTask'):
                tasks.append(obj)
    return tasks


def get_schedule_tasks(work_schedule):
    """Ritorna tutte le task (radice + annidate ricorsivamente) per una IfcWorkSchedule."""
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
    """Converte una lista di IfcTask in dict semplificati: Identification, Name, Start, Finish."""
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


def get_all_schedule_task_ids(ifc_file):
    """Ritorna l'insieme degli id() delle IfcTask presenti in qualunque IfcWorkSchedule (incluse le radici)."""
    task_ids = set()
    schedules = ifc_file.by_type("IfcWorkSchedule") or []
    for ws in schedules:
        for root in get_root_tasks(ws):
            try:
                task_ids.add(root.id())
            except Exception:
                pass
            # ricorsione su task annidate
            def add_desc(t):
                for n in get_nested_tasks(t):
                    try:
                        task_ids.add(n.id())
                    except Exception:
                        pass
                    add_desc(n)
            add_desc(root)
    return task_ids


def get_scheduled_element_ids(ifc_file):
    """Ritorna un set di ExpressID per gli elementi collegati a task di qualunque WorkSchedule (IfcRelAssignsToProcess)."""
    scheduled = set()
    try:
        task_ids = get_all_schedule_task_ids(ifc_file)
        for rel in ifc_file.by_type("IfcRelAssignsToProcess") or []:
            try:
                proc = getattr(rel, 'RelatingProcess', None)
                if proc and hasattr(proc, 'id') and proc.id() in task_ids:
                    for obj in getattr(rel, 'RelatedObjects', []) or []:
                        if obj.is_a('IfcElement') or obj.is_a('IfcProduct'):
                            scheduled.add(obj.id())
            except Exception:
                continue
    except Exception:
        pass
    return scheduled


def build_unscheduled_df(ifc_file):
    """Crea un DataFrame Pandas con tutti gli IfcElement che non risultano assegnati a nessuna WorkSchedule."""
    rows = []
    scheduled_ids = get_scheduled_element_ids(ifc_file)
    try:
        elements = ifc_file.by_type('IfcElement') or []
    except Exception:
        elements = []
    for el in elements:
        try:
            eid = el.id() if hasattr(el, 'id') else None
            if eid in scheduled_ids:
                continue
            container = None
            try:
                c = ifc_element.get_container(el)
                container = c.Name if c is not None else None
            except Exception:
                container = None
            tname = None
            try:
                t = ifc_element.get_type(el)
                tname = t.Name if t is not None else None
            except Exception:
                tname = None
            rows.append({
                'ExpressId': eid,
                'GlobalId': getattr(el, 'GlobalId', None),
                'Class': el.is_a() if hasattr(el, 'is_a') else None,
                'Name': getattr(el, 'Name', None),
                'Level': container,
                'Type': tname,
            })
        except Exception:
            continue
    return pd.DataFrame(rows)

# ─────────────────────────────────────────────
# 🧠 Alias per lo stato della sessione Streamlit
# ─────────────────────────────────────────────
session = st.session_state 


# ─────────────────────────────────────────────
# ⚙️ Funzioni principali della pagina
# ─────────────────────────────────────────────

def initialize_session_state():
    """Inizializza lo stato di sessione con chiavi usate dalla pagina (health, grafici, sequenze)."""
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
    """Carica IfcWorkSchedule e IfcTask dal file in sessione e popola SequenceData."""
    session["SequenceData"]["schedules"] = session.ifc_file.by_type("IfcWorkSchedule")
    session["SequenceData"]["tasks"] = session.ifc_file.by_type("IfcTask")
    session["SequenceData"]["ScheduleData"] = [
        {"Id": schedule.id(), "Data": get_schedule_tasks(schedule)}
        for schedule in session.ifc_file.by_type("IfcWorkSchedule")
    ]


def add_work_schedule():
    """Crea una IfcWorkSchedule con il nome inserito nella sidebar e ricarica i dati in sessione."""
    create_work_schedule(session.ifc_file, session["schedule_input"])
    load_work_schedules()


def delete_work_schedule(schedule_id: int):
    """Elimina la WorkSchedule con l'ExpressID fornito e aggiorna la lista."""
    try:
        ws = session.ifc_file.by_id(int(schedule_id))
        if not ws:
            st.error("WorkSchedule not found")
            return
        try:
            ifc.api.run('sequence.remove_work_schedule', session.ifc_file, work_schedule=ws)
        except Exception:
            try:
                session.ifc_file.remove(ws)
            except Exception:
                st.error("Unable to delete WorkSchedule")
                return
        load_work_schedules()
        st.success("WorkSchedule deleted")
    except Exception as e:
        st.error(f"Error deleting WorkSchedule: {e}")
    

def draw_schedules():
    """Mostra elenco delle schedule come tabella con conteggio delle task associate e colonna Delete."""
    # Evita errori se SequenceData o schedules non sono presenti
    if "SequenceData" not in session or "schedules" not in session["SequenceData"]:
        st.warning("No schedule data available. Please load or create a schedule.")
        return
    
    schedules = session["SequenceData"].get("schedules") or []
    st.subheader(f'Work Schedules: {len(schedules)}')
    st.markdown("This table lists all WorkSchedules available in the model. If none exist, create one from the 'Unscheduled' tab and then come back here.")

    if not schedules:
        st.info("No schedules found. Create one from the 'Unscheduled' tab.")
        return

    # Intestazioni
    h1, h2, h3, h4 = st.columns([1, 5, 2, 2])
    h1.markdown("**Id**")
    h2.markdown("**Name**")
    h3.markdown("**TaskCount**")
    h4.markdown("**Delete**")

    # Righe
    for ws in schedules:
        try:
            task_count = len(get_schedule_tasks(ws))
        except Exception:
            task_count = 0
        c1, c2, c3, c4 = st.columns([1, 5, 2, 2])
        ws_id = ws.id() if hasattr(ws, 'id') else None
        c1.write(ws_id)
        c2.write(getattr(ws, 'Name', None))
        c3.write(task_count)
        if c4.button("Delete", key=f"del_ws_{ws_id}"):
            delete_work_schedule(ws_id)

def assign_elements_to_schedule(schedule_id, element_ids, task_name_prefix='Task'):
    """Crea IfcTask per gli elementi selezionati e li associa alla WorkSchedule scelta (IfcRelAssignsToProcess)."""
    if not schedule_id:
        st.error('Please select a WorkSchedule')
        return
    if not element_ids:
        st.error('No selected elements to assign')
        return
    schedule = session.ifc_file.by_id(int(schedule_id))
    if not schedule:
        st.error('Selected WorkSchedule not found')
        return
    created = 0
    for eid in element_ids:
        el = session.ifc_file.by_id(int(eid))
        if not el:
            continue
        task = None
        # Crea la task nella schedule (preferibilmente via API)
        try:
            task = ifc.api.run('sequence.add_task', session.ifc_file, work_schedule=schedule, name=f"{task_name_prefix}_{eid}")
        except Exception:
            try:
                task = session.ifc_file.create_entity('IfcTask', Name=f"{task_name_prefix}_{eid}")
            except Exception:
                task = None
        if not task:
            continue
        # Associa elemento alla task (via API, fallback a entità diretta)
        try:
            ifc.api.run('sequence.assign_process', session.ifc_file, relating_process=task, related_objects=[el])
        except Exception:
            try:
                session.ifc_file.create_entity('IfcRelAssignsToProcess', GlobalId=new_guid(), RelatingProcess=task, RelatedObjects=[el])
            except Exception:
                pass
        created += 1
    # Aggiorna dati e feedback
    try:
        load_work_schedules()
    except Exception:
        pass
    st.success(f'Assigned tasks to {created} selected elements')

# ─────────────────────────────────────────────
# 🚀 Entry point della pagina
# ─────────────────────────────────────────────

def execute():
    """Costruisce UI, tab e sidebar della pagina 4D (output in inglese)."""
    
    # Intestazione e descrizione (output in inglese)
    st.header(" 📅 Project Timeline")
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

    # Rileva se un file IFC è caricato in sessione e allinea il flag health
    has_ifc = hasattr(session, "ifc_file") and session.ifc_file is not None
    if has_ifc:
        session.isHealthDataLoaded = True

    if session.isHealthDataLoaded and has_ifc:
        # Funzione di salvataggio disponibile nella tab Schedules
        def save_file():
            """Salva il file IFC corrente sul percorso noto in sessione."""
            session.ifc_file.write(session.file_name)

        # Tabs principali (Schedules, Unscheduled)
        (tab_schedules, tab_unscheduled) = st.tabs(["📝 Schedules", "🔍 Unscheduled"])
        
        # Tab Schedules
        with tab_schedules:
            # Carica i dati delle schedule se non presenti
            try:
                if not session["SequenceData"].get("schedules"):
                    load_work_schedules()
            except Exception:
                pass
            draw_schedules()
            # Pulsante di salvataggio spostato qui (tab 1)
            st.button("💾 Save File", key="save_file_tab", on_click=save_file)

        # Tab Unscheduled: DataFrame + filtri (Level/Class/Type)
        with tab_unscheduled:
            st.subheader("Unscheduled elements")
            st.markdown("Use the filters below to list elements not yet assigned to any WorkSchedule. If you need a new WorkSchedule, create it using the controls at the bottom; you can then view it in the 'Schedules' tab.")
            df_unscheduled = build_unscheduled_df(session.ifc_file)
            if df_unscheduled is None or df_unscheduled.empty:
                st.info("No unscheduled elements found.")
            else:
                # Selector per Level/Class/Type (con All)
                levels = ["All"] + sorted([v for v in df_unscheduled['Level'].dropna().unique()])
                classes = ["All"] + sorted([v for v in df_unscheduled['Class'].dropna().unique()])
                types = ["All"] + sorted([v for v in df_unscheduled['Type'].dropna().unique()])
                col1, col2, col3 = st.columns(3)
                sel_level = col1.selectbox("Level", levels, index=0, key="unsched_level")
                sel_class = col2.selectbox("Class", classes, index=0, key="unsched_class")
                sel_type = col3.selectbox("Type", types, index=0, key="unsched_type")
                # Applica filtri
                filtered = df_unscheduled.copy()
                if sel_level != "All":
                    filtered = filtered[filtered['Level'] == sel_level]
                if sel_class != "All":
                    filtered = filtered[filtered['Class'] == sel_class]
                if sel_type != "All":
                    filtered = filtered[filtered['Type'] == sel_type]
                st.caption(f"Unscheduled elements: {len(filtered)}")
                st.dataframe(filtered, use_container_width=True)

                # Seleziona elementi filtrati
                if st.button("Add a schedule to selection", key="add_schedule_to_selection"):
                    try:
                        ids = [int(x) for x in filtered['ExpressId'].dropna().tolist()]
                    except Exception:
                        ids = []
                    session["selected_element_ids"] = ids
                    st.success(f"Added {len(ids)} elements to selection")

                # Blocchi per creare/assegnare WorkSchedule nella pagina principale
                
                # Creazione nuova schedule
                st.text_input("New WorkSchedule name", key="schedule_input", help="Enter a name for the new WorkSchedule to be created.")
                if st.button("Add WorkSchedule", key="create_ws_main"):
                    add_work_schedule()

                # Selettore WorkSchedule esistente
                scheds = session.ifc_file.by_type('IfcWorkSchedule') or []
                sched_options = ["Select a schedule"] + [f"{s.id()} - {getattr(s,'Name',str(s))}" for s in scheds]
                sel_sched = st.selectbox("WorkSchedule", sched_options, index=0, key="unsched_sel_sched", help="Select an existing WorkSchedule to assign the selected elements.")
                sel_sched_id = int(sel_sched.split(' - ', 1)[0]) if sel_sched and sel_sched != "Select a schedule" else None
                # Prefisso per task e assegnazione (layout verticale, senza columns)
                task_prefix = st.text_input("Task name prefix", value="Task", key="assign_task_prefix", help="Prefix used to name tasks created for selected elements (e.g., Task_123)")
                if st.button("Assign selected elements to schedule", key="assign_selected_to_schedule"):
                    assign_elements_to_schedule(sel_sched_id, session.get("selected_element_ids", []), task_prefix)
                    st.success("WorkSchedule created. You can view it in the 'Schedules' tab.")
                

        # Rimuovo il pulsante di salvataggio dalla sidebar
        # Solo salvataggio in sidebar; gestione WorkSchedule spostata nella pagina principale
        # st.sidebar.button("💾 Save File", key="save_file", on_click=save_file)
    else:
        # Istruzione iniziale quando nessun file è caricato (output in inglese)
        st.header("Step 1: Load a file from the Home Page")


# Esegue la pagina
execute()