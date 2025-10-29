import os
import glob
import shutil
from pathlib import Path
import streamlit as st
from tools import p5_viewer
from tools.pathhelper import ensure_session_id
from tools import p_shared as shared  # shared model info helpers
import subprocess
import time

# ─────────────────────────────────────────────
# 🧠 Session alias
# ─────────────────────────────────────────────
session = st.session_state

st.set_page_config(page_title="Viewer", layout="wide")
# Header and short description
st.header("🔎 3D Model Viewer (IFC → XKT with Xeokit)")
st.markdown(
    """
    Automated model viewer with IFC4x3 support. Upload an IFC on the IFC Import page and it will load here automatically.
    """
)
st.markdown(
    "Reference: [Building 3D Model Viewers with xeokit-webcomponents](https://xeokit.io/blog/building-3d-model-viewers-with-xeokit-webcomponents/)"
)


ifc_path = Path("static/temp_file/uploaded.ifc")
xkt_path = Path("static/models/uploaded.xkt")
viewer_path = Path("viewer/viewer.html")

# 1️⃣ Controllo esistenza file IFC
if not ifc_path.exists():
    st.warning("⚠️ No IFC file found at `static/temp_file/uploaded.ifc`.")
    st.stop()

# 2️⃣ Bottone per conversione
if st.button("Convert IFC → XKT"):
    st.write("⏳ Converting... (this may take a few seconds)")
    try:
        # Ensure output directory exists
        xkt_path.parent.mkdir(parents=True, exist_ok=True)
        # Run converter
        subprocess.run([
            "xeokit-convert",
            str(ifc_path),
            str(xkt_path)
        ], check=True)
        st.success("✅ Conversion completed! File created: `static/models/uploaded.xkt`")
    except FileNotFoundError:
        st.error("❌ 'xeokit-convert' not found. Make sure it is installed and on PATH.")
        st.stop()
    except Exception as e:
        st.error(f"❌ Conversion error: {e}")
        st.stop()

# 3️⃣ Mostra il viewer
if xkt_path.exists():
    st.markdown("---")
    st.subheader("3D Model Viewer")

    # Leggi il file HTML del viewer
    with open(viewer_path, "r", encoding="utf-8") as f:
        html_code = f.read()

    # Cache-bust the model URL to avoid stale loads
    ts = int(time.time())
    html_code = html_code.replace("/static/models/uploaded.xkt", f"/static/models/uploaded.xkt?ts={ts}")

    # Inserisci direttamente il viewer nella pagina
    st.components.v1.html(html_code, height=800)
else:
    st.info("ℹ️ Please convert the IFC file first to view it.")
