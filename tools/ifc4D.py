import ifcopenshell as ifc
import ifcopenshell
import ifcopenshell.api.sequence
from ifcopenshell.guid import new as new_guid
from ifcopenshell.util import element as ifc_element
import pandas as pd
import datetime

# Helpers di formattazione

def _to_datetime(val):
    try:
        if isinstance(val, datetime.datetime):
            return val
        if isinstance(val, datetime.date):
            return datetime.datetime.combine(val, datetime.time())
        if isinstance(val, str):
            return datetime.datetime.fromisoformat(val)
    except Exception:
        return None
    return None


def _iso_dur_to_days(dur: str) -> int:
    if not dur or not isinstance(dur, str):
        return 0
    dur = dur.upper()
    try:
        if dur.startswith('P') and 'W' in dur:
            n = int(dur.strip('P').split('W')[0])
            return n * 7
        if dur.startswith('P') and 'D' in dur:
            n = int(dur.strip('P').split('D')[0])
            return n
    except Exception:
        pass
    return 0

# Wrappers IFC

def declare_under_project(model, obj):
    try:
        project = (model.by_type("IfcProject") or [None])[0]
        if project and obj:
            model.create_entity("IfcRelDeclares", GlobalId=new_guid(), RelatingContext=project, RelatedDefinitions=[obj])
    except Exception:
        pass


def assign_control(model, control, related_objects):
    try:
        ifcopenshell.api.run("control.assign_control", model, relating_control=control, related_objects=related_objects)
    except Exception:
        try:
            model.create_entity("IfcRelAssignsToControl", GlobalId=new_guid(), RelatingControl=control, RelatedObjects=list(related_objects))
        except Exception:
            pass


def nest_under(model, parent_task, child_task):
    try:
        ifcopenshell.api.run("nest.assign_object", model, relating_object=parent_task, related_object=child_task)
    except Exception:
        try:
            model.create_entity("IfcRelNests", GlobalId=new_guid(), RelatingObject=parent_task, RelatedObjects=[child_task])
        except Exception:
            pass


def add_task(model, name, predecessor, work_schedule):
    task = ifcopenshell.api.sequence.add_task(
        model, work_schedule=work_schedule, name=name, predefined_type="CONSTRUCTION"
    )
    task_time = ifcopenshell.api.sequence.add_task_time(model, task=task)
    ifcopenshell.api.sequence.edit_task_time(
        model, task_time=task_time, attributes={"ScheduleStart": datetime.date(2000, 1, 1), "ScheduleDuration": "P1W"}
    )
    if predecessor:
        ifcopenshell.api.sequence.assign_sequence(model, relating_process=predecessor, related_process=task)
    return task


def _collect_nested_tasks(task, acc:list):
    acc.append(task)
    try:
        for rel in getattr(task, 'IsNestedBy', []) or []:
            for obj in getattr(rel, 'RelatedObjects', []) or []:
                if obj.is_a('IfcTask'):
                    _collect_nested_tasks(obj, acc)
    except Exception:
        pass


def get_schedule_tasks(schedule) -> list:
    tasks = []
    try:
        for rel in getattr(schedule, 'Controls', []) or []:
            if rel.is_a('IfcRelAssignsToControl'):
                for obj in getattr(rel, 'RelatedObjects', []) or []:
                    if obj.is_a('IfcTask'):
                        _collect_nested_tasks(obj, tasks)
    except Exception:
        pass
    seen = set(); out = []
    for t in tasks:
        tid = getattr(t, 'id', None)
        tid = tid() if callable(tid) else id(t)
        if tid not in seen:
            seen.add(tid); out.append(t)
    return out


def get_all_schedule_task_ids(ifc_file):
    task_ids = set()
    for ws in ifc_file.by_type('IfcWorkSchedule') or []:
        for t in get_schedule_tasks(ws):
            try:
                task_ids.add(t.id())
            except Exception:
                pass
    return task_ids


def get_scheduled_element_ids(ifc_file):
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


def build_tasks_df(schedule) -> pd.DataFrame:
    rows = []
    for t in get_schedule_tasks(schedule):
        name = getattr(t, 'Name', None)
        ident = getattr(t, 'Identification', None)
        tt = getattr(t, 'TaskTime', None)
        s = _to_datetime(getattr(tt, 'ScheduleStart', None)) if tt else None
        f = _to_datetime(getattr(tt, 'ScheduleFinish', None)) if tt else None
        dur = getattr(tt, 'ScheduleDuration', None) if tt else None
        if not f and s and dur:
            try:
                f = s + datetime.timedelta(days=_iso_dur_to_days(dur))
            except Exception:
                pass
        rows.append({
            'Task': name,
            'Identification': ident,
            'Start Date': s.date() if isinstance(s, datetime.datetime) else None,
            'End Date': f.date() if isinstance(f, datetime.datetime) else None,
            'Duration': dur or '',
            'Start': s,
            'Finish': f,
        })
    df = pd.DataFrame(rows)
    try:
        df = df.sort_values(by=['Start', 'Finish'], na_position='last')
    except Exception:
        pass
    return df


def create_work_schedule(model, name=None, identification=None, predefined_type='PLANNED', start_time=None, finish_time=None, purpose=None):
    ws = None
    try:
        ws = ifc.api.run(
            'sequence.add_work_schedule',
            model,
            name=name,
            identification=identification,
            predefined_type=predefined_type,
            start_time=start_time,
            finish_time=finish_time,
            purpose=purpose,
        )
        return ws
    except Exception:
        pass
    try:
        ws = model.create_entity(
            'IfcWorkSchedule',
            Name=name,
            Identification=identification,
            PredefinedType=predefined_type,
            Purpose=purpose,
            StartTime=start_time,
            FinishTime=finish_time,
        )
    except Exception:
        ws = None
    return ws


def map_task_to_schedule(ifc_file):
    mapping = {}
    try:
        for ws in ifc_file.by_type('IfcWorkSchedule') or []:
            for rel in getattr(ws, 'Controls', []) or []:
                if rel.is_a('IfcRelAssignsToControl'):
                    for obj in getattr(rel, 'RelatedObjects', []) or []:
                        if obj.is_a('IfcTask'):
                            try:
                                mapping[obj.id()] = ws
                            except Exception:
                                pass
    except Exception:
        pass
    return mapping


def get_unassigned_tasks(ifc_file):
    mapping = map_task_to_schedule(ifc_file)
    try:
        tasks = ifc_file.by_type('IfcTask') or []
    except Exception:
        tasks = []
    out = []
    for t in tasks:
        try:
            if t.id() not in mapping:
                out.append(t)
        except Exception:
            continue
    return out


def assign_tasks_to_schedule(model, schedule_id: int, task_ids: list[int]) -> int:
    ws = model.by_id(int(schedule_id)) if schedule_id else None
    if not ws:
        return 0
    assigned = 0
    for tid in task_ids or []:
        t = model.by_id(int(tid))
        if not t:
            continue
        try:
            ifc.api.run('control.assign_control', model, relating_control=ws, related_objects=[t])
        except Exception:
            try:
                model.create_entity('IfcRelAssignsToControl', GlobalId=new_guid(), RelatingControl=ws, RelatedObjects=[t])
            except Exception:
                continue
        assigned += 1
    return assigned


def create_work_plan(model, name=None):
    wp = None
    try:
        wp = ifc.api.run('sequence.add_work_plan', model, name=name)
    except Exception:
        try:
            wp = model.create_entity('IfcWorkPlan', Name=(name or 'WorkPlan'))
        except Exception:
            wp = None
    try:
        project = (model.by_type('IfcProject') or [None])[0]
        if project and wp:
            model.create_entity('IfcRelDeclares', GlobalId=new_guid(), RelatingContext=project, RelatedDefinitions=[wp])
    except Exception:
        pass
    return wp


def aggregate_schedule_to_workplan(model, workplan_id, schedule_id) -> bool:
    wp = model.by_id(int(workplan_id)) if workplan_id else None
    sched = model.by_id(int(schedule_id)) if schedule_id else None
    if not wp or not sched:
        return False
    try:
        ifc.api.run('aggregate.assign_object', model, product=sched, relating_object=wp)
        return True
    except Exception:
        pass
    try:
        model.create_entity('IfcRelAggregates', GlobalId=new_guid(), RelatingObject=wp, RelatedObjects=[sched])
        return True
    except Exception:
        return False


def delete_task(model, task_id: int) -> bool:
    t = model.by_id(int(task_id)) if task_id else None
    if not t:
        return False
    try:
        ifc.api.run('sequence.remove_task', model, task=t)
        return True
    except Exception:
        try:
            model.remove(t)
            return True
        except Exception:
            return False


def delete_work_plan(model, plan_id: int) -> bool:
    wp = model.by_id(int(plan_id)) if plan_id else None
    if not wp:
        return False
    try:
        model.remove(wp)
        return True
    except Exception:
        return False


def get_aggregated_schedules(wp):
    out = []
    try:
        for rel in getattr(wp, 'IsDecomposedBy', []) or []:
            if rel.is_a('IfcRelAggregates'):
                for obj in getattr(rel, 'RelatedObjects', []) or []:
                    if obj.is_a('IfcWorkSchedule'):
                        out.append(obj)
    except Exception:
        pass
    return out


def build_nesting_df(ifc_file) -> pd.DataFrame:
    rows = []
    schedule_map = map_task_to_schedule(ifc_file)
    try:
        tasks = ifc_file.by_type('IfcTask') or []
    except Exception:
        tasks = []
    for t in tasks:
        parent = None
        try:
            for rel in getattr(t, 'Decomposes', []) or []:
                if rel.is_a('IfcRelNests'):
                    parent = getattr(rel, 'RelatingObject', None)
                    break
        except Exception:
            parent = None
        s = schedule_map.get(t.id())
        tt = getattr(t, 'TaskTime', None)
        sdt = _to_datetime(getattr(tt, 'ScheduleStart', None)) if tt else None
        fdt = _to_datetime(getattr(tt, 'ScheduleFinish', None)) if tt else None
        rows.append({
            'TaskId': t.id() if hasattr(t, 'id') else None,
            'TaskName': getattr(t, 'Name', None),
            'ParentId': (parent.id() if parent is not None and hasattr(parent, 'id') else None),
            'ParentName': (getattr(parent, 'Name', None) if parent is not None else None),
            'ScheduleId': (s.id() if s is not None and hasattr(s, 'id') else None),
            'ScheduleName': (getattr(s, 'Name', None) if s is not None else None),
            'Start': sdt,
            'Finish': fdt,
        })
    return pd.DataFrame(rows)


def build_all_tasks_df(ifc_file, schedule_id: int | None = None) -> pd.DataFrame:
    if schedule_id:
        ws = ifc_file.by_id(int(schedule_id))
        if not ws:
            return pd.DataFrame()
        return build_tasks_df(ws)
    rows = []
    for ws in ifc_file.by_type('IfcWorkSchedule') or []:
        df = build_tasks_df(ws)
        if not df.empty:
            df = df.copy(); df['WorkSchedule'] = getattr(ws, 'Name', None)
            rows.append(df)
    if rows:
        out = pd.concat(rows, ignore_index=True)
        try:
            out = out.sort_values(by=['Start', 'Finish'], na_position='last')
        except Exception:
            pass
        return out
    return pd.DataFrame()


def create_tasks(model, element_ids: list[int], name_prefix: str = "Task", identification_prefix: str | None = None,
                 start_date=None, start_time=None, finish_date=None, finish_time=None, duration_iso: str | None = None,
                 mode: str = "per_element") -> int:
    if not element_ids:
        return 0
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
    if mode == "single":
        tname = name_prefix.strip() or "Task"
        ident = (identification_prefix or None)
        try:
            task = model.create_entity('IfcTask', Name=tname, Identification=ident)
        except Exception:
            task = None
        if task:
            if s_iso or f_iso or duration_iso:
                try:
                    tt = model.create_entity('IfcTaskTime', ScheduleStart=s_iso, ScheduleFinish=f_iso, ScheduleDuration=duration_iso)
                    try:
                        task.TaskTime = tt
                    except Exception:
                        pass
                except Exception:
                    pass
            objs = [model.by_id(int(e)) for e in element_ids if model.by_id(int(e)) is not None]
            if objs:
                try:
                    ifc.api.run('sequence.assign_process', model, relating_process=task, related_objects=objs)
                except Exception:
                    try:
                        model.create_entity('IfcRelAssignsToProcess', GlobalId=new_guid(), RelatingProcess=task, RelatedObjects=objs)
                    except Exception:
                        pass
            created = 1
    else:
        for eid in element_ids:
            el = model.by_id(int(eid))
            if not el:
                continue
            tname = f"{name_prefix}_{eid}" if name_prefix else f"Task_{eid}"
            ident = (f"{identification_prefix}{eid}" if identification_prefix else None)
            try:
                task = model.create_entity('IfcTask', Name=tname, Identification=ident)
            except Exception:
                task = None
            if not task:
                continue
            if s_iso or f_iso or duration_iso:
                try:
                    tt = model.create_entity('IfcTaskTime', ScheduleStart=s_iso, ScheduleFinish=f_iso, ScheduleDuration=duration_iso)
                    try:
                        task.TaskTime = tt
                    except Exception:
                        pass
                except Exception:
                    pass
            try:
                ifc.api.run('sequence.assign_process', model, relating_process=task, related_objects=[el])
            except Exception:
                try:
                    model.create_entity('IfcRelAssignsToProcess', GlobalId=new_guid(), RelatingProcess=task, RelatedObjects=[el])
                except Exception:
                    pass
            created += 1
    return created


def create_tasks_for_elements_in_schedule(model, schedule_id: int, element_ids: list[int], task_name_prefix: str = 'Task') -> int:
    """Crea una task per ogni elemento e la inserisce nella WorkSchedule, collegando elemento (RelAssignsToProcess) e schedule (RelAssignsToControl)."""
    sched = model.by_id(int(schedule_id)) if schedule_id else None
    if not sched or not element_ids:
        return 0
    created = 0
    for eid in element_ids:
        el = model.by_id(int(eid))
        if not el:
            continue
        task = None
        try:
            task = ifc.api.run('sequence.add_task', model, work_schedule=sched, name=f"{task_name_prefix}_{eid}")
        except Exception:
            try:
                task = model.create_entity('IfcTask', Name=f"{task_name_prefix}_{eid}")
            except Exception:
                task = None
        if not task:
            continue
        try:
            ifc.api.run('sequence.assign_process', model, relating_process=task, related_objects=[el])
        except Exception:
            try:
                model.create_entity('IfcRelAssignsToProcess', GlobalId=new_guid(), RelatingProcess=task, RelatedObjects=[el])
            except Exception:
                pass
        try:
            ifc.api.run('control.assign_control', model, relating_control=sched, related_objects=[task])
        except Exception:
            try:
                model.create_entity('IfcRelAssignsToControl', GlobalId=new_guid(), RelatingControl=sched, RelatedObjects=[task])
            except Exception:
                pass
        created += 1
    return created


def list_work_calendars(model):
    try:
        return model.by_type('IfcWorkCalendar') or []
    except Exception:
        return []


def create_work_calendar(model, name: str | None = None, predefined_type: str = 'NOTDEFINED', description: str | None = None):
    wc = None
    try:
        wc = model.create_entity('IfcWorkCalendar', Name=name, PredefinedType=predefined_type, Description=description)
    except Exception:
        wc = None
    return wc


def delete_work_calendar(model, calendar_id: int) -> bool:
    cal = model.by_id(int(calendar_id)) if calendar_id else None
    if not cal:
        return False
    try:
        model.remove(cal)
        return True
    except Exception:
        return False


def add_calendar_time(model, calendar_id: int, name: str | None = None, start_iso: str | None = None, finish_iso: str | None = None, is_exception: bool = False) -> bool:
    cal = model.by_id(int(calendar_id)) if calendar_id else None
    if not cal:
        return False
    try:
        wt = model.create_entity('IfcWorkTime', Name=name, Start=start_iso, Finish=finish_iso)
    except Exception:
        return False
    try:
        if is_exception:
            lst = list(getattr(cal, 'ExceptionTimes', []) or [])
            lst.append(wt)
            cal.ExceptionTimes = lst
        else:
            lst = list(getattr(cal, 'WorkingTimes', []) or [])
            lst.append(wt)
            cal.WorkingTimes = lst
        return True
    except Exception:
        return False


def assign_calendar_to_objects(model, calendar_id: int, object_ids: list[int]) -> int:
    cal = model.by_id(int(calendar_id)) if calendar_id else None
    if not cal:
        return 0
    count = 0
    for oid in object_ids or []:
        obj = model.by_id(int(oid))
        if not obj:
            continue
        try:
            ifc.api.run('control.assign_control', model, relating_control=cal, related_objects=[obj])
            count += 1
        except Exception:
            try:
                model.create_entity('IfcRelAssignsToControl', GlobalId=new_guid(), RelatingControl=cal, RelatedObjects=[obj])
                count += 1
            except Exception:
                continue
    return count


def build_calendars_df(model) -> pd.DataFrame:
    rows = []
    for cal in list_work_calendars(model):
        wt = getattr(cal, 'WorkingTimes', []) or []
        et = getattr(cal, 'ExceptionTimes', []) or []
        rows.append({
            'Id': (cal.id() if hasattr(cal, 'id') else None),
            'Name': getattr(cal, 'Name', None),
            'PredefinedType': getattr(cal, 'PredefinedType', None),
            'WorkingTimes': len(list(wt)),
            'ExceptionTimes': len(list(et)),
        })
    return pd.DataFrame(rows)
