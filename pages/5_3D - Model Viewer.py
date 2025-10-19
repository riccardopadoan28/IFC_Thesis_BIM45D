# ─────────────────────────────────────────────
# 📦 Importazioni
# ─────────────────────────────────────────────
import streamlit as st
import json
import ifcopenshell
import streamlit.components.v1 as components
from pathlib import Path
from typing import Optional
from tools import ifchelper


# ─────────────────────────────────────────────
# 🧠 Alias per lo stato della sessione Streamlit
# ─────────────────────────────────────────────
session = st.session_state

# -----------------------------
# ORGANIZZAZIONE DELLA PAGINA
# -----------------------------
# Elenco funzioni/aree (in italiano):
# - ifc_js_viewer: USATA: viewer component; SCOPO: wrapper per componente custom
# - draw_3d_viewer: USATA: tab principale; SCOPO: salva file temporaneo e carica viewer
# - get_psets_from_ifc_js / format_ifc_js_psets: USATA: Properties tab; SCOPO: mostra property sets
# - Debug helpers (initialise_debug_props, get_object_data, edit_object_data): USATA: Debug tab
# - execute: USATA: entry point


# ─────────────────────────────────────────────
# 📦 Dichiarazione componente custom IFC.js Viewer
# ─────────────────────────────────────────────
# Percorso assoluto alla build del frontend (React/JS)
frontend_dir = (Path(__file__).parent.parent / "frontend-viewer" / "build").absolute()
_component_func = components.declare_component(
    "ifc_js_viewer", path=str(frontend_dir)
)

def ifc_js_viewer(url: Optional[str] = None):
    """
    Wrapper per visualizzare l'IFC nel viewer custom.
    - url: percorso accessibile dal browser (es. 'http://localhost:8502/temp_model.ifc')
    """
    component_value = _component_func(url=url)
    return component_value

# ─────────────────────────────────────────────
# 📡 Funzione per mostrare il 3D viewer
# ─────────────────────────────────────────────
def draw_3d_viewer():
    # Salva il file IFC nella cartella build
    if "ifc_file" in session and session["ifc_file"]:
        output_dir = Path(__file__).parent.parent / "frontend-viewer" / "build"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / "temp_model.ifc"
        # Salva sempre il file IFC (sovrascrive)
        with open(output_path, "wb") as f:
            f.write(session["ifc_file"].to_string().encode("utf-8"))
        # Passa l'URL del server statico al componente custom
        url = "http://localhost:8502/temp_model.ifc"
        session.ifc_js_response = ifc_js_viewer(url)
        st.sidebar.success("Visualiser loaded")
        st.sidebar.info("Avvia il server statico: python -m http.server 8502 nella cartella frontend-viewer/build")
    else:
        st.sidebar.warning("No IFC file loaded.")

# ─────────────────────────────────────────────
# 📦 Recupera i property set dal viewer IFC.js
# ─────────────────────────────────────────────
def get_psets_from_ifc_js():
    if session.ifc_js_response:
        return json.loads(session.ifc_js_response)

# ─────────────────────────────────────────────
# 🧽 Formatta i property set per la visualizzazione
# ─────────────────────────────────────────────
def format_ifc_js_psets(data):
    return ifchelper.format_ifcjs_psets(data)

# ─────────────────────────────────────────────
# 🧠 Inizializza proprietà di debug IFC
# ─────────────────────────────────────────────
def initialise_debug_props(force=False):
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

# ─────────────────────────────────────────────
# 🔎 Estrae dati oggetto IFC per debug
# ─────────────────────────────────────────────
def get_object_data(fromId=None):
    def add_attribute(prop, key, value):
        if isinstance(value, tuple) and len(value) < 10:
            for i, item in enumerate(value):
                add_attribute(prop, key + f"[{i}]", item)
            return
        elif isinstance(value, tuple) and len(value) >= 10:
            key = key + "({})".format(len(value))
        propy = {
            "name": key,
            "string_value": str(value),
            "int_value": int(value.id()) if isinstance(value, ifcopenshell.entity_instance) else None,
        }
        prop.append(propy)
    if session.BIMDebugProperties:
        initialise_debug_props(force=True)
        step_id = int(fromId) if fromId else int(session.object_id) if session.object_id else 0
        debug_props = st.session_state.BIMDebugProperties
        debug_props["active_step_id"] = step_id
        crumb = {"name": str(step_id)}
        debug_props["step_id_breadcrumb"].append(crumb)
        element = session.ifc_file.by_id(step_id)
        debug_props["inverse_attributes"] = []
        debug_props["inverse_references"] = []
        if element:
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

# ─────────────────────────────────────────────
# ✏️ Modifica dati oggetto IFC (debug)
# ─────────────────────────────────────────────
def edit_object_data(object_id, attribute):
    entity = session.ifc_file.by_id(object_id)
    print(getattr(entity, attribute))

# ─────────────────────────────────────────────
# 📋 Mostra i dati dei Property Sets
# ─────────────────────────────────────────────
def write_pset_data():
    data = get_psets_from_ifc_js()
    if data:
        st.subheader("🧮 Object Properties")
        psets = format_ifc_js_psets(data['props'])
        for pset in psets.values():
            st.subheader(pset["Name"])
            st.table(pset["Data"])

# ─────────────────────────────────────────────
# 🩺 Debugger IFC: mostra attributi e riferimenti
# ─────────────────────────────────────────────
def write_health_data():
    st.subheader("🩺 Debugger")
    row1_col1, row1_col2 = st.columns([1,5])
    with row1_col1:
        st.number_input("Object ID", key="object_id")
    with row1_col2:
        st.button("Inspect From Id", key="edit_object_button", on_click=get_object_data, args=(st.session_state.object_id,))
        data = get_psets_from_ifc_js()
        if data:
            st.button("Inspect from Model", key="get_object_button", on_click=get_object_data, args=(data['id'],)) if data else ""
    if "BIMDebugProperties" in session and session.BIMDebugProperties:
        props = session.BIMDebugProperties
        if props["attributes"]:
            st.subheader("Attributes")
            for prop in props["attributes"]:
                col2, col3 = st.columns([3,3])
                if prop["int_value"]:
                    col2.text(f'🔗 {prop["name"]}')
                    col2.info(prop["string_value"])
                    col3.write("🔗")
                    col3.button("Get Object", key=f'get_object_pop_button_{prop["int_value"]}', on_click=get_object_data, args=(prop["int_value"],))
                else:
                    col2.text_input(label=prop["name"], key=prop["name"], value=prop["string_value"])
        if props["inverse_attributes"]:
            st.subheader("Inverse Attributes")
            for inverse in props["inverse_attributes"]:
                col1, col2, col3 = st.columns([3,5,8])
                col1.text(inverse["name"])
                col2.text(inverse["string_value"])
                if inverse["int_value"]:
                    col3.button("Get Object", key=f'get_object_pop_button_{inverse["int_value"]}', on_click=get_object_data, args=(inverse["int_value"],))
        if props["inverse_references"]:
            st.subheader("Inverse References")
            for inverse in props["inverse_references"]:
                col1, col3 = st.columns([3,3])
                col1.text(inverse["string_value"])
                if inverse["int_value"]:
                    col3.button("Get Object", key=f'get_object_pop_button_inverse_{inverse["int_value"]}', on_click=get_object_data, args=(inverse["int_value"],))

# ─────────────────────────────────────────────
# ▶️ Funzione principale di esecuzione pagina
# ─────────────────────────────────────────────
def execute():
    initialise_debug_props()
    st.set_page_config(page_title="3D", layout="wide")
    st.header("🎮 IFC.js Model Viewer")
    st.markdown(
        "This viewer can inspect the model and its properties."
    )


    if "ifc_file" in session and session["ifc_file"]:
        if "ifc_js_response" not in session:
            session["ifc_js_response"] = ""
        draw_3d_viewer()
        tab1, tab2 = st.tabs(["🧮 Properties", "🩺 Debugger"])
        with tab1:
            write_pset_data()
        with tab2:
            write_health_data()
    else:
        st.header("Step 1: Load a file from the Home Page")
session = st.session_state
execute()

# Per servire il file IFC, avvia un server statico nella cartella public:
# python -m http.server 8502
# Poi carica il modello con l'url: http://localhost:8502/temp_model.ifc