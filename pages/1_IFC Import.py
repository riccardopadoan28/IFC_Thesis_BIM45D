# ─────────────────────────────────────────────
# 📦 Importazioni
# ─────────────────────────────────────────────
import ifcopenshell as ifc
import streamlit as st
import os
import time

# ─────────────────────────────────────────────
# 🧠 Alias per lo stato della sessione Streamlit
# ─────────────────────────────────────────────
session = st.session_state

# -----------------------------
# ORGANIZZAZIONE DELLA PAGINA
# -----------------------------
# Funzioni principali e scopi (in italiano):
# 1) callback_upload -> USATA: file_uploader callback; SCOPO: salva file in sessione e temp path
# 2) load_ifc_file -> USATA: helper; SCOPO: ricarica il file IFC dal temp path
# 3) main -> USATA: entry point della pagina; SCOPO: interfaccia upload e rimozione file

# ─────────────────────────────────────────────
# 📤 Callback per caricamento file
# ─────────────────────────────────────────────
def callback_upload():
    if "uploaded_file" in session and session["uploaded_file"] is not None:
        uploaded_data = session["uploaded_file"].getvalue()
        session["array_buffer"] = uploaded_data
        session["file_name"] = session["uploaded_file"].name
        session["is_file_uploaded"] = True

        # Salva temporaneamente il file per lettura affidabile
        os.makedirs("temp_downloads", exist_ok=True)
        temp_path = os.path.join("temp_downloads", "temp_model.ifc")
        with open(temp_path, "wb") as f:
            f.write(uploaded_data)
        session["temp_ifc_path"] = temp_path

        # Carica e salva l'oggetto IFC file in sessione
        try:
            ifc_file = ifc.open(temp_path)
            session["ifc_file"] = ifc_file
            session["ifc_schema"] = ifc_file.schema  # salva l'oggetto schema, non la stringa
        except Exception as e:
            st.error(f"⚠️ Failed to load IFC file: {e}")

# ─────────────────────────────────────────────
# 🔄 Funzione per caricare IFC dal file temporaneo
# ─────────────────────────────────────────────
def load_ifc_file():
    if "temp_ifc_path" in session:
        try:
            ifc_file = ifc.open(session["temp_ifc_path"])
            session["ifc_schema"] = ifc_file.schema
            return ifc_file
        except Exception as e:
            st.error(f"⚠️ Failed to load IFC file: {e}")
    return None

# ─────────────────────────────────────────────
# 🚀 Funzione principale Streamlit
# ─────────────────────────────────────────────
def main():
    st.title("📁 Upload IFC Model")
    st.markdown("Upload your IFC model (max 200 MB) to start exploring its data.")

    uploaded_file = st.file_uploader(
        "Choose a file", 
        key="uploaded_file", 
        on_change=callback_upload
    )

    # Mostra info file caricato se già presente in sessione
    if session.get("is_file_uploaded") and session.get("temp_ifc_path"):
        st.sidebar.success("✅ File uploaded successfully!")
        st.write(f"**File name:** {session.get('file_name', 'Unknown')}")
        ifc_file = session.get("ifc_file")
        if ifc_file:
            st.info(f"📐 IFC Schema Detected: **{str(session.get('ifc_schema', 'Unknown'))}**")
        if st.button("🗑️ Remove IFC File"):
            for key in ["array_buffer", "uploaded_file", "file_name", "ifc_schema", "is_file_uploaded", "temp_ifc_path", "ifc_file"]:
                session.pop(key, None)
            st.sidebar.warning("🗑️ IFC file removed from session.")
    elif session.get("is_file_uploaded"):
        with st.spinner("🔃 Processing uploaded file..."):
            time.sleep(1)
        st.sidebar.success("✅ File uploaded successfully!")
        st.write(f"**File name:** {session.get('file_name', 'Unknown')}")
        ifc_file = session.get("ifc_file")
        if ifc_file:
            st.info(f"📐 IFC Schema Detected: **{str(session.get('ifc_schema', 'Unknown'))}**")
        if st.button("🗑️ Remove IFC File"):
            for key in ["array_buffer", "uploaded_file", "file_name", "ifc_schema", "is_file_uploaded", "temp_ifc_path", "ifc_file"]:
                session.pop(key, None)
            st.sidebar.warning("🗑️ IFC file removed from session.")
    else:
        st.info("⚠️ No IFC file uploaded yet.")

# ─────────────────────────────────────────────
# ▶️ Entry Point
# ─────────────────────────────────────────────
if __name__ == "__main__":
    main()
