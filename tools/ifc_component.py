import os
import streamlit.components.v1 as components
import shutil

# Percorso assoluto alla build del frontend
_build_dir = os.path.join(os.path.dirname(__file__), "../frontend-viewer/build")
print("Percorso build frontend:", os.path.abspath(_build_dir))

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

# Funzione per copiare il file IFC caricato nella cartella frontend-viewer/public e restituire l'url

def save_ifc_to_public(ifc_file):
    public_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend-viewer", "public"))
    os.makedirs(public_dir, exist_ok=True)
    dest_path = os.path.join(public_dir, "temp_model.ifc")
    # Gestione sia file-like che bytes
    if hasattr(ifc_file, "getbuffer"):
        data = ifc_file.getbuffer()
    elif isinstance(ifc_file, bytes):
        data = ifc_file
    else:
        raise TypeError("Il file IFC deve essere un file-like con getbuffer() o bytes.")
    with open(dest_path, "wb") as f:
        f.write(data)
    # L'url sarà relativo alla root del frontend (public)
    return "/temp_model.ifc"
