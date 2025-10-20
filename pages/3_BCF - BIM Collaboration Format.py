# ─────────────────────────────────────────────
# 📦 Importazioni
# ─────────────────────────────────────────────
import streamlit as st
import json
import textwrap
import re
import io
from fpdf import FPDF

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

        # Download buttons for report artifacts
        summary_csv = summary.to_csv(index=False).encode('utf-8')
        st.download_button("Download Summary CSV", summary_csv, "report_summary.csv", "text/csv")

        combined_html = f"<h1>{report_title}</h1><p><strong>Author:</strong> {report_author}</p><p><strong>Project:</strong> {report_project}</p><p><strong>Date:</strong> {report_date}</p>"
        if include_summary:
            combined_html += summary.to_html(index=False)
        combined_html += selected_df.to_html(index=False)

        st.download_button("Download Full Report (HTML)", combined_html.encode('utf-8'), "report_full.html", "text/html")

        # HTML export (separate full issues table)
        html_report = selected_df.to_html(index=False, border=0)
        st.download_button("Export HTML", html_report.encode('utf-8'), "bcf_issues.html", "text/html")

        # BCF (.bcf) export - simple BCF-like XML serialization of selected issues
        try:
            import xml.etree.ElementTree as ET
            from xml.dom import minidom

            bcf_root = ET.Element('BCFMarkup')
            meta = ET.SubElement(bcf_root, 'Metadata')
            ET.SubElement(meta, 'Title').text = str(report_title if 'report_title' in locals() else '')
            ET.SubElement(meta, 'Author').text = str(report_author if 'report_author' in locals() else '')
            ET.SubElement(meta, 'Project').text = str(report_project if 'report_project' in locals() else '')
            ET.SubElement(meta, 'Date').text = str(report_date if 'report_date' in locals() else '')

            topics = ET.SubElement(bcf_root, 'Topics')
            cols = list(selected_df.columns)
            for i, row in selected_df.iterrows():
                topic = ET.SubElement(topics, 'Topic', {'id': str(i)})
                for c in cols:
                    child = ET.SubElement(topic, re.sub(r"[^0-9a-zA-Z_]", "_", str(c)))
                    child.text = '' if row[c] is None else str(row[c])

            bcf_bytes = ET.tostring(bcf_root, encoding='utf-8')
            pretty_bcf = minidom.parseString(bcf_bytes).toprettyxml(indent='  ')
            st.download_button("Export .bcf", pretty_bcf.encode('utf-8'), "report_issues.bcf", "application/xml")
        except Exception as e:
            st.error(f"Error generating .bcf file: {e}")
    else:
        st.info("Select at least one issue to enable exports.")
