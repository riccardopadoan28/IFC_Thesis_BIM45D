import os
import json
import base64
import subprocess
from pathlib import Path
import streamlit as st
from streamlit.components.v1 import html

# Page setup
st.set_page_config(page_title="3D Model Viewer (xeokit SDK)", layout="wide")
st.title("3D Model Viewer (xeokit SDK)")

# Session and IFC input
session = st.session_state
input_ifc_path = session.get("temp_ifc_path", "")
input_ifc_name = session.get("file_name", "model.ifc")

st.subheader("Load Scene")
if not input_ifc_path or not os.path.exists(input_ifc_path):
    st.warning("No IFC loaded. Go to 'IFC Import' to upload a file.")
else:
    st.success(f"Source IFC: {input_ifc_name}")

# Path to convesion.js (wrapper)
default_conversion_js = Path(__file__).resolve().parents[1] / "frontend-viewer" / "convesion.js"
conversion_js_str = st.text_input(
    "Path to convesion.js",
    value=str(default_conversion_js),
    help="Path to the Node wrapper script (convesion.js) for convert2xkt."
)
conversion_js = Path(conversion_js_str)
st.caption(f"Using converter script: {conversion_js}")

# Node executable
node_exec = st.text_input(
    "Node executable",
    value="node",
    help="Full path to node.exe or 'node' if Node.js is available on PATH"
)
st.caption(f"Using Node: {node_exec}")

base_name = os.path.splitext(os.path.basename(input_ifc_name))[0]
out_dir = Path("temp-download")
out_name = f"{base_name}.xkt"
mem_mb = st.number_input(
    "Node max-old-space-size (MB)",
    min_value=2048,
    max_value=65536,
    value=16384,
    step=1024,
    help="Increase if you hit out-of-memory errors"
)

col_a, col_b, col_c = st.columns([1, 1, 2])
with col_a:
    export_props = st.checkbox("Export properties (-p)", value=False)
with col_b:
    show_help = st.button("Show CLI help")
with col_c:
    run_convert = st.button("Load Scene")

props_dir_input = None
if export_props:
    default_props_dir = str(out_dir / "properties" / base_name)
    props_dir_input = st.text_input(
        "Target directory for properties (-p)",
        value=default_props_dir,
        help="Directory where object property files will be written"
    )

meta_model_src = st.text_input(
    "Optional source metamodel JSON path (-m)",
    value="",
    help="Path to a source metamodel JSON file, if you have one"
)

# Helper to run subprocess
def _run(cmd_list):
    return subprocess.run(cmd_list, capture_output=True, text=True, shell=False)

# CLI help
if show_help:
    if not conversion_js.exists():
        st.error(f"convesion.js not found at: {conversion_js}")
    else:
        try:
            result = _run([node_exec, f"--max-old-space-size={int(mem_mb)}", str(conversion_js), "-h"]) 
            st.code(result.stdout or result.stderr or "No output", language="bash")
        except FileNotFoundError:
            st.error(f"Node executable not found: '{node_exec}'. Set full path to node.exe or add Node.js to PATH.")
        except Exception as e:
            st.error(f"Error running help: {e}")

# Conversion
if run_convert:
    if not input_ifc_path or not os.path.exists(input_ifc_path):
        st.error("No IFC available to convert.")
    elif not conversion_js.exists():
        st.error("Provided convesion.js path does not exist.")
    else:
        try:
            out_dir.mkdir(parents=True, exist_ok=True)
            out_path = out_dir / out_name
            cmd = [
                node_exec,
                f"--max-old-space-size={int(mem_mb)}",
                str(conversion_js),
                "-s", input_ifc_path,
                "-o", str(out_path),
                "-l"
            ]
            if export_props and props_dir_input:
                Path(props_dir_input).mkdir(parents=True, exist_ok=True)
                cmd.extend(["-p", props_dir_input])
            if meta_model_src.strip():
                cmd.extend(["-m", meta_model_src.strip()])

            with st.spinner("Converting and loading scene... (please wait)"):
                result = _run(cmd)

            if result.returncode == 0 and out_path.exists():
                try:
                    xkt_bytes = out_path.read_bytes()
                    session["last_xkt_path"] = str(out_path)
                    session["last_xkt_b64"] = base64.b64encode(xkt_bytes).decode("ascii")
                    st.success(f"Scene ready: {out_path}")
                    st.download_button(
                        "Download .xkt",
                        data=xkt_bytes,
                        file_name=out_path.name,
                        mime="application/octet-stream"
                    )
                    if export_props and props_dir_input:
                        st.info(f"Properties written to: {props_dir_input}")
                    with st.expander("Conversion log"):
                        st.text(result.stdout or "No log output.")
                        if result.stderr:
                            st.text("STDERR:\n" + result.stderr)
                except Exception as e:
                    st.warning(f"Generated file but could not offer download automatically: {e}")
            else:
                st.error("Conversion failed.")
                with st.expander("Execution details"):
                    st.text("STDOUT:\n" + (result.stdout or ""))
                    st.text("STDERR:\n" + (result.stderr or ""))
        except FileNotFoundError:
            st.error("Node or convesion.js not found. Check the paths and Node.js installation.")
        except Exception as e:
            st.error(f"Error during execution: {e}")

# Viewer
st.subheader("Viewer")
meta_model_url = st.text_input("metaModel JSON URL (optional)", "")

xkt_b64 = session.get("last_xkt_b64", "")
html_path = Path(__file__).resolve().parent / "xeokit_xkt_viewer.html"
if not html_path.exists():
    st.error(f"Template not found: {html_path}")
else:
    html_content = html_path.read_text(encoding="utf-8")
    # Nessun URL XKT: usiamo base64 incorporato
    html_content = html_content.replace("XKT_URL_JSON", json.dumps(""))
    html_content = html_content.replace("META_URL_JSON", json.dumps(meta_model_url.strip()))
    html_content = html_content.replace("XKT_B64_JSON", json.dumps(xkt_b64))
    html(html_content, height=800, scrolling=False)

