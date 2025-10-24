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
import datetime
import re

import ifcopenshell as ifc
import ifcopenshell
import ifcopenshell.api.sequence
import pandas as pd
import plotly.express as px
import streamlit as st

from ifcopenshell.guid import new as new_guid
from ifcopenshell.util.element import get_decomposition
from ifcopenshell.util import element as ifc_element
from ifcopenshell.guid import new as new_guid

from tools import ifc4D as ifc4d

# ─────────────────────────────────────────────
# 🧠 Alias per lo stato della sessione Streamlit
# ─────────────────────────────────────────────
session = st.session_state 

# Rimuovo gli helper IfcOpenShell locali e uso solo ifc4d

# ─────────────────────────────────────────────
# 🔁 Funzioni spostate da tools.ifchelper e rese locali a questa pagina
# Nota: commenti in italiano, output UI in inglese
# ─────────────────────────────────────────────

def format_date_from_iso(iso_date=None):
    """Formatta una stringa ISO in '15 Sep 25'; ritorna stringa vuota se non valida."""
    try:
        return datetime.datetime.fromisoformat(iso_date).strftime('%d %b %y') if iso_date else ''
    except Exception:
        return ''


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
        {"Id": schedule.id(), "Data": ifc4d.get_schedule_tasks(schedule)}
        for schedule in session.ifc_file.by_type("IfcWorkSchedule")
    ]


def add_work_schedule():
    """Crea una IfcWorkSchedule con attributi IFC4x3 (Identification, PredefinedType, Purpose, Start/Finish) e ricarica i dati."""
    start_dt = None
    finish_dt = None
    try:
        sd = session.get("ws_start_date")
        stime = session.get("ws_start_time")
        if sd and stime:
            start_dt = datetime.datetime.combine(sd, stime).isoformat()
    except Exception:
        start_dt = None
    try:
        fd = session.get("ws_finish_date")
        ftime = session.get("ws_finish_time")
        if fd and ftime:
            finish_dt = datetime.datetime.combine(fd, ftime).isoformat()
    except Exception:
        finish_dt = None

    ifc4d.create_work_schedule(
        session.ifc_file,
        name=session.get("schedule_input"),
        identification=session.get("ws_identification"),
        predefined_type=session.get("ws_predefined_type", "PLANNED"),
        start_time=start_dt,
        finish_time=finish_dt,
        purpose=session.get("ws_purpose"),
    )
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
    h1, h2, h3, h4 = st.columns([1, 5, 2, 2])
    h1.markdown("**Id**"); h2.markdown("**Name**"); h3.markdown("**TaskCount**"); h4.markdown("**Delete**")
    for ws in schedules:
        try:
            task_count = len(ifc4d.get_schedule_tasks(ws))
        except Exception:
            task_count = 0
        c1, c2, c3, c4 = st.columns([1, 5, 2, 2])
        ws_id = ws.id() if hasattr(ws, 'id') else None
        c1.write(ws_id)
        c2.write(getattr(ws, 'Name', None))
        c3.write(task_count)
        if c4.button("Delete", key=f"del_ws_{ws_id}"):
            delete_work_schedule(ws_id)

# Nuove funzioni di anteprima per Task e WorkPlan

def draw_task():
    try:
        tasks_list = session.ifc_file.by_type('IfcTask') or []
    except Exception:
        tasks_list = []
    st.subheader("Tasks")
    st.caption(f"IfcTask in model: {len(tasks_list)}")
    if not tasks_list:
        st.info("No IfcTask found.")
        return
    rows = []
    for t in tasks_list[:200]:
        tt = getattr(t, 'TaskTime', None)
        s = ifc4d._to_datetime(getattr(tt, 'ScheduleStart', None)) if tt else None
        f = ifc4d._to_datetime(getattr(tt, 'ScheduleFinish', None)) if tt else None
        rows.append({
            "Id": (t.id() if hasattr(t, 'id') else None),
            "Name": getattr(t, 'Name', None),
            "Identification": getattr(t, 'Identification', None),
            "Start": s.date().isoformat() if s else None,
            "Finish": f.date().isoformat() if f else None,
        })
    st.dataframe(pd.DataFrame(rows), use_container_width=True)


def draw_workplan():
    """Mostra IfcWorkPlan presenti nel modello con anteprima e conteggio."""
    try:
        plans_list = session.ifc_file.by_type('IfcWorkPlan') or []
    except Exception:
        plans_list = []
    st.subheader("Work Plans")
    st.caption(f"IfcWorkPlan in model: {len(plans_list)}")
    if not plans_list:
        st.info("No IfcWorkPlan found.")
        return
    rows = [{"Id": (p.id() if hasattr(p, 'id') else None), "Name": getattr(p, 'Name', None)} for p in plans_list[:200]]
    st.dataframe(pd.DataFrame(rows), use_container_width=True)

def assign_elements_to_schedule(schedule_id, element_ids, task_name_prefix='Task'):
    """Crea IfcTask per gli elementi selezionati dentro una WorkSchedule e collega process/control (usa ifc4d)."""
    if not schedule_id:
        st.error('Please select a WorkSchedule')
        return
    if not element_ids:
        st.error('No selected elements to assign')
        return
    created = ifc4d.create_tasks_for_elements_in_schedule(session.ifc_file, int(schedule_id), element_ids, task_name_prefix)
    if created:
        try:
            load_work_schedules()
        except Exception:
            pass
        st.success(f'Assigned tasks to {created} selected elements')
    else:
        st.warning('No tasks created')

def create_tasks_from_planner(schedule_id, df: pd.DataFrame, summary_name: str | None = "Plan Summary", link_sequential: bool = True):
    if not schedule_id:
        st.error('Please select a WorkSchedule')
        return
    schedule = session.ifc_file.by_id(int(schedule_id))
    if not schedule:
        st.error('Selected WorkSchedule not found')
        return
    summary_task = None
    if summary_name:
        try:
            for rel in getattr(schedule, 'Controls', []) or []:
                if rel.is_a('IfcRelAssignsToControl'):
                    for obj in getattr(rel, 'RelatedObjects', []) or []:
                        if obj.is_a('IfcTask') and getattr(obj, 'Name', None) == summary_name:
                            summary_task = obj
                            break
        except Exception:
            pass
        if not summary_task:
            try:
                summary_task = ifcopenshell.api.sequence.add_task(session.ifc_file, work_schedule=schedule, name=summary_name)
                try:
                    ifc.api.run('control.assign_control', session.ifc_file, relating_control=schedule, related_objects=[summary_task])
                except Exception:
                    session.ifc_file.create_entity('IfcRelAssignsToControl', GlobalId=new_guid(), RelatingControl=schedule, RelatedObjects=[summary_task])
            except Exception:
                summary_task = None

    def to_iso(d, t):
        try:
            if pd.isna(d) or pd.isna(t):
                return None
        except Exception:
            pass
        try:
            return datetime.datetime.combine(d, t).isoformat()
        except Exception:
            return None

    created_tasks = []
    for _, row in (df or pd.DataFrame()).iterrows():
        name = str(row.get('Name') or '').strip()
        if not name:
            continue
        ident = str(row.get('Identification')) if row.get('Identification') is not None else None
        dur = str(row.get('Duration')) if row.get('Duration') else None
        s_iso = to_iso(row.get('StartDate'), row.get('StartTime'))
        f_iso = to_iso(row.get('FinishDate'), row.get('FinishTime'))
        elem_str = row.get('ElementIds')
        task = None
        try:
            task = ifc.api.run('sequence.add_task', session.ifc_file, work_schedule=schedule, name=name, identification=ident)
        except Exception:
            try:
                task = session.ifc_file.create_entity('IfcTask', Name=name, Identification=ident)
            except Exception:
                task = None
        if not task:
            continue
        if s_iso or f_iso or dur:
            try:
                tt = session.ifc_file.create_entity('IfcTaskTime', ScheduleStart=s_iso, ScheduleFinish=f_iso, ScheduleDuration=dur)
                try:
                    task.TaskTime = tt
                except Exception:
                    pass
            except Exception:
                pass
        try:
            ifc.api.run('control.assign_control', session.ifc_file, relating_control=schedule, related_objects=[task])
        except Exception:
            try:
                session.ifc_file.create_entity('IfcRelAssignsToControl', GlobalId=new_guid(), RelatingControl=schedule, RelatedObjects=[task])
            except Exception:
                pass
        if summary_task:
            try:
                ifcopenshell.api.run('nest.assign_object', session.ifc_file, relating_object=summary_task, related_object=task)
            except Exception:
                try:
                    session.ifc_file.create_entity('IfcRelNests', GlobalId=new_guid(), RelatingObject=summary_task, RelatedObjects=[task])
                except Exception:
                    pass
        ids = []
        try:
            if elem_str is not None:
                for tok in re.split(r"[;,\s]+", str(elem_str).strip()):
                    if tok.isdigit():
                        ids.append(int(tok))
        except Exception:
            ids = []
        for eid in ids:
            el = session.ifc_file.by_id(int(eid))
            if not el:
                continue
            try:
                ifcopenshell.api.sequence.assign_product(session.ifc_file, relating_product=el, related_object=task)
            except Exception:
                try:
                    ifc.api.run('sequence.assign_process', session.ifc_file, relating_process=task, related_objects=[el])
                except Exception:
                    try:
                        session.ifc_file.create_entity('IfcRelAssignsToProcess', GlobalId=new_guid(), RelatingProcess=task, RelatedObjects=[el])
                    except Exception:
                        pass
        created_tasks.append(task)
    if link_sequential and len(created_tasks) > 1:
        for prev, curr in zip(created_tasks[:-1], created_tasks[1:]):
            try:
                ifcopenshell.api.sequence.assign_sequence(session.ifc_file, relating_process=prev, related_process=curr)
            except Exception:
                pass
    try:
        load_work_schedules()
    except Exception:
        pass
    st.success(f'Created {len(created_tasks)} tasks from table')

def create_tasks(element_ids: list[int], name_prefix: str = "Task", identification_prefix: str | None = None,
                              start_date=None, start_time=None, finish_date=None, finish_time=None, duration_iso: str | None = None,
                              mode: str = "per_element"):
    """Crea task con la stessa pianificazione per tutti gli elementi selezionati, senza associare ancora una WorkSchedule.
    mode: "per_element" crea una task per ogni elemento; "single" crea una sola task che raggruppa tutti gli elementi."""
    if not element_ids:
        st.error("No selected elements.")
        return
    # Prepara orari ISO
    s_iso = None; f_iso = None
    try:
        if start_date and start_time:
            s_iso = datetime.datetime.combine(start_date, start_time).isoformat()
    except Exception:
        s_iso = None
    try:
        if finish_date and finish_time:
            f_iso = datetime.datetime.combine(finish_date, finish_time).isoformat()
    except Exception:
        f_iso = None

    created = 0
    m = session.ifc_file
    if mode == "single":
        # Una sola task per tutti gli elementi
        tname = name_prefix.strip() or "Task"
        ident = (identification_prefix or None)
        try:
            task = m.create_entity('IfcTask', Name=tname, Identification=ident)
        except Exception:
            task = None
        if task:
            if s_iso or f_iso or duration_iso:
                try:
                    tt = m.create_entity('IfcTaskTime', ScheduleStart=s_iso, ScheduleFinish=f_iso, ScheduleDuration=duration_iso)
                    try:
                        task.TaskTime = tt
                    except Exception:
                        pass
                except Exception:
                    pass
            # Assegna tutti gli elementi
            objs = [m.by_id(int(e)) for e in element_ids if m.by_id(int(e)) is not None]
            if objs:
                try:
                    ifc.api.run('sequence.assign_process', m, relating_process=task, related_objects=objs)
                except Exception:
                    try:
                        m.create_entity('IfcRelAssignsToProcess', GlobalId=new_guid(), RelatingProcess=task, RelatedObjects=objs)
                    except Exception:
                        pass
            created = 1
    else:
        # Una task per ciascun elemento
        for eid in element_ids:
            el = session.ifc_file.by_id(int(eid))
            if not el:
                continue
            tname = f"{name_prefix}_{eid}" if name_prefix else f"Task_{eid}"
            ident = (f"{identification_prefix}{eid}" if identification_prefix else None)
            try:
                task = m.create_entity('IfcTask', Name=tname, Identification=ident)
            except Exception:
                task = None
            if not task:
                continue
            if s_iso or f_iso or duration_iso:
                try:
                    tt = m.create_entity('IfcTaskTime', ScheduleStart=s_iso, ScheduleFinish=f_iso, ScheduleDuration=duration_iso)
                    try:
                        task.TaskTime = tt
                    except Exception:
                        pass
                except Exception:
                    pass
            try:
                ifc.api.run('sequence.assign_process', m, relating_process=task, related_objects=[el])
            except Exception:
                try:
                    m.create_entity('IfcRelAssignsToProcess', GlobalId=new_guid(), RelatingProcess=task, RelatedObjects=[el])
                except Exception:
                    pass
            created += 1

    st.success(f"Created {created} simultaneous task(s)")

# ─────────────────────────────────────────────
# 🚀 Entry point della pagina
# ─────────────────────────────────────────────

def execute():
    """Costruisce UI, tab e sidebar della pagina 4D (output in inglese)."""
    
    # Intestazione e descrizione (output in inglese)
    st.header(" 📅 Project Timeline")
    st.markdown(
        """
        Manage the 4D project timeline with IFC WorkPlans, WorkSchedules, and IfcTasks.
        Use the tabs to: 1) check existing data, 2) build a work plan and aggregate schedules,
        3) create tasks from selected elements, 4) assign tasks to schedules, 5) manage work calendars,
        and 6) review the full nesting with an interactive Gantt chart.
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
        def save_file():
            session.ifc_file.write(session.file_name)

        (tab_check, tab_workplan,  tab_calendars, tab_schedules, tab_elements_tasks, tab_nesting) = st.tabs(["✅ Check", "🗂️ Work Plan", "🗓️ Work Calendars", "📝 Schedules → Tasks", "🧱 Tasks → Elements", "📊 Timeline & Gantt chart"])


        # Check tab
        with tab_check:
            st.subheader("Model contents")
            try:
                plans = session.ifc_file.by_type('IfcWorkPlan') or []
                schedules = session.ifc_file.by_type('IfcWorkSchedule') or []
                tasks = session.ifc_file.by_type('IfcTask') or []
            except Exception:
                plans, schedules, tasks = [], [], []
            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric("IfcWorkPlan", len(plans))
            with c2:
                st.metric("IfcWorkSchedule", len(schedules))
            with c3:
                st.metric("IfcTask", len(tasks))

            st.markdown("---")

            colA, colB, colC = st.columns(3)
            with colA:
                st.text("WorkPlans")
                df_wp = pd.DataFrame([{ 'Id': p.id(), 'Name': getattr(p,'Name',None)} for p in plans[:50]])
                if not df_wp.empty:
                    df_wp['Delete'] = False
                    edited_wp = st.data_editor(
                        df_wp,
                        use_container_width=True,
                        key="ed_wp_check",
                        column_config={"Delete": st.column_config.CheckboxColumn("Delete")},
                        hide_index=True,
                    )
                    if st.button("Delete selected", key="btn_del_sel_wp_check"):
                        ids = [int(r['Id']) for _, r in edited_wp.iterrows() if r.get('Delete')]
                        deleted = 0
                        for pid in ids:
                            if ifc4d.delete_work_plan(session.ifc_file, pid):
                                deleted += 1
                        if deleted:
                            st.success(f"Deleted {deleted} WorkPlan(s)")
                        else:
                            st.info("Nothing to delete")
                else:
                    st.info("No WorkPlans to show")
            with colB:
                st.text("WorkSchedules")
                df_ws = pd.DataFrame([{ 'Id': s.id(), 'Name': getattr(s,'Name',None)} for s in schedules[:50]])
                if not df_ws.empty:
                    df_ws['Delete'] = False
                    edited_ws = st.data_editor(
                        df_ws,
                        use_container_width=True,
                        key="ed_ws_check",
                        column_config={"Delete": st.column_config.CheckboxColumn("Delete")},
                        hide_index=True,
                    )
                    if st.button("Delete selected", key="btn_del_sel_ws_check"):
                        ids = [int(r['Id']) for _, r in edited_ws.iterrows() if r.get('Delete')]
                        deleted = 0
                        for sid in ids:
                            delete_work_schedule(sid)
                            deleted += 1
                        if deleted:
                            st.success(f"Deleted {deleted} WorkSchedule(s)")
                        else:
                            st.info("Nothing to delete")
                else:
                    st.info("No WorkSchedules to show")
            with colC:
                st.text("Tasks")
                df_t = pd.DataFrame([{ 'Id': t.id(), 'Name': getattr(t,'Name',None)} for t in tasks[:50]])
                if not df_t.empty:
                    df_t['Delete'] = False
                    edited_t = st.data_editor(
                        df_t,
                        use_container_width=True,
                        key="ed_task_check",
                        column_config={"Delete": st.column_config.CheckboxColumn("Delete")},
                        hide_index=True,
                    )
                    if st.button("Delete selected", key="btn_del_sel_task_check"):
                        ids = [int(r['Id']) for _, r in edited_t.iterrows() if r.get('Delete')]
                        deleted = 0
                        for tid in ids:
                            if ifc4d.delete_task(session.ifc_file, tid):
                                deleted += 1
                        if deleted:
                            st.success(f"Deleted {deleted} Task(s)")
                        else:
                            st.info("Nothing to delete")
                else:
                    st.info("No Tasks to show")
            st.button("💾 Save File", key="save_file_tab_check", on_click=save_file)


        # WorkPlan
        with tab_workplan:
            st.subheader("WorkPlan")
            plans = session.ifc_file.by_type('IfcWorkPlan') or []
            scheds = session.ifc_file.by_type('IfcWorkSchedule') or []

            options = ["Create new WorkPlan"] + [f"{w.id()} - {getattr(w,'Name',str(w))}" for w in plans]
            sel_wp_mgr = st.selectbox(
                "WorkPlan",
                options,
                key="wp_manager_sel",
                help="Select an existing WorkPlan to edit, or choose 'Create new WorkPlan' to create one.",
            )
            creating_new = (sel_wp_mgr == "Create new WorkPlan")

            # Resolve current attributes
            if creating_new:
                attrs = {
                    'Name': 'Work Plan',
                    'Identification': '',
                    'Purpose': '',
                    'PredefinedType': 'PLANNED',
                    'CreationDate': None,
                    'StartTime': None,
                    'FinishTime': None,
                }
                current_pid = None
            else:
                current_pid = int(sel_wp_mgr.split(' - ',1)[0])
                wp_obj = session.ifc_file.by_id(current_pid)
                attrs = ifc4d.get_work_plan_attrs(wp_obj)

            c1, c2 = st.columns(2)
            with c1:
                new_name = st.text_input("Name", value=(attrs.get('Name') or ''), key="wp_form_name", help="WorkPlan name.")
                new_ident = st.text_input("Identification", value=(attrs.get('Identification') or ''), key="wp_form_ident", help="Optional identifier/code for the WorkPlan.")
                new_purpose = st.text_input("Purpose", value=(attrs.get('Purpose') or ''), key="wp_form_purpose", help="Description or objective of the WorkPlan.")
                types = ["ACTUAL", "BASELINE", "PLANNED", "USERDEFINED", "NOTDEFINED"]
                try:
                    idx = types.index(attrs.get('PredefinedType') or 'PLANNED')
                except Exception:
                    idx = 2
                new_type = st.selectbox("PredefinedType", types, index=idx, key="wp_form_type", help="WorkPlan type: PLANNED, BASELINE, ACTUAL, or USERDEFINED.")
                new_object_type = st.text_input("ObjectType", value=(attrs.get('ObjectType') or ''), key="wp_form_objecttype", help="Required when PredefinedType is USERDEFINED.")
            with c2:
                def _parse_dt(s):
                    try:
                        return datetime.datetime.fromisoformat(s)
                    except Exception:
                        return None
                cd_dt = _parse_dt(attrs.get('CreationDate')) or datetime.datetime.combine(datetime.date.today(), datetime.time(9,0))
                st_dt = _parse_dt(attrs.get('StartTime')) or datetime.datetime.combine(datetime.date.today(), datetime.time(9,0))
                fn_dt = _parse_dt(attrs.get('FinishTime')) or datetime.datetime.combine(datetime.date.today(), datetime.time(17,0))
                cd = st.date_input("Creation date", value=cd_dt.date(), key="wp_form_creation_date", help="Date part of CreationDate.")
                ct = st.time_input("Creation time", value=cd_dt.time(), key="wp_form_creation_time", help="Time part of CreationDate.")
                sd = st.date_input("Start date", value=st_dt.date(), key="wp_form_start_date", help="Scheduled start date for the WorkPlan.")
                stime = st.time_input("Start time", value=st_dt.time(), key="wp_form_start_time", help="Scheduled start time for the WorkPlan.")
                fd = st.date_input("Finish date", value=fn_dt.date(), key="wp_form_finish_date", help="Scheduled finish date for the WorkPlan.")
                ftime = st.time_input("Finish time", value=fn_dt.time(), key="wp_form_finish_time", help="Scheduled finish time for the WorkPlan.")
                dur_iso = st.text_input("Duration (ISO 8601)", value=(attrs.get('Duration') or ''), key="wp_form_duration", help="Overall duration (e.g., P5D, P2W). Optional if FinishTime is set.")
                tf_iso = st.text_input("TotalFloat (ISO 8601)", value=(attrs.get('TotalFloat') or ''), key="wp_form_totalfloat", help="Total float/slack (e.g., P2D). Optional.")

            def to_iso(d,t):
                try:
                    return datetime.datetime.combine(d,t).isoformat()
                except Exception:
                    return None

            if st.button("Save WorkPlan", key="btn_save_wp_unified"):
                if creating_new:
                    created = ifc4d.create_work_plan(session.ifc_file, new_name or "Work Plan")
                    if created:
                        ok = ifc4d.update_work_plan(
                            session.ifc_file,
                            created.id(),
                            name=new_name or None,
                            identification=new_ident or None,
                            purpose=new_purpose or None,
                            predefined_type=new_type or None,
                            creation_datetime=to_iso(cd, ct),
                            start_time=to_iso(sd, stime),
                            finish_time=to_iso(fd, ftime),
                            object_type=new_object_type or None,
                            duration_iso=dur_iso or None,
                            total_float_iso=tf_iso or None,
                        )
                        linked = ifc4d.link_work_plan_to_project(session.ifc_file, created)
                        if ok:
                            st.success("WorkPlan created and saved")
                        else:
                            st.warning("WorkPlan created, but attributes were not fully saved")
                        if linked:
                            st.info("Linked WorkPlan to IfcProject")
                        else:
                            st.warning("Unable to link WorkPlan to IfcProject")
                    else:
                        st.error("Failed to create WorkPlan")
                else:
                    ok = ifc4d.update_work_plan(
                        session.ifc_file,
                        current_pid,
                        name=new_name or None,
                        identification=new_ident or None,
                        purpose=new_purpose or None,
                        predefined_type=new_type or None,
                        creation_datetime=to_iso(cd, ct),
                        start_time=to_iso(sd, stime),
                        finish_time=to_iso(fd, ftime),
                        object_type=new_object_type or None,
                        duration_iso=dur_iso or None,
                        total_float_iso=tf_iso or None,
                    )
                    if ok:
                        st.success("WorkPlan updated")
                    else:
                        st.error("Failed to update WorkPlan")

            if plans and scheds:
                st.markdown("---")
                st.subheader("Aggregate WorkSchedule into WorkPlan")
                psel2 = st.selectbox("WorkPlan", [f"{w.id()} - {getattr(w,'Name',str(w))}" for w in (session.ifc_file.by_type('IfcWorkPlan') or [])], key="sel_wp", help="Target WorkPlan that will aggregate the selected schedule.")
                ssel = st.selectbox("WorkSchedule", [f"{s.id()} - {getattr(s,'Name',str(s))}" for s in scheds], key="sel_ws_for_plan", help="WorkSchedule to be aggregated under the selected WorkPlan.")
                pid2 = int(psel2.split(' - ',1)[0]); sid2 = int(ssel.split(' - ',1)[0])
                if st.button("Aggregate schedule to plan", key="btn_aggr_ws_wp"):
                    ok = ifc4d.aggregate_schedule_to_workplan(session.ifc_file, pid2, sid2)
                    if ok:
                        st.success("Aggregated")
                    else:
                        st.error("Failed")
            st.button("💾 Save File", key="save_file_tab_wp", on_click=save_file)
        

        # Calendars tab
        with tab_calendars:
            st.subheader("Work Calendars")
            df_cal = ifc4d.build_calendars_df(session.ifc_file)
            st.dataframe(df_cal, use_container_width=True)
            st.markdown("---")
            st.subheader("Create calendar")
            cname = st.text_input("Name", key="wc_name", help="Name of the work calendar.")
            ctype = st.selectbox("PredefinedType", ["FIRSTSHIFT", "SECONDSHIFT", "THIRDSHIFT", "USERDEFINED", "NOTDEFINED"], index=4, key="wc_type", help="IfcWorkCalendarTypeEnum")
            cobj = st.text_input("ObjectType", key="wc_object_type", help="Required when PredefinedType is USERDEFINED.")
            cdesc = st.text_input("Description", key="wc_desc", help="Optional description")
            if st.button("Create WorkCalendar", key="btn_create_wc"):
                wc = ifc4d.create_work_calendar(session.ifc_file, cname or None, ctype, cdesc or None, (cobj or None))
                if wc:
                    st.success("WorkCalendar created")
                else:
                    st.error("Failed to create WorkCalendar (check ObjectType when USERDEFINED)")
            st.markdown("---")
            st.subheader("Base calendar (inheritance)")
            calendars = ifc4d.list_work_calendars(session.ifc_file)
            if calendars and len(calendars) > 1:
                child_sel = st.selectbox("Child calendar", [f"{c.id()} - {getattr(c,'Name',str(c))}" for c in calendars], key="wc_child", help="Calendar that will inherit from a base calendar.")
                base_sel = st.selectbox("Base calendar", [f"{c.id()} - {getattr(c,'Name',str(c))}" for c in calendars], key="wc_base", help="Base calendar providing default working times.")
                if st.button("Link base calendar", key="btn_link_base_cal"):
                    try:
                        child_id = int(child_sel.split(' - ',1)[0]); base_id = int(base_sel.split(' - ',1)[0])
                        if child_id == base_id:
                            st.warning("Child and base calendars must be different")
                        else:
                            ok = ifc4d.link_base_calendar(session.ifc_file, child_id, base_id)
                            if ok:
                                st.success("Linked")
                            else:
                                st.error("Failed to link")
                    except Exception:
                        st.error("Invalid selection")
            st.markdown("---")
            st.subheader("Add working/exception time")
            calendars = ifc4d.list_work_calendars(session.ifc_file)
            if calendars:
                selc = st.selectbox("Calendar", [f"{c.id()} - {getattr(c,'Name',str(c))}" for c in calendars], key="wc_sel", help="Calendar to which the time period will be added.")
                cal_id = int(selc.split(' - ',1)[0])
                tname = st.text_input("Time name", key="wt_name", help="Optional label for the working/exception time.")
                col1, col2 = st.columns(2)
                with col1:
                    sd = st.date_input("Start date", key="wt_start_date", help="Start date of the time period.")
                    stime = st.time_input("Start time", key="wt_start_time", help="Start time of the time period.")
                with col2:
                    fd = st.date_input("Finish date", key="wt_finish_date", help="Finish date of the time period.")
                    ftime = st.time_input("Finish time", key="wt_finish_time", help="Finish time of the time period.")
                is_exc = st.checkbox("Exception time", value=False, key="wt_is_exc", help="Mark as exception (non-working) time; otherwise it's a working time.")
                def to_iso(d,t):
                    try:
                        return datetime.datetime.combine(d,t).isoformat()
                    except Exception:
                        return None
                if st.button("Add time", key="btn_add_wt"):
                    ok = ifc4d.add_calendar_time(session.ifc_file, cal_id, tname or None, to_iso(sd, stime), to_iso(fd, ftime), is_exception=is_exc)
                    if ok:
                        st.success("Added")
                    else:
                        st.error("Failed")
            st.markdown("---")
            st.subheader("Assign calendar")
            if calendars:
                selc2 = st.selectbox("Calendar", [f"{c.id()} - {getattr(c,'Name',str(c))}" for c in calendars], key="wc_sel_assign", help="Calendar to assign to objects.")
                cal_id2 = int(selc2.split(' - ',1)[0])
                scope = st.radio("Assign to", ["WorkSchedules", "Tasks"], horizontal=True, key="wc_scope", help="Choose target object type for assignment.")
                if scope == "WorkSchedules":
                    items = session.ifc_file.by_type('IfcWorkSchedule') or []
                else:
                    items = session.ifc_file.by_type('IfcTask') or []
                opts = st.multiselect("Objects", [f"{o.id()} - {getattr(o,'Name',str(o))}" for o in items], key="wc_objs", help="Pick one or more target objects.")
                ids = [int(x.split(' - ',1)[0]) for x in opts]
                if st.button("Assign calendar to selected", key="btn_assign_cal"):
                    n = ifc4d.assign_calendar_to_objects(session.ifc_file, cal_id2, ids)
                    if n:
                        st.success(f"Assigned to {n} object(s)")
                    else:
                        st.info("Nothing assigned")
            st.markdown("---")
            st.subheader("Delete calendar")
            if calendars:
                seld = st.selectbox("Calendar to delete", [f"{c.id()} - {getattr(c,'Name',str(c))}" for c in calendars], key="wc_del", help="Select a calendar to delete (only the calendar object is removed).")
                del_id = int(seld.split(' - ',1)[0])
                if st.button("Delete WorkCalendar", key="btn_del_wc"):
                    ok = ifc4d.delete_work_calendar(session.ifc_file, del_id)
                    if ok:
                        st.success("Calendar deleted")
                    else:
                        st.error("Failed to delete")
            st.button("💾 Save File", key="save_file_tab_wc", on_click=save_file)


        # Schedules management
        with tab_schedules:
            st.subheader("Assign tasks to WorkSchedules")
            scheds = session.ifc_file.by_type('IfcWorkSchedule') or []
            if not scheds:
                st.info("No WorkSchedules found. Create one in previous tab.")
            else:
                sched_options = [f"{s.id()} - {getattr(s,'Name',str(s))}" for s in scheds]
                sel = st.selectbox("WorkSchedule", sched_options, index=0, key="sch_sel", help="WorkSchedule that will receive the selected tasks.")
                sel_id = int(sel.split(' - ',1)[0]) if sel else None
                unassigned = ifc4d.get_unassigned_tasks(session.ifc_file)
                if not unassigned:
                    st.info("No unassigned tasks.")
                else:
                    task_options = [f"{t.id()} - {getattr(t,'Name',str(t))}" for t in unassigned]
                    chosen = st.multiselect("Tasks to assign", task_options, key="tasks_to_assign", help="Select one or more unassigned tasks to add to the WorkSchedule.")
                    chosen_ids = [int(x.split(' - ',1)[0]) for x in chosen]
                    if st.button("Assign selected to schedule", key="btn_assign_tasks_to_ws"):
                        assigned = ifc4d.assign_tasks_to_schedule(session.ifc_file, sel_id, chosen_ids)
                        if assigned:
                            st.success(f"Assigned {assigned} tasks to schedule")
            st.button("💾 Save File", key="save_file_tab_sched", on_click=save_file)


        # Tasks -> Elements
        with tab_elements_tasks:
            st.subheader("Select elements and create tasks")
            df_unscheduled = ifc4d.build_unscheduled_df(session.ifc_file)
            if df_unscheduled is None or df_unscheduled.empty:
                st.info("No elements found or all already scheduled.")
            else:
                levels = ["All"] + sorted([v for v in df_unscheduled['Level'].dropna().unique()])
                classes = ["All"] + sorted([v for v in df_unscheduled['Class'].dropna().unique()])
                types = ["All"] + sorted([v for v in df_unscheduled['Type'].dropna().unique()])
                col1, col2, col3 = st.columns(3)
                sel_level = col1.selectbox("Level", levels, index=0, key="el_level", help="Filter elements by level.")
                sel_class = col2.selectbox("Class", classes, index=0, key="el_class", help="Filter elements by IFC class.")
                sel_type = col3.selectbox("Type", types, index=0, key="el_type", help="Filter elements by IFC type.")
                filtered = df_unscheduled.copy()
                if sel_level != "All":
                    filtered = filtered[filtered['Level'] == sel_level]
                if sel_class != "All":
                    filtered = filtered[filtered['Class'] == sel_class]
                if sel_type != "All":
                    filtered = filtered[filtered['Type'] == sel_type]
                st.caption(f"Filtered elements: {len(filtered)}")
                st.dataframe(filtered, use_container_width=True)
                if st.button("Use filtered as selection", key="btn_select_filtered"):
                    try:
                        session["selected_element_ids"] = [int(x) for x in filtered['ExpressId'].dropna().tolist()]
                        st.success(f"Selected {len(session['selected_element_ids'])} elements")
                    except Exception:
                        session["selected_element_ids"] = []
                st.markdown("---")
                st.caption("Create tasks for selected elements")
                mode = st.radio(
                    "Mode",
                    ["One task per element", "Single task for all selected"],
                    horizontal=True,
                    key="el_mode",
                    help="Choose one task per element or a single task covering all selected elements.",
                )
                name_prefix = st.text_input(
                    "Task name / prefix",
                    value="Task",
                    key="el_name_prefix",
                    help="Base name for created tasks. With 'One task per element', the element id will be appended (e.g., Task_123).",
                )
                ident_prefix = st.text_input(
                    "Identification prefix",
                    value="",
                    key="el_ident_prefix",
                    help="Optional code prefix. With 'One task per element', the element id will be appended.",
                )
                colA, colB = st.columns(2)
                with colA:
                    sd = st.date_input("Start date", key="el_start_date", help="Planned start date for the task(s).")
                    stime = st.time_input("Start time", key="el_start_time", help="Planned start time for the task(s).")
                with colB:
                    fd = st.date_input("Finish date", key="el_finish_date", help="Planned finish date. Leave empty and use Duration if not known.")
                    ftime = st.time_input("Finish time", key="el_finish_time", help="Planned finish time for the task(s).")
                duration_iso = st.text_input(
                    "Duration (ISO 8601)",
                    value="P1W",
                    key="el_dur",
                    help="Optional duration in ISO 8601 (e.g., P5D, P1W). Used if finish is not provided.",
                )
                if st.button("Create tasks", key="el_create_tasks"):
                    created = ifc4d.create_tasks(session.ifc_file, session.get("selected_element_ids", []), name_prefix, (ident_prefix or None), sd, stime, fd, ftime, (duration_iso or None), ("per_element" if mode=="One task per element" else "single"))
                    st.success(f"Created {created} task(s)")
                st.button("💾 Save File", key="save_file_tab_elements", on_click=save_file)


        # Nesting & Gantt
        with tab_nesting:
            st.subheader("Nesting overview")
            df_nesting = ifc4d.build_nesting_df(session.ifc_file)
            st.dataframe(df_nesting, use_container_width=True)
            st.markdown("---")
            st.subheader("Delete entities")
            colx, coly, colz = st.columns(3)
            with colx:
                tasks = session.ifc_file.by_type('IfcTask') or []
                tsel = st.selectbox("Task to delete", ["Select"] + [f"{t.id()} - {getattr(t,'Name',str(t))}" for t in tasks], key="del_task_sel", help="Choose a task to delete from the model.")
                if tsel != "Select" and st.button("Delete task", key="btn_del_task"):
                    tid = int(tsel.split(' - ',1)[0])
                    if ifc4d.delete_task(session.ifc_file, tid): st.success("Task deleted")
            with coly:
                scheds = session.ifc_file.by_type('IfcWorkSchedule') or []
                ssel = st.selectbox("Schedule to delete", ["Select"] + [f"{s.id()} - {getattr(s,'Name',str(s))}" for s in scheds], key="del_sched_sel", help="Choose a WorkSchedule to delete from the model.")
                if ssel != "Select" and st.button("Delete schedule", key="btn_del_sched"):
                    sid = int(ssel.split(' - ',1)[0])
                    delete_work_schedule(sid)
            with colz:
                plans = session.ifc_file.by_type('IfcWorkPlan') or []
                psel = st.selectbox("WorkPlan to delete", ["Select"] + [f"{p.id()} - {getattr(p,'Name',str(p))}" for p in plans], key="del_plan_sel", help="Choose a WorkPlan to delete from the model.")
                if psel != "Select" and st.button("Delete plan", key="btn_del_plan"):
                    pid = int(psel.split(' - ',1)[0])
                    if ifc4d.delete_work_plan(session.ifc_file, pid): st.success("WorkPlan deleted")
            st.markdown("---")
            st.subheader("Gantt")
            scheds = session.ifc_file.by_type('IfcWorkSchedule') or []
            options = ["All schedules"] + [f"{s.id()} - {getattr(s,'Name',str(s))}" for s in scheds]
            sel = st.selectbox("Scope", options, key="gantt_scope", help="Select a specific WorkSchedule to plot, or 'All schedules'.")
            sch_id = None if sel == "All schedules" else int(sel.split(' - ',1)[0])
            df_tasks = ifc4d.build_all_tasks_df(session.ifc_file, sch_id)
            if df_tasks is None or df_tasks.empty:
                st.info("No tasks with dates to plot.")
            else:
                plot_df = df_tasks.dropna(subset=["Start", "Finish"]).copy()
                if not plot_df.empty:
                    fig = px.timeline(plot_df, x_start="Start", x_end="Finish", y="Task", color=("WorkSchedule" if 'WorkSchedule' in plot_df.columns else None))
                    fig.update_yaxes(autorange="reversed")
                    st.plotly_chart(fig, use_container_width=True)
            st.button("💾 Save File", key="save_file_tab_nesting", on_click=save_file)
    else:
        # Istruzione iniziale quando nessun file è caricato (output in inglese)
        st.header("Step 1: Load a file from the Home Page")


# Esegue la pagina
execute()