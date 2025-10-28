# ─────────────────────────────────────────────
# 📦 Imports (standardized)
# ─────────────────────────────────────────────
import streamlit as st
from tools import ifc_prop_qtt as ifc_props  # per-page helper (page 6)
from tools import p_shared as shared  # shared model info helpers
import pandas as pd
import plotly.express as px
from tools import pandashelper
from tools.pathhelper import save_text

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

# ----------------------------------------------------
# Inizializza le variabili necessarie nella sessione
# ----------------------------------------------------
def initialize_session_state():
    session.setdefault("DataFrame", None)
    session.setdefault("Classes", [])
    session.setdefault("IsDataFrameLoaded", False)

# ----------------------------------------------------
# Carica i dati IFC in un DataFrame e aggiorna sessione
# ----------------------------------------------------
def load_data():
    if "ifc_file" not in session or session["ifc_file"] is None:
        st.warning("⚠️ Please upload an IFC file first.")
        return pandashelper.create_empty_dataframe()

    session["Classes"] = []
    df = ifc_props.get_ifc_pandas(session.get("ifc_file"), session.get("ifc_schema", ""))
    session["DataFrame"] = df

    if isinstance(df, pd.DataFrame) and "Class" in df.columns:
        session["Classes"] = df["Class"].value_counts().keys().tolist()
    else:
        session["Classes"] = []
        st.info("Column 'Class' not found — continuing with Property Sets.")

    session["IsDataFrameLoaded"] = True

# ----------------------------------------------------
# Carica i dati IFC in un DataFrame Quantities
# ----------------------------------------------------
def load_quantities():
    session["Classes"] = []
    ifc_file = session.get("ifc_file")
    df = ifc_props.get_ifc_quantities(ifc_file)

    session["QuantitiesFrame"] = df

    if isinstance(df, pd.DataFrame) and "Class" in df.columns:
        session["Classes"] = df["Class"].value_counts().keys().tolist()
    else:
        session["Classes"] = []
        st.info("Column 'Class' not found in Quantities DataFrame.")

    session["IsQuantitiesLoaded"] = True

# ----------------------------------------------------
# Funzioni di download del DataFrame
# ----------------------------------------------------

def download_csv():
    """Return CSV bytes using helper implementation in tools.ifc_prop_qtt."""
    model = session.get('ifc_file')
    df = session.get('DataFrame')
    csv_bytes = None
    try:
        csv_bytes = ifc_props.export_ifc_as_csv_bytes(model=model, df=df)
    except Exception:
        csv_bytes = None

    if csv_bytes:
        return csv_bytes
    else:
        st.error('Unable to generate CSV (see logs).')
        return None


def download_excel():
    pandashelper.download_excel(session.get('file_name'), session.get('QuantitiesFrame'))


# ----------------------------------------------------
# Esecuzione principale dell’app Streamlit
# ----------------------------------------------------
def execute():
    st.set_page_config(page_title="Properties  & QTO", layout="wide", initial_sidebar_state="expanded")
    st.header("📐 Model Properties & Quantities")
    # Breve descrizione della pagina (visibile all'utente in inglese)
    st.markdown(
        """
        This page extracts properties and quantities from the loaded IFC model and provides interactive filters, charts and export options. Use the tabs to inspect the full dataframe, analyze properties per class/type/level, review quantities (QTO) and generate exportable reports.
        """
    )
    
    # Inizializzazione stato
    if "IsDataFrameLoaded" not in session:
        initialize_session_state()
    if not session["IsDataFrameLoaded"]:
        load_data()   # 👈 qui usiamo load_data() perché vogliamo tutto

    if session["IsDataFrameLoaded"]:
        tab1, tab2, tab3, tab4 = st.tabs([
            "🗂️ Dataframe Utilities", 
            "⚙️ Properties Review", 
            "📊 Quantities Review", 
            "📝 Create Report"
        ])

        # ----------------------------------------
        # TAB 1 - Visualizzazione e download
        # ----------------------------------------
        with tab1:
            st.subheader("DataFrame Review")

            if "DataFrame" in session and session["DataFrame"] is not None and not session["DataFrame"].empty:
                # 🔹 Visualizzazione dinamica
                st.dataframe(session["DataFrame"], use_container_width=True)
                # 🔹 Pulsante download CSV (Excel export removed)
                st.download_button(
                    "Download CSV",
                    session["DataFrame"].to_csv(index=False).encode("utf-8"),
                    "full_dataframe.csv",
                    "text/csv"
                )
                if st.button("Save CSV to temp_file", key="btn_save_df_csv"):
                    try:
                        path, url = save_text("full_dataframe.csv", session["DataFrame"].to_csv(index=False))
                        st.success(f"Saved in static/temp_file — {path.name}")
                        st.markdown(f"[Click to download]({url})")
                    except Exception as e:
                        st.error(f"Unable to save: {e}")
            else:
                st.warning("⚠️ No data available. Please load an IFC file first.")


        # ----------------------------------------
        # TAB 2 - Analisi proprietà + Grafico
        # ----------------------------------------
        with tab2:
            if "DataFrame" in session and session["DataFrame"] is not None and not session["DataFrame"].empty:
                df = session["DataFrame"]

                st.subheader("Properties Analysis")

                # 🔹 Filtri con opzione "All"
                col1, col2, col3 = st.columns(3)

                # Order: Level -> Class -> Type
                with col1:
                    level_options = ["All"] + (sorted(df["Level"].dropna().unique().tolist()) if "Level" in df else [])
                    level_filter = st.selectbox("Filter by Level", level_options, key="props_level_filter")
                with col2:
                    class_options = ["All"] + (sorted(df["Class"].dropna().unique().tolist()) if "Class" in df else [])
                    class_filter = st.selectbox("Filter by Class", class_options, key="props_class_filter")
                with col3:
                    # Type options depend on selected class when not All
                    if class_filter != "All" and "Class" in df:
                        type_opts = sorted(df[df["Class"] == class_filter]["Type"].dropna().unique().tolist())
                    else:
                        type_opts = sorted(df["Type"].dropna().unique().tolist()) if "Type" in df else []
                    type_options = ["All"] + type_opts
                    type_filter = st.selectbox("Filter by Type", type_options, key="props_type_filter")

                # 🔹 Applica filtri solo se diverso da "All" (apply Level, then Class, then Type)
                df_filtered = df.copy()
                if level_filter != "All":
                    df_filtered = df_filtered[df_filtered["Level"] == level_filter]
                if class_filter != "All":
                    df_filtered = df_filtered[df_filtered["Class"] == class_filter]
                if type_filter != "All":
                    df_filtered = df_filtered[df_filtered["Type"] == type_filter]

                # Dopo i filtri, dentro tab2
                if df_filtered.empty:
                    st.warning("⚠️ No data available with the selected filters.")
                else:
                    # 🔹 Scelta della proprietà da analizzare
                    # If a specific class is selected, limit properties to columns present for that class
                    if class_filter != "All" and "Class" in df:
                        prop_options = sorted(df[df["Class"] == class_filter].columns.tolist())
                    else:
                        prop_options = sorted(df_filtered.columns.tolist())

                    if not prop_options:
                        st.info("No properties available for the selected class/filters.")
                    else:
                        property_name = st.selectbox("Select property", prop_options, key="props_property_select")

                        if property_name:
                            # Conta frequenze
                            df_report = df_filtered[property_name].value_counts(dropna=False).reset_index()
                            df_report.columns = [property_name, "Count"]

                            st.markdown("Class distribution")
                            st.dataframe(df_report, use_container_width=True)

                            # 🔹 Pulisci il dataframe filtrato
                            df_display = df_filtered.copy()

                            # Rimuovi colonne completamente vuote
                            df_display = df_display.dropna(axis=1, how="all")

                            # Seleziona solo colonne di tipo stringa o booleane
                            df_display = df_display.select_dtypes(include=["object", "bool"])

                            # Se resta qualcosa da mostrare
                            if not df_display.empty:
                                st.markdown("Filtered data")
                                st.dataframe(df_display, use_container_width=True)
                            else:
                                st.info("ℹ️ No descriptive properties available for the selected filters.")

                            # 🔹 Grafico interattivo (includibile nel report)
                            fig = px.bar(
                                df_report,
                                x=property_name,
                                y="Count",
                                title=f"Distribution of {property_name}",
                                text="Count"
                            )
                            fig.update_traces(marker_color=session.get('color1', '#00FFAA'), textposition="outside")
                            st.plotly_chart(fig, use_container_width=True)

                            # Unico bottone: aggiunge al report la tabella visualizzata + il grafico
                            add_key = f"add_filtered_table_{level_filter}_{class_filter}_{type_filter}_{property_name}".replace(" ", "_").replace("/", "_")
                            if st.button("Add current table and chart to report", key=add_key):
                                session.setdefault('report_components', [])
                                session['report_components'].append({
                                    'type': 'property',
                                    'level': level_filter,
                                    'class': class_filter,
                                    'type_filter': type_filter,
                                    'property': property_name,
                                    'data': df_display.copy(),
                                    'fig': fig
                                })
                                st.success("Added current table and chart to report components.")

                            # Rimuove i vecchi salvataggi non utilizzati per evitare confusione
                            session.pop("report_data", None)
                            session.pop("report_fig", None)
            else:
                st.warning("⚠️ No data available. Please load an IFC file first.")

        # ----------------------------------------
        # TAB 3 - Quantities Review
        # ----------------------------------------
        with tab3:
            st.subheader("📐 Quantities Analysis")

            try:
                if "ifc_file" not in session or session["ifc_file"] is None:
                    st.warning("⚠️ No IFC file loaded yet.")
                else:
                    # Carica le quantità dal modello IFC
                    qto_df = ifc_props.get_ifc_quantities(session["ifc_file"])

                    if qto_df.empty:
                        st.warning("⚠️ Quantities DataFrame is empty.")
                    else:
                        # ------------------------------
                        # FILTRI DINAMICI
                        # ------------------------------
                        col1, col2, col3 = st.columns(3)
                        # Order: Level -> Class -> Type (Type depends on Class)
                        with col1:
                            level_options = ["All"] + (sorted(qto_df["Level"].dropna().unique().tolist()) if "Level" in qto_df else [])
                            level_filter = st.selectbox("Filter by Level", level_options, key="qto_level_filter")
                        with col2:
                            class_options = ["All"] + (sorted(qto_df["Class"].dropna().unique().tolist()) if "Class" in qto_df else [])
                            class_filter = st.selectbox("Filter by Class", class_options, key="qto_class_filter")
                        with col3:
                            if class_filter != "All" and "Class" in qto_df:
                                type_opts = sorted(qto_df[qto_df["Class"] == class_filter]["Type"].dropna().unique().tolist())
                            else:
                                type_opts = sorted(qto_df["Type"].dropna().unique().tolist()) if "Type" in qto_df else []
                            type_options = ["All"] + type_opts
                            type_filter = st.selectbox("Filter by Type", type_options, key="qto_type_filter")

                        # Applica i filtri (Level -> Class -> Type)
                        filtered_df = qto_df.copy()
                        if level_filter != "All" and "Level" in filtered_df:
                            filtered_df = filtered_df[filtered_df["Level"] == level_filter]
                        if class_filter != "All" and "Class" in filtered_df:
                            filtered_df = filtered_df[filtered_df["Class"] == class_filter]
                        if type_filter != "All" and "Type" in filtered_df:
                            filtered_df = filtered_df[filtered_df["Type"] == type_filter]

                        # ------------------------------
                        # COLONNE DA MOSTRARE
                        # ------------------------------
                        requested_fixed_cols = ["GlobalId", "Class", "PredefinedType", "Name", "Level", "Type"]
                        fixed_cols = [col for col in requested_fixed_cols if col in filtered_df.columns]
                        numeric_cols = filtered_df.select_dtypes(include=["int64", "float64"]).columns.tolist()
                        cols_to_show = fixed_cols + numeric_cols
                        df_quantities_filtered = filtered_df[cols_to_show] if cols_to_show else filtered_df.copy()

                        # ------------------------------
                        # AGGIUNGI RIGA "TOTAL"
                        # ------------------------------
                        if not df_quantities_filtered.empty:
                            total_row = {
                                col: "TOTAL" if col in fixed_cols else df_quantities_filtered[col].sum()
                                for col in df_quantities_filtered.columns
                            }
                            df_quantities_final = pd.concat(
                                [df_quantities_filtered, pd.DataFrame([total_row])],
                                ignore_index=True
                            )

                            # Mostra tabella
                            st.dataframe(df_quantities_final, use_container_width=True)

                            # Pulsante: aggiungi la tabella delle quantità attualmente visualizzata al report
                            if st.button("Add displayed quantities table to report", key=f"add_qto_table_{class_filter}_{type_filter}_{level_filter}"):
                                session.setdefault('report_components', [])
                                session['report_components'].append({
                                    'type': 'quantity_table',
                                    'level': level_filter,
                                    'class': class_filter,
                                    'type_filter': type_filter,
                                    'data': df_quantities_final.copy(),
                                    'fig': None
                                })
                                st.success("Added displayed quantities table to report components.")

                            # ------------------------------
                            # SOLO SE HO SCELTO UNA CLASSE
                            # ------------------------------
                            if class_filter != "All" and not df_quantities_filtered.empty:
                                st.subheader(f"📊 Distribution for Class: {class_filter}")

                                chart_cols = st.columns(2)

                                # Pie chart TYPE
                                if "Type" in df_quantities_filtered:
                                    with chart_cols[0]:
                                        fig = px.pie(
                                            df_quantities_filtered,
                                            names="Type",
                                            title="Type Distribution"
                                        )
                                        st.plotly_chart(fig, use_container_width=True)

                                # Pie chart LEVEL
                                if "Level" in df_quantities_filtered:
                                    with chart_cols[1]:
                                        fig2 = px.pie(
                                            df_quantities_filtered,
                                            names="Level",
                                            title="Level Distribution"
                                        )
                                        st.plotly_chart(fig2, use_container_width=True)

                            # ------------------------------
                            # Aggiungi ai componenti del report
                            # ------------------------------
                            if numeric_cols:
                                st.markdown("**Add quantities visualization to report**")
                                q_col = st.selectbox("Select numeric quantity to chart/add to report", numeric_cols, key="qto_select_numeric")
                                if q_col:
                                    q_fig = px.bar(
                                        filtered_df.groupby(q_col)[q_col].sum().reset_index(name='Sum'),
                                        x=q_col,
                                        y='Sum',
                                        title=f"Sum by {q_col}"
                                    )
                                    st.plotly_chart(q_fig, use_container_width=True)
                                    if st.button("Add quantities chart to report", key=f"add_qto_report_{q_col}"):
                                        session.setdefault('report_components', [])
                                        summary_df = filtered_df[["GlobalId", "Class", "Name", q_col]].copy() if "GlobalId" in filtered_df.columns else filtered_df[[q_col]].copy()
                                        session['report_components'].append({
                                            'type': 'quantity',
                                            'level': level_filter,
                                            'class': class_filter,
                                            'type_filter': type_filter,
                                            'quantity': q_col,
                                            'data': summary_df,
                                            'fig': q_fig
                                        })
                                        st.success("Added quantities summary to report components.")

                        else:
                            st.info("ℹ️ No quantities available for the selected filters.")

                        st.success(f"✅ Quantities DataFrame loaded: {len(filtered_df)} elements displayed.")

            except Exception as e:
                st.error(f"❌ Error loading Quantities DataFrame: {e}")


        # ----------------------------------------
        # TAB 4 - Report HTML / PDF
        # ----------------------------------------
        with tab4:
            st.subheader("Generate HTML Report")

            # Build report from session['report_components'] when available
            report_components = session.get('report_components', [])

            if not report_components:
                st.info("No report components defined. Use 'Add to report' in Properties or Quantities tabs.")
            else:
                # New: remove all components at once
                if st.button("🗑️ Remove all components", key="remove_all_report_components"):
                    session['report_components'] = []
                    st.success("All components removed from report.")
                    st.stop()

                remove_indices = []
                for i, comp in enumerate(report_components):
                    cols = st.columns([8,1])
                    cols[0].markdown(f"**{i+1}. {comp.get('type').title()}** - {comp.get('property') or comp.get('quantity') or ''}")
                    if cols[1].button("Remove", key=f"remove_comp_{i}"):
                        remove_indices.append(i)

                if remove_indices:
                    for idx in sorted(remove_indices, reverse=True):
                        session['report_components'].pop(idx)
                    st.success("Selected components removed from report.")

                # Compose HTML by iterating components (improved table styling)
                html_parts = []
                for idx, comp in enumerate(report_components):
                    comp_title = f"Component {idx+1}: {comp.get('type').title()}"
                    html_parts.append(f"<h2>{comp_title}</h2>")

                    meta = []
                    if comp.get('level') and comp.get('level') != 'All':
                        meta.append(f"Level: <b>{comp.get('level')}</b>")
                    if comp.get('class') and comp.get('class') != 'All':
                        meta.append(f"Class: <b>{comp.get('class')}</b>")
                    if comp.get('type_filter') and comp.get('type_filter') != 'All':
                        meta.append(f"Type: <b>{comp.get('type_filter')}</b>")
                    if meta:
                        html_parts.append("<p style='color:#666'>" + " • ".join(meta) + "</p>")

                    # Charts FIRST (support single Plotly fig or list of figs)
                    try:
                        figs = comp.get('fig')
                        if figs:
                            if isinstance(figs, list):
                                for f in figs:
                                    try:
                                        plot_html = f.to_html(include_plotlyjs='cdn', full_html=False)
                                        html_parts.append(plot_html)
                                    except Exception:
                                        html_parts.append('<p>Chart unavailable</p>')
                            else:
                                plot_html = figs.to_html(include_plotlyjs='cdn', full_html=False)
                                html_parts.append(plot_html)
                    except Exception:
                        html_parts.append('<p>Chart unavailable</p>')

                    # Table AFTER charts
                    try:
                        table_html = comp['data'].to_html(index=False, na_rep='', classes='tbl')
                    except Exception:
                        table_html = "<p>No table available</p>"
                    html_parts.append(table_html)

                # Improved global HTML structure and CSS
                full_html = """<!doctype html>
                <html>
                <head>
                    <meta charset='utf-8'/>
                    <title>Custom Distribution Report</title>
                    <style>
                        body{font-family: Arial, Helvetica, sans-serif; padding:24px; color:#1f2937;}
                        h1{margin:0 0 8px 0}
                        h2{margin:24px 0 8px 0; color:#111827}
                        .subtitle{color:#6b7280; margin-bottom:20px}
                        table.tbl{width:100%; border-collapse:collapse; font-size:13px;}
                        table.tbl thead th{position:sticky; top:0; background:#f9fafb; color:#111827; text-align:left; border-bottom:1px solid #e5e7eb; padding:8px}
                        table.tbl td{border-bottom:1px solid #f3f4f6; padding:6px; vertical-align:top;}
                        table.tbl tr:nth-child(even){background:#fbfdff}
                        table.tbl tr:hover{background:#eef6ff}
                        .footer{margin-top:24px; color:#9ca3af; font-size:12px}
                    </style>
                </head>
                <body>
                    <h1>Custom Distribution Report</h1>
                    <div class='subtitle'>Generated on: """ + pd.Timestamp.now().strftime('%Y-%m-%d %H:%M') + """</div>
                    """ + "\n".join(html_parts) + """
                    <div class='footer'>End of report</div>
                </body>
                </html>"""

                # Generate only HTML (no PDF)
                if st.button("Generate HTML Report"):
                    session['report_html_content'] = full_html
                    st.success("HTML report generated and ready to download.")
                # Explicit save only on click
                if session.get('report_html_content') and st.button("Save HTML report to temp_file", key="btn_save_props_report_html"):
                    try:
                        path, url = save_text("report_distribution.html", session['report_html_content'])
                        st.success(f"Saved in static/temp_file — {path.name}")
                        st.markdown(f"[Click to download]({url})")
                    except Exception as e:
                        st.error(f"Unable to save: {e}")


# Avvio applicazione
execute()