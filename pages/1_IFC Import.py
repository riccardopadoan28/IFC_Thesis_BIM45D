# ─────────────────────────────────────────────
# 📦 Imports (standardized)
# ─────────────────────────────────────────────
import streamlit as st
from tools import p_shared as shared  # shared model info helpers
from tools import p1_ifc_import as p1  # per-page helper
from pathlib import Path
from tools.pathhelper import ensure_data_dir, public_url
import ifcopenshell as ifc
import time

# ─────────────────────────────────────────────
# 🧠 Session alias
# ─────────────────────────────────────────────
session = st.session_state

# -----------------------------
# ORGANIZZAZIONE DELLA PAGINA
# -----------------------------
# 1) initialize_session_state — init page state
# 2) support functions — UI/data helpers (no ifcopenshell here)
# 3) execute — main entry point building the UI

# ─────────────────────────────────────────────
# 📤 Callback per caricamento file
# ─────────────────────────────────────────────

def callback_upload():
    if "uploaded_file" in session and session["uploaded_file"] is not None:
        uploaded_data = session["uploaded_file"].getvalue()
        session["array_buffer"] = uploaded_data
        session["file_name"] = session["uploaded_file"].name
        session["is_file_uploaded"] = True

        # Save everything under static/temp_file
        try:
            data_dir = ensure_data_dir()
            original_name = session.get("uploaded_file").name or "uploaded.ifc"
            ext = Path(original_name).suffix or ".ifc"
            stored_path = data_dir / ("uploaded" + ext)
            with open(stored_path, "wb") as f:
                f.write(uploaded_data)
            session["temp_ifc_path"] = str(stored_path)
            session["viewer_src_rel"] = public_url(stored_path)
        except Exception as e:
            st.error(f"⚠️ Failed to persist IFC: {e}")
            return

        # Load IFC file object into session
        try:
            ifc_file = ifc.open(session["temp_ifc_path"])
            session["ifc_file"] = ifc_file
            session["ifc_schema"] = ifc_file.schema
        except Exception as e:
            st.error(f"⚠️ Failed to load IFC file: {e}")

# ─────────────────────────────────────────────
# 🚀 Funzione principale Streamlit
# ─────────────────────────────────────────────

def main():
    st.title("📁 Upload IFC Model")
    st.markdown("Upload your IFC model (max 200 MB).")

    st.file_uploader(
        "Choose a file",
        key="uploaded_file",
        on_change=callback_upload
    )

    # On-page expander for status and actions (no sidebar)
    if session.get("is_file_uploaded") and session.get("temp_ifc_path"):
        with st.expander("Uploaded IFC details", expanded=True):
            st.success("✅ File uploaded successfully.")
            st.write(f"File name: {session.get('file_name', 'Unknown')}")
            if session.get("ifc_file"):
                st.info(f"📐 IFC schema detected: {str(session.get('ifc_schema', 'Unknown'))}")
            if st.button("🗑️ Remove IFC File"):
                for key in [
                    "array_buffer", "uploaded_file", "file_name", "ifc_schema",
                    "is_file_uploaded", "temp_ifc_path", "ifc_file"
                ]:
                    session.pop(key, None)
                st.warning("🗑️ IFC file removed from session.")
    elif session.get("is_file_uploaded"):
        with st.spinner("🔃 Processing uploaded file..."):
            time.sleep(1)
        with st.expander("Uploaded IFC details", expanded=True):
            st.success("✅ File uploaded successfully.")
            st.write(f"File name: {session.get('file_name', 'Unknown')}")
            if session.get("ifc_file"):
                st.info(f"📐 IFC schema detected: {str(session.get('ifc_schema', 'Unknown'))}")
            if st.button("🗑️ Remove IFC File"):
                for key in [
                    "array_buffer", "uploaded_file", "file_name", "ifc_schema",
                    "is_file_uploaded", "temp_ifc_path", "ifc_file"
                ]:
                    session.pop(key, None)
                st.warning("🗑️ IFC file removed from session.")
    else:
        st.info("⚠️ No IFC file uploaded yet.")

# ─────────────────────────────────────────────
# ▶️ Entry Point
# ─────────────────────────────────────────────
if __name__ == "__main__":
    main()
