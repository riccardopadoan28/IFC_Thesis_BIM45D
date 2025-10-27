# ─────────────────────────────────────────────
# 📦 Importazioni
# ─────────────────────────────────────────────
import ifcopenshell as ifc
import streamlit as st
import time
from pathlib import Path

# Usa la cartella temporanea unificata se disponibile
try:
    from tools.pathhelper import ensure_temp_dir, TEMP_DIR
except Exception:
    ensure_temp_dir = None
    TEMP_DIR = Path("temp")

# ─────────────────────────────────────────────
# 🧠 Alias per lo stato della sessione Streamlit
# ─────────────────────────────────────────────
session = st.session_state

# -----------------------------
# ORGANIZZAZIONE DELLA PAGINA
# -----------------------------
# Funzioni principali e scopi (in italiano):
# 1) callback_upload -> USATA: file_uploader callback; SCOPO: salva file in sessione e temp path
# 2) main -> USATA: entry point della pagina; SCOPO: interfaccia upload e info

# ─────────────────────────────────────────────
# 📤 Callback per caricamento file
# ─────────────────────────────────────────────

def callback_upload():
    if "uploaded_file" in session and session["uploaded_file"] is not None:
        uploaded_data = session["uploaded_file"].getvalue()
        session["array_buffer"] = uploaded_data
        session["file_name"] = session["uploaded_file"].name
        session["is_file_uploaded"] = True

        # Save to unified temp folder
        try:
            temp_dir = ensure_temp_dir() if ensure_temp_dir else (Path.cwd() / "temp")
            temp_dir.mkdir(parents=True, exist_ok=True)
            temp_path = temp_dir / "temp_model.ifc"
            with open(temp_path, "wb") as f:
                f.write(uploaded_data)
            session["temp_ifc_path"] = str(temp_path)

            # Save to static/uploads (served by Streamlit) and expose URL for viewer
            project_root = Path(__file__).resolve().parent.parent
            static_uploads = project_root / "static" / "uploads"
            static_uploads.mkdir(parents=True, exist_ok=True)
            uploaded_name = session.get("uploaded_file").name or "uploaded.ifc"
            safe_name = "uploaded" + (Path(uploaded_name).suffix or ".ifc")
            target_path = static_uploads / safe_name
            with open(target_path, "wb") as vf:
                vf.write(uploaded_data)
            session["viewer_src_rel"] = f"/static/uploads/{safe_name}"
        except Exception as e:
            st.error(f"⚠️ Failed to write temp IFC file: {e}")
            return

        # Load IFC file object into session
        try:
            ifc_file = ifc.open(str(temp_path))
            session["ifc_file"] = ifc_file
            session["ifc_schema"] = ifc_file.schema
        except Exception as e:
            st.error(f"⚠️ Failed to load IFC file: {e}")

# ─────────────────────────────────────────────
# 🚀 Funzione principale Streamlit
# ─────────────────────────────────────────────

def main():
    st.title("📁 Upload IFC Model")
    st.markdown("Upload your IFC model (max 200 MB). XKT conversion and the 3D view are available on page ‘5_3D Model Viewer’.")

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
