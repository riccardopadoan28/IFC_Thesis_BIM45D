"""
Helper per Pagina 5 — 3D Model Viewer

Uso: pages/5_3D Model Viewer.py
Funzioni:
- ensure_viewer_static(project_root): copia/mirrors viewer/ sotto static/viewer
- compose_iframe_src(src): costruisce l'URL dell'iframe (forza CDN)
"""

# Commenti in italiano, output in inglese

from __future__ import annotations
from pathlib import Path
import shutil


def ensure_viewer_static(project_root: Path) -> Path:
    """Copia la cartella `viewer/` in `static/viewer/` per essere servita da Streamlit."""
    viewer_src = project_root / "viewer"
    static_dir = project_root / "static"
    static_dir.mkdir(parents=True, exist_ok=True)
    viewer_dst = static_dir / "viewer"
    shutil.copytree(viewer_src, viewer_dst, dirs_exist_ok=True)
    # Se presente una build locale di webcomponents, copia anche i chunk
    dist_static_src = viewer_src / "lib" / "dist" / "static"
    if dist_static_src.exists():
        shutil.copytree(dist_static_src, viewer_dst / "static", dirs_exist_ok=True)
    return viewer_dst


def compose_iframe_src(src: str | None) -> str:
    """Costruisce l'URL per /static/viewer/viewer.html includendo i parametri query.
    Forziamo il CDN per evitare errori di MIME quando i chunk locali non esistono."""
    params = []
    if src:
        params.append(f"src={src}")
    params.append("useCdn=1")
    q = ("?" + "&".join(params)) if params else ""
    return f"/static/viewer/viewer.html{q}"
