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

# Ensure viewer.html is served from /static
project_root = Path(__file__).resolve().parent.parent
viewer_src_path = project_root / "viewer" / "viewer.html"
static_dir = project_root / "static"
static_dir.mkdir(parents=True, exist_ok=True)
viewer_static_path = static_dir / "viewer.html"
try:
    shutil.copyfile(viewer_src_path, viewer_static_path)
except Exception:
    pass

# Resolve model src from unified data dir
sid = ensure_session_id(st.session_state)
src = st.session_state.get("viewer_src_rel")  # like /static/temp_file/uploaded.ifc
iframe_src = "/static/viewer.html" + (f"?src={src}" if src else "")

col1, col2 = st.columns([1, 1])
with col1:
    st.markdown(
        f'<iframe src="{iframe_src}" style="width:100%;height:70vh;border:0;" scrolling="no" allow="fullscreen"></iframe>',
        unsafe_allow_html=True,
    )
with col2:
    dd = ensure_data_dir()
    st.info("Unified folder: static/temp_file")
    if src:
        st.success("Model URL: " + src)
    if st.button("🧹 Clear temp_file", type="primary"):
        clear_data_dir()
        for k in [
            "viewer_src_rel",
            "array_buffer",
            "uploaded_file",
            "file_name",
            "ifc_schema",
            "is_file_uploaded",
            "temp_ifc_path",
            "ifc_file",
        ]:
            st.session_state.pop(k, None)
        st.rerun()