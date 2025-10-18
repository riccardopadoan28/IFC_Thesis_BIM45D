# New page: BCF / BIM Collaboration Specification
import streamlit as st
import json
import textwrap
import re
import io

session = st.session_state

st.set_page_config(page_title="BCF / BIM Collaboration", layout='wide')
st.title("📦 BIM Collaboration / BCF Reports")

st.markdown("This page allows exporting the latest IDS validation results as TXT or HTML for BCF-like reporting.")

# Reference to buildingSMART BCF
st.markdown("Reference: [buildingSMART - BIM Collaboration Format (BCF)](https://www.buildingsmart.org/standards/bsi-standards/bim-collaboration-format/)")

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
    else:
        selected = st.multiselect("Select issue rows (by index)", options, default=options[:0])

    selected_df = df_display[df_display["_row_id"].isin(selected)].drop(columns=["_row_id"]) if selected else df_display.iloc[0:0]
    st.dataframe(selected_df, use_container_width=True)

    if not selected_df.empty:
        # TXT export
        txt_content = selected_df.to_csv(sep='\t', index=False)
        st.download_button("Export TXT", txt_content.encode('utf-8'), "bcf_issues.txt", "text/plain")

        # HTML export
        html_report = selected_df.to_html(index=False, border=0)
        st.download_button("Export HTML", html_report.encode('utf-8'), "bcf_issues.html", "text/html")
    else:
        st.info("Select at least one issue to enable exports.")
