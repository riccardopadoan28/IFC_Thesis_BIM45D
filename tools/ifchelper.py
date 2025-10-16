import ifcopenshell
import ifcopenshell.util.element as Element
import ifcopenshell.api
from datetime import datetime
import pandas as pd
from . import ifchelper as helper
import streamlit as st

session = st.session_state


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
