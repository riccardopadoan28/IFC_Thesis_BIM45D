# ─────────────────────────────────────────────
# 📦 Imports (standardized)
# ─────────────────────────────────────────────
import streamlit as st
from tools import p3_bcf as p3  # per-page helper
from tools import p_shared as shared  # shared model info helpers

# ─────────────────────────────────────────────
# 🧠 Session alias
# ─────────────────────────────────────────────
session = st.session_state

# -----------------------------
# ORGANIZZAZIONE DELLA PAGINA
# -----------------------------
# 1) initialize_session_state — init page state
# 2) support functions — UI/data helpers (no ifcopenshell here)
# 3) execute — main entry point building the UI

# ─────────────────────────────────────────────
# 📦 Importazioni
# ─────────────────────────────────────────────
import json
import textwrap
import re
import io
import zipfile
import uuid
import xml.etree.ElementTree as ET
from xml.dom import minidom
from tools.pathhelper import save_text, save_bytes

# ─────────────────────────────────────────────
# 🧠 Alias per lo stato della sessione Streamlit
# ─────────────────────────────────────────────
session = st.session_state

# -----------------------------
# ORGANIZZAZIONE DELLA PAGINA
# -----------------------------
# Questa pagina mostra i risultati IDS salvati e consente l'export in TXT/HTML per report BCF-like.
# Funzioni principali:
# - visualizzazione df di issues e selezione righe per esportazione

st.set_page_config(page_title="BCF / BIM Collaboration", layout='wide')
st.title("📦 BIM Collaboration / BCF Reports")

st.markdown("This page allows exporting the latest IDS validation results as TXT or HTML for BCF-like reporting.")

# Reference to buildingSMART BCF
st.markdown("Reference: [buildingSMART - BIM Collaboration Format (BCF)](https://www.buildingsmart.org/standards/bsi-standards/bim-collaboration-format/)")

# Brief explanation of BCF standard and file structure
st.markdown(
    "BCF is more than a file format — it is a set of specifications, APIs and implementer agreements governed by buildingSMART. "
    "On disk, BCF data can be serialized as individual markup files (.bcf), project index files (.bcfp) and optional visualization files (.bcfv). "
    "A full BCF exchange is commonly packaged as a .bcfzip (a ZIP archive containing the project and markup files)."
)

if "ids_last_validation_df" not in session or session.ids_last_validation_df is None:
    st.info("No validation results available. Run IDS validation or test in the IDS page first.")
else:
    df_export = session.ids_last_validation_df
    df_display = df_export.reset_index(drop=True)
    df_display["_row_id"] = df_display.index.astype(str)
    options = df_display["_row_id"].tolist()
    select_all = st.checkbox("Select all issues", value=True)
    if select_all:
        selected = options
        # reset preview when selection changes
        session.report_preview = False
    else:
        selected = st.multiselect("Select issue rows (by index)", options, default=options[:0])
        # reset preview when selection changes
        session.report_preview = False

    selected_df = df_display[df_display["_row_id"].isin(selected)].drop(columns=["_row_id"]) if selected else df_display.iloc[0:0]
    if selected_df.empty:
        st.info("No issues selected.")
    else:
        st.info(f"{len(selected_df)} issue(s) selected — click 'Generate Preview' to view summary and details.")

    # Report Generator: metadata inputs, summary table and preview
    st.subheader("🧾 Report Generator")
    report_title = st.text_input("Report Title", value="IDS Validation Report")
    report_author = st.text_input("Author", value=session.get("user_email", "generated@bim45d.local"))
    report_project = st.text_input("Project", value="")
    from datetime import date
    report_date = st.date_input("Report Date", value=date.today())
    include_summary = st.checkbox("Include summary table", value=True)

    if "report_preview" not in session:
        session.report_preview = False

    if st.button("Generate Preview"):
        session.report_preview = True

    # Render preview only when requested
    if session.report_preview:
        # Build summary per IFCClass
        try:
            summary = selected_df.groupby("IFCClass").agg(
                Total=("ElementID", "count"),
                Passed=("Compliant", lambda s: int(s.sum())),
                Failed=("Compliant", lambda s: int((~s.astype(bool)).sum()))
            ).reset_index()
        except Exception:
            # fallback empty summary
            import pandas as pd
            summary = pd.DataFrame(columns=["IFCClass", "Total", "Passed", "Failed"]) 

        st.markdown(f"**{report_title}** — Author: {report_author} — Project: {report_project} — Date: {report_date}")
        if include_summary:
            summary_container = st.container()
            summary_container.subheader("Report Summary")
            summary_container.dataframe(summary, use_container_width=True)

        st.subheader("Selected Issues (preview)")
        st.dataframe(selected_df, use_container_width=True)

        # Only two export buttons: Full Report (HTML) and .bcfzip
        combined_html = f"<h1>{report_title}</h1><p><strong>Author:</strong> {report_author}</p><p><strong>Project:</strong> {report_project}</p><p><strong>Date:</strong> {report_date}</p>"
        if include_summary:
            combined_html += summary.to_html(index=False)
        combined_html += selected_df.to_html(index=False)

        # Button: Full HTML report
        st.download_button("Download Full Report (HTML)", combined_html.encode('utf-8'), "report_full.html", "text/html")
        if st.button("Save HTML to temp_file", key="btn_save_bcf_html"):
            try:
                path, url = save_text("report_full.html", combined_html)
                st.success(f"Saved in static/temp_file — {path.name}")
                st.markdown(f"[Click to download]({url})")
            except Exception as e:
                st.error(f"Unable to save: {e}")

        # Button: Export .bcfzip (minimal BCF archive)
        try:
            # Helper to build a simple markup.bcf XML for a topic
            def build_markup_xml(topic_id, title, description, author, date_str, fields):
                root = ET.Element('Markup')
                topic = ET.SubElement(root, 'Topic')
                ET.SubElement(topic, 'Guid').text = topic_id
                ET.SubElement(topic, 'Title').text = title
                ET.SubElement(topic, 'Description').text = description
                ET.SubElement(topic, 'CreationAuthor').text = author
                ET.SubElement(topic, 'CreationDate').text = date_str

                custom_data = ET.SubElement(topic, 'CustomData')
                for k, v in fields.items():
                    cd = ET.SubElement(custom_data, 'Field')
                    ET.SubElement(cd, 'Name').text = str(k)
                    ET.SubElement(cd, 'Value').text = '' if v is None else str(v)

                raw = ET.tostring(root, encoding='utf-8')
                return minidom.parseString(raw).toprettyxml(indent='  ')

            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, mode='w', compression=zipfile.ZIP_DEFLATED) as z:
                topic_ids = []
                cols = list(selected_df.columns)
                for _, row in selected_df.reset_index(drop=True).iterrows():
                    tid = str(uuid.uuid4())
                    topic_ids.append(tid)
                    title = str(row.get('ElementName', 'Issue'))
                    description = f"Issue for ElementID: {row.get('ElementID', '')}\nIFCClass: {row.get('IFCClass', '')}\nProperty: {row.get('PropertyName', '')}\nValue: {row.get('Value', '')}"
                    fields = {c: row[c] for c in cols}
                    markup_xml = build_markup_xml(tid, title, description, report_author, str(report_date), fields)
                    topic_folder = f"topics/{tid}/"
                    z.writestr(topic_folder + 'markup.bcf', markup_xml.encode('utf-8'))

                project_root = ET.Element('BCFProject')
                ET.SubElement(project_root, 'Title').text = str(report_title)
                ET.SubElement(project_root, 'ProjectID').text = str(uuid.uuid4())
                ET.SubElement(project_root, 'Author').text = str(report_author)
                ET.SubElement(project_root, 'Project').text = str(report_project)
                ET.SubElement(project_root, 'Date').text = str(report_date)

                topics_el = ET.SubElement(project_root, 'Topics')
                for tid in topic_ids:
                    t = ET.SubElement(topics_el, 'Topic')
                    ET.SubElement(t, 'Guid').text = tid
                    ET.SubElement(t, 'MarkupFile').text = f"topics/{tid}/markup.bcf"

                project_raw = ET.tostring(project_root, encoding='utf-8')
                project_pretty = minidom.parseString(project_raw).toprettyxml(indent='  ')
                z.writestr('project.bcfp', project_pretty.encode('utf-8'))

            zip_buffer.seek(0)
            bcfzip_bytes = zip_buffer.read()
            st.download_button("Export .bcfzip", bcfzip_bytes, "report_issues.bcfzip", "application/zip")
            if st.button("Save .bcfzip to temp_file", key="btn_save_bcf_zip"):
                try:
                    path, url = save_bytes("report_issues.bcfzip", bcfzip_bytes)
                    st.success(f"Saved in static/temp_file — {path.name}")
                    st.markdown(f"[Click to download]({url})")
                except Exception as e:
                    st.error(f"Unable to save: {e}")

        except Exception as e:
            st.error(f"Error generating .bcfzip file: {e}")
    else:
        st.info("Select at least one issue to enable exports.")

# Uniform page structure applied. If you still have direct ifcopenshell logic here, consider moving it into the corresponding tools module (p0..p8) for consistency.
