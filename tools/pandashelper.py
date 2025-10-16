import io
import os
import streamlit as st
import pandas as pd
from fpdf import FPDF
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image, Spacer, PageBreak
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
import matplotlib.pyplot as plt
import tempfile
import plotly.io as pio

session = st.session_state

# ===============================================================
# Costanti principali del DataFrame
# ===============================================================
CLASS = "Class"
LEVEL = "Level"


# -------------------------------------------------------------------
# Filtra il DataFrame per una specifica classe IFC
# Richiamata in: Model Quantities
# -------------------------------------------------------------------
def filter_dataframe_per_class(dataframe, class_name):
    return dataframe[dataframe[CLASS] == class_name].dropna(axis=1, how="all")


# -------------------------------------------------------------------
# Calcola il numero totale di oggetti nel DataFrame
# Richiamata in: Model Properties
# -------------------------------------------------------------------
def get_total(dataframe):
    return dataframe[CLASS].value_counts().sum()


# -------------------------------------------------------------------
# Estrae tutti i Quantity Sets presenti nel DataFrame
# Richiamata in: Model Properties (tab 2 - Analisi proprietà)
# -------------------------------------------------------------------
def get_qsets_columns(df: pd.DataFrame):
    if df is None or df.empty:
        return []

    qsets = {col.split(".")[0] for col in df.columns if "." in col}

    if "ManualQuantities" in df.columns or any(c.startswith("ManualQuantities.") for c in df.columns):
        qsets.add("ManualQuantities")

    return sorted(qsets)


# -------------------------------------------------------------------
# Estrae tutti i Property Sets presenti nel DataFrame
# Richiamata in: Model Properties
# -------------------------------------------------------------------
def get_psets_columns(df: pd.DataFrame) -> list:
    if df is None or df.empty:
        return []
    psets = {col.split(".")[0] for col in df.columns if col.startswith("Pset_")}
    return sorted(list(psets))


# -------------------------------------------------------------------
# Restituisce tutte le quantità disponibili in un certo Quantity Set
# Richiamata in: Model Quantities
# -------------------------------------------------------------------
def get_quantities(df: pd.DataFrame, qset: str):
    if df is None or df.empty:
        return []
    return sorted({col.split(".")[1] for col in df.columns if col.startswith(f"{qset}.")})


# -------------------------------------------------------------------
# Esporta il DataFrame come Excel (download via Streamlit)
# Richiamata in: Model Quantities, Report tab
# -------------------------------------------------------------------
def download_excel_button(file_name, df):
    if df is None or df.empty:
        st.warning("⚠️ No dataframe available for export.")
        return

    buffer = io.BytesIO()
    df.to_excel(buffer, index=False, engine="openpyxl")
    buffer.seek(0)

    st.download_button(
        label="📥 Download Excel",
        data=buffer,
        file_name=f"{file_name}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


# -------------------------------------------------------------------
# Esporta il DataFrame come Excel (un foglio per classe, salvataggio su file)
# Richiamata in: Create Report
# -------------------------------------------------------------------
def download_excel_file(file_name, dataframe):
    file_name = file_name.replace('.ifc', '.xlsx')
    os.makedirs("./downloads", exist_ok=True)
    writer = pd.ExcelWriter(f'./downloads/{file_name}', engine="xlsxwriter")
    for object_class in dataframe[CLASS].unique():
        df_class = dataframe[dataframe[CLASS] == object_class].dropna(axis=1, how="all")
        df_class.to_excel(writer, sheet_name=object_class)
    writer.close()


# -------------------------------------------------------------------
# Restituisce un DataFrame vuoto
# Richiamata in: inizializzazione sessione
# -------------------------------------------------------------------
def create_empty_dataframe():
    return pd.DataFrame()


# ------------------------------------------------------------------- 
# Crea un report PDF delle distribuzioni con tabella + grafici Plotly
# Richiamata in: Create Report
# -------------------------------------------------------------------
def create_distribution_report(df, charts, output_path="distribution_report.pdf", logo_path=None):
    """
    Genera un PDF con tabella delle proprietà e grafici di distribuzione.
    """

    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image, Spacer
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from datetime import datetime
    import plotly.io as pio
    import io
    import os

    # Inizializza documento PDF
    doc = SimpleDocTemplate(output_path, pagesize=A4)
    elements = []

    # Stili
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="CenterTitle", alignment=1, fontSize=16, spaceAfter=20, leading=20))
    styles.add(ParagraphStyle(name="SectionHeading", fontSize=12, spaceAfter=10, leading=14))

    # -----------------------------------
    # LOGO
    # -----------------------------------
    if logo_path and os.path.exists(logo_path):
        elements.append(Image(logo_path, width=120, height=60))
        elements.append(Spacer(1, 12))

    # -----------------------------------
    # TITOLO
    # -----------------------------------
    elements.append(Paragraph("📊 MODEL DISTRIBUTION REPORT", styles["CenterTitle"]))
    gen_date = datetime.now().strftime("%Y-%m-%d %H:%M")
    elements.append(Paragraph(f"<i>Generated on: {gen_date}</i>", styles["Normal"]))
    elements.append(Spacer(1, 20))

    # -----------------------------------
    # TABELLA DATI
    # -----------------------------------
    if not df.empty:
        table_data = [df.columns.tolist()] + df.values.tolist()
        table = Table(table_data)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
            ("GRID", (0, 0), (-1, -1), 0.25, colors.black),
        ]))
        elements.append(Paragraph("Properties Table", styles["SectionHeading"]))
        elements.append(table)
        elements.append(Spacer(1, 20))

    # -----------------------------------
    # GRAFICI PLOTLY
    # -----------------------------------
    for idx, fig in enumerate(charts, 1):
        img_bytes = io.BytesIO()
        pio.write_image(fig, img_bytes, format="png", scale=2)  # requires kaleido
        img_bytes.seek(0)

        elements.append(Paragraph(f"Distribution Chart {idx}", styles["SectionHeading"]))
        elements.append(Image(img_bytes, width=450, height=250))
        elements.append(Spacer(1, 20))

    # -----------------------------------
    # CREA PDF
    # -----------------------------------
    doc.build(elements)
    return output_path