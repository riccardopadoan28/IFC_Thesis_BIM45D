import os
import streamlit.components.v1 as components

# Percorso assoluto alla build del frontend
_build_dir = os.path.join(os.path.dirname(__file__), "../frontend-viewer/build")

# Dichiarazione del componente custom
ifc_js_viewer_component = components.declare_component(
    "ifc_js_viewer",
    path=_build_dir
)

def ifc_js_viewer(url: str, key: str = None):
    """
    Wrapper per visualizzare l'IFC nel viewer.
    - url: percorso accessibile al browser (es. '/static/temp_model.ifc')
    - key: chiave Streamlit opzionale
    """
    return ifc_js_viewer_component(url=url, key=key)
