import os
import glob
import shutil
from pathlib import Path
import streamlit as st
from tools.pathhelper import ensure_session_id, get_session_dir, cleanup_session, ensure_data_dir, clear_data_dir

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
viewer_src_dir = project_root / "viewer"
static_dir = project_root / "static"
static_dir.mkdir(parents=True, exist_ok=True)
viewer_static_dir = static_dir / "viewer"
try:
    shutil.copytree(viewer_src_dir, viewer_static_dir, dirs_exist_ok=True)
except Exception:
    pass

# Resolve model src from unified data dir
sid = ensure_session_id(st.session_state)
src = st.session_state.get("viewer_src_rel")  # like /static/temp_file/uploaded.ifc
iframe_src = "/static/viewer/viewer.html" + (f"?src={src}" if src else "")

# Full-width viewer (no right column)
st.markdown(
    f'<iframe src="{iframe_src}" style="width:100%;height:80vh;border:0;" scrolling="no" allow="fullscreen"></iframe>',
    unsafe_allow_html=True,
)