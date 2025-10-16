import sys
import os
import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
import base64
import ifcopenshell as ifc
from tools import ifchelper, pandashelper, graph_maker
from tools.ifchelper import get_ifc_quantities


# Import helpers
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Alias per la sessione Streamlit
session = st.session_state

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
        st.warning("⚠️ Please upload an IFC file first in the sidebar.")
        return pandashelper.create_empty_dataframe()

    session["Classes"] = []
    df = get_ifc_pandas()
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
    ifc_file = session.get("ifc_file")   # recupera il file IFC dalla sessione
    df = get_ifc_quantities(ifc_file)    # passa il file come argomento

    session["QuantitiesFrame"] = df

    if isinstance(df, pd.DataFrame) and "Class" in df.columns:
        session["Classes"] = df["Class"].value_counts().keys().tolist()
    else:
        session["Classes"] = []
        st.info("Column 'Class' not found in Quantities DataFrame.")

    session["IsQuantitiesLoaded"] = True

# ----------------------------------------------------
# Estrae i dati dal file IFC e costruisce un DataFrame
# ----------------------------------------------------
def get_ifc_pandas():
    schema = session.get("ifc_schema", "").upper()

    try:
        classes_by_schema = {
            "IFC2X3": [
                "IfcBeam", "IfcColumn", "IfcSlab", "IfcWall", "IfcWallStandardCase",
                "IfcFooting", "IfcMember", "IfcReinforcingBar", "IfcReinforcingMesh",
                "IfcTendon", "IfcTendonAnchor", "IfcStructuralConnection",
                "IfcStructuralCurveMember", "IfcStructuralSurfaceMember",
                "IfcRamp", "IfcStair"
            ],
            "IFC4": [
                "IfcBeam", "IfcColumn", "IfcSlab", "IfcWall", "IfcWallStandardCase",
                "IfcFooting", "IfcMember", "IfcReinforcingBar", "IfcReinforcingMesh",
                "IfcTendon", "IfcTendonAnchor", "IfcStructuralConnection",
                "IfcStructuralCurveMember", "IfcStructuralSurfaceMember",
                "IfcRamp", "IfcStair"
            ],
            "IFC4X3": [
                "IfcBeam", "IfcColumn", "IfcSlab", "IfcWall", "IfcWallStandardCase",
                "IfcFooting", "IfcMember", "IfcReinforcingBar", "IfcReinforcingMesh",
                "IfcTendon", "IfcTendonAnchor", "IfcStructuralConnection",
                "IfcStructuralCurveMember", "IfcStructuralSurfaceMember",
                "IfcRamp", "IfcStair", "IfcBearing"
            ]
        }

        target_classes = classes_by_schema.get(schema, classes_by_schema["IFC4"])
        dfs = []

        for cls in target_classes:
            try:
                data, pset = ifchelper.get_objects_data_by_class(session["ifc_file"], cls)
                df = ifchelper.create_pandas_dataframe(data, pset)
                if not df.empty:
                    df["Class"] = cls
                    dfs.append(df)
            except Exception as e:
                st.warning(f"⚠️ Error loading class {cls}: {e}")

        if not dfs:
            st.warning("No structural objects found in the IFC file.")
            return pandashelper.create_empty_dataframe()

        df_all = pd.concat(dfs, ignore_index=True)
        return df_all

    except Exception as e:
        st.error(f"❌ Error while extracting IFC data: {e}")
        return pandashelper.create_empty_dataframe()

# ----------------------------------------------------
# Estrae i Quantities dal file IFC e costruisce DataFrame
# ----------------------------------------------------
def get_ifc_quantities(model) -> pd.DataFrame:
    """
    Estrae tutte le Quantity Sets (Qto) dal modello IFC e le restituisce in un DataFrame.

    Colonne principali:
    - GlobalId
    - Class
    - Type
    - Level
    - Qto_XXX.Quantity
    """
    records = []

    for element in model.by_type("IfcProduct"):
        # Evita entità senza rappresentazione geometrica
        if not hasattr(element, "IsDefinedBy"):
            continue

        row = {
            "GlobalId": element.GlobalId,
            "Class": element.is_a(),
            "Type": None,
            "Level": None,
        }

        # Tipo (se disponibile)
        if hasattr(element, "ObjectType") and element.ObjectType:
            row["Type"] = str(element.ObjectType)

        # Level (If RelatingObject -> IfcBuildingStorey)
        try:
            for rel in getattr(element, "ContainedInStructure", []):
                if rel.RelatingStructure.is_a("IfcBuildingStorey"):
                    row["Level"] = rel.RelatingStructure.Name
        except:
            pass

        # Leggo tutte le quantità nei Qto
        try:
            psets = ifc.util.element.get_psets(element, qtos_only=True)
            for qset, quantities in psets.items():
                for qname, qvalue in quantities.items():
                    row[f"{qset}.{qname}"] = qvalue
        except:
            continue

        records.append(row)

    if not records:
        return pd.DataFrame()

    df = pd.DataFrame(records)

    # Riordino le colonne (alfabetico dopo quelle principali)
    base_cols = ["GlobalId", "Class", "Type", "Level"]
    other_cols = sorted([c for c in df.columns if c not in base_cols])
    df = df[base_cols + other_cols]

    return df

# ----------------------------------------------------
# Funzioni di download del DataFrame
# ----------------------------------------------------
def download_csv():
    pandashelper.download_csv(session["file_name"], session["QuantitiesFrame"])

def download_excel():
    pandashelper.download_excel(session["file_name"], session["QuantitiesFrame"])


# ----------------------------------------------------
# Esecuzione principale dell’app Streamlit
# ----------------------------------------------------
def execute():
    st.set_page_config(page_title="Properties  & QTO", layout="wide", initial_sidebar_state="expanded")
    st.header("📐 Model Properties & Quantities")
    st.text("Explore the model properties, quantities and generate reports.")

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
                st.dataframe(session["DataFrame"], width="stretch")   # instead of use_container_width=True
                # 🔹 Pulsante download CSV
                st.download_button(
                    "Download CSV",
                    session["DataFrame"].to_csv(index=False).encode("utf-8"),
                    "full_dataframe.csv",
                    "text/csv"
                )

                # 🔹 Pulsante download Excel
                from io import BytesIO
                buffer = BytesIO()
                session["DataFrame"].to_excel(buffer, index=False, engine="xlsxwriter")
                buffer.seek(0)

                st.download_button(
                    "Download Excel",
                    buffer,
                    "full_dataframe.xlsx",
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
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

                with col1:
                    class_filter = st.selectbox("Filter by Class", ["All"] + sorted(df["Class"].dropna().unique().tolist()))
                with col2:
                    level_filter = st.selectbox("Filter by Level", ["All"] + sorted(df["Level"].dropna().unique().tolist()))
                with col3:
                    type_filter = st.selectbox("Filter by Type", ["All"] + sorted(df["Type"].dropna().unique().tolist()))

                # 🔹 Applica filtri solo se diverso da "All"
                df_filtered = df.copy()
                if class_filter != "All":
                    df_filtered = df_filtered[df_filtered["Class"] == class_filter]
                if level_filter != "All":
                    df_filtered = df_filtered[df_filtered["Level"] == level_filter]
                if type_filter != "All":
                    df_filtered = df_filtered[df_filtered["Type"] == type_filter]

                # Dopo i filtri, dentro tab2
                if df_filtered.empty:
                    st.warning("⚠️ No data available with the selected filters.")
                else:
                    # 🔹 Scelta della proprietà da analizzare
                    property_name = st.selectbox("Select property/column", sorted(df_filtered.columns))

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
                            st.dataframe(df_display, width="stretch")
                        else:
                            st.info("ℹ️ No descriptive properties available for the selected filters.")

                        # 🔹 Grafico interattivo
                        fig = px.bar(
                            df_report,
                            x=property_name,
                            y="Count",
                            title=f"Distribution of {property_name}",
                            text="Count"
                        )
                        fig.update_traces(textposition="outside")
                        st.plotly_chart(fig, width="content")  # instead of use_container_width=False

                        # 🔹 Salvo i risultati in sessione per export/report
                        session["report_data"] = df_report
                        session["report_fig"] = fig
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
                    qto_df = get_ifc_quantities(session["ifc_file"])

                    if qto_df.empty:
                        st.warning("⚠️ Quantities DataFrame is empty.")
                    else:
                        # ------------------------------
                        # FILTRI DINAMICI
                        # ------------------------------
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            class_filter = st.selectbox(
                                "Filter by Class", ["All"] + sorted(qto_df["Class"].dropna().unique().tolist())
                                if "Class" in qto_df else ["All"]
                            )
                        with col2:
                            level_filter = st.selectbox(
                                "Filter by Level", ["All"] + sorted(qto_df["Level"].dropna().unique().tolist())
                                if "Level" in qto_df else ["All"]
                            )
                        with col3:
                            type_filter = st.selectbox(
                                "Filter by Type", ["All"] + sorted(qto_df["Type"].dropna().unique().tolist())
                                if "Type" in qto_df else ["All"]
                            )

                        # Applica i filtri
                        filtered_df = qto_df.copy()
                        if class_filter != "All" and "Class" in filtered_df:
                            filtered_df = filtered_df[filtered_df["Class"] == class_filter]
                        if level_filter != "All" and "Level" in filtered_df:
                            filtered_df = filtered_df[filtered_df["Level"] == level_filter]
                        if type_filter != "All" and "Type" in filtered_df:
                            filtered_df = filtered_df[filtered_df["Type"] == type_filter]

                        # ------------------------------
                        # COLONNE DA MOSTRARE
                        # ------------------------------
                        requested_fixed_cols = ["GlobalId", "Class", "PredefinedType", "Name", "Level", "Type"]
                        fixed_cols = [col for col in requested_fixed_cols if col in filtered_df.columns]
                        numeric_cols = filtered_df.select_dtypes(include=["int64", "float64"]).columns.tolist()
                        cols_to_show = fixed_cols + numeric_cols
                        df_quantities_filtered = filtered_df[cols_to_show]

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
                            st.dataframe(df_quantities_final, width="stretch")

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
                                        st.plotly_chart(fig, width="content")  # instead of use_container_width=False

                                # Pie chart LEVEL
                                if "Level" in df_quantities_filtered:
                                    with chart_cols[1]:
                                        fig = px.pie(
                                            df_quantities_filtered,
                                            names="Level",
                                            title="Level Distribution"
                                        )
                                        st.plotly_chart(fig, width="content")  # instead of use_container_width=False

                        else:
                            st.info("ℹ️ No quantities available for the selected filters.")

                        st.success(f"✅ Quantities DataFrame loaded: {len(filtered_df)} elements displayed.")

            except Exception as e:
                st.error(f"❌ Error loading Quantities DataFrame: {e}")


        # ----------------------------------------
        # TAB 4 - Report PDF
        # ----------------------------------------
        with tab4:
            if "report_data" in st.session_state:
                st.subheader("Generate Report")

                df_report = st.session_state["report_data"]
                fig = st.session_state["report_fig"]

                if st.button("Generate PDF Report"):
                    try:
                        charts = [fig]  # lista di grafici Plotly
                        output_path = pandashelper.create_distribution_report(
                            df_report,
                            charts=charts,
                            output_path="report_distribution.pdf",
                            logo_path="assets/logo.png"  # 🔹 Inserisci qui il tuo logo se serve
                        )

                        # 🔹 Leggi il file PDF come base64 per mostrarlo in anteprima
                        with open(output_path, "rb") as f:
                            base64_pdf = base64.b64encode(f.read()).decode("utf-8")

                        pdf_display = f"""
                        <iframe src="data:application/pdf;base64,{base64_pdf}" 
                                width="100%" height="800" type="application/pdf">
                        </iframe>
                        """
                        st.markdown(pdf_display, unsafe_allow_html=True)

                        # 🔹 Pulsante di download sotto l'anteprima
                        with open(output_path, "rb") as f:
                            st.download_button(
                                label="📥 Download PDF Report",
                                data=f,
                                file_name=os.path.basename(output_path),
                                mime="application/pdf",
                            )

                    except Exception as e:
                        st.error(f"❌ Failed to generate the report: {e}")

# Avvio applicazione
execute()