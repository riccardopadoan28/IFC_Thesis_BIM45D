# ─────────────────────────────────────────────
# 📦 Importazioni
# ─────────────────────────────────────────────
import streamlit as st
from tools import ifchelper
import json
import ifcopenshell as ifc
from tools.ifc_component import ifc_js_viewer  # usa il nuovo wrapper


# ─────────────────────────────────────────────
# 🧠 Stato della sessione Streamlit
# ─────────────────────────────────────────────
session = st.session_state


# ─────────────────────────────────────────────
# 📡 Funzione per mostrare il 3D viewer
# ─────────────────────────────────────────────
def draw_3d_viewer():
    if "public_ifc_path" not in session:
        st.error("❌ IFC file not found. Please upload a model first.")
        return

    file_url = session["public_ifc_path"]
    st.write("📎 IFC File URL:", file_url)
    session.ifc_js_response = ifc_js_viewer(url=file_url, key="ifc_viewer")
    st.sidebar.success("3D Viewer loaded successfully!")


# ─────────────────────────────────────────────
# 📦 Recupera i property set dal viewer IFC.js
# ─────────────────────────────────────────────
def get_psets_from_ifc_js():
    if session.ifc_js_response:
        try:
            return json.loads(session.ifc_js_response)
        except Exception as e:
            st.error(f"❌ Error parsing ifc_js_response: {e}")
            return None


# ─────────────────────────────────────────────
# 🧽 Formatta i property set per la visualizzazione
# ─────────────────────────────────────────────
def format_ifc_js_psets(data):
    return ifchelper.format_ifcjs_psets(data)


# ─────────────────────────────────────────────
# 📋 Mostra i dati dei Property Sets
# ─────────────────────────────────────────────
def write_pset_data():
    data = get_psets_from_ifc_js()
    if not data:
        st.info("No properties from IFC.js available.")
        raw = session.get("ifc_js_response")
        if raw:
            st.warning("⚠️ Raw ifc_js_response:")
            st.code(raw, language="json")
        return

    st.subheader("🧮 Object Properties")
    try:
        psets = format_ifc_js_psets(data.get("props", {}))
        for pset in psets.values():
            st.subheader(pset.get("Name", "Unnamed PSet"))
            st.table(pset.get("Data", []))
    except Exception as e:
        st.error(f"❌ Error showing psets: {e}")


# ─────────────────────────────────────────────
# 🚀 Funzione principale di esecuzione pagina
# ─────────────────────────────────────────────
def execute():
    st.set_page_config(page_title="3D", layout="wide")
    st.header("🎮 IFC.js Model Viewer")
    st.markdown(
        "This viewer can inspect the model and its properties."
    )

    if "ifc_file" in session and session["ifc_file"]:
        if "ifc_js_response" not in session:
            session["ifc_js_response"] = ""

        draw_3d_viewer()

        tab1 = st.tabs(["🧮 Properties"])[0]
        with tab1:
            write_pset_data()

    else:
        st.warning("⚠️ Load an IFC file in Home. Please upload a file first.")


# ─────────────────────────────────────────────
# ▶️ Avvia l'app
# ─────────────────────────────────────────────
execute()
