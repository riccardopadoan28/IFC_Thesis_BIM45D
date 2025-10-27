import os
import glob
from pathlib import Path
import streamlit as st

st.set_page_config(page_title="Viewer", layout="wide")
st.header("🔎 Model Viewer")

# Short English description
st.markdown("""
            Automated model viewer with IFC4x3 support.
            Upload an IFC file on the page to visualize it here.
    """)
st.markdown("Reference: [Building 3D Model Viewers with xeokit-webcomponents](https://xeokit.io/blog/building-3d-model-viewers-with-xeokit-webcomponents/)")

# Load viewer HTML
viewer_path = os.path.join(os.path.dirname(__file__), "..", "viewer", "viewer.html")
with open(viewer_path, "r", encoding="utf-8") as f:
    html = f.read()

# Resolve model src: session → latest in static/uploads → none
src = st.session_state.get("viewer_src_rel")
if not src:
    project_root = Path(__file__).resolve().parent.parent
    uploads_dir = project_root / "static" / "uploads"
    patterns = [str(uploads_dir / "*.ifc"), str(uploads_dir / "*.ifczip")]
    candidates = []
    for pat in patterns:
        candidates.extend(glob.glob(pat))
    if candidates:
        latest = max(candidates, key=lambda p: os.path.getmtime(p))
        src = "/static/uploads/" + os.path.basename(latest)

# Inject MODEL_SRC if available
if src:
    inject = f"<script>window.MODEL_SRC='{src}';</script>"
    html = html.replace("</head>", inject + "\n</head>")

st.components.v1.html(html, height=900, scrolling=True)