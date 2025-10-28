import os
import glob
import shutil
from pathlib import Path
import streamlit as st
from tools import p5_viewer
from tools.pathhelper import ensure_session_id
from tools import p_shared as shared  # shared model info helpers

# ─────────────────────────────────────────────
# 🧠 Session alias
# ─────────────────────────────────────────────
session = st.session_state

st.set_page_config(page_title="Viewer", layout="wide")
# Header and short description
st.header("🔎 Model Viewer")
st.markdown(
    """
    Automated model viewer with IFC4x3 support. Upload an IFC on the IFC Import page and it will load here automatically.
    """
)
st.markdown(
    "Reference: [Building 3D Model Viewers with xeokit-webcomponents](https://xeokit.io/blog/building-3d-model-viewers-with-xeokit-webcomponents/)"
)

# Ensure viewer folder is mirrored under /static
project_root = Path(__file__).resolve().parent.parent
viewer_static_dir = p5_viewer.ensure_viewer_static(project_root)

# Resolve model src from unified data dir
sid = ensure_session_id(st.session_state)
src = st.session_state.get("viewer_src_rel")  # like /static/temp_file/uploaded.ifc
iframe_src = p5_viewer.compose_iframe_src(src)

# Full-width viewer (no right column)
st.markdown(
    f'<iframe src="{iframe_src}" style="width:100%;height:80vh;border:0;" scrolling="no" allow="fullscreen"></iframe>',
    unsafe_allow_html=True,
)

# Uniform page structure applied. If you still have direct ifcopenshell logic here, consider moving it into the corresponding tools module (p0..p8) for consistency.