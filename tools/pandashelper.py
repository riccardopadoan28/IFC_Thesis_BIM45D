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
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Table, TableStyle
from datetime import datetime
from PIL import Image

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


def create_distribution_report(df_report, charts=None, output_path="report_distribution.pdf", logo_path=None, operator_name=None, title="Distribution Report", include_session_data=False):
    """Crea un PDF ben formattato contenente:
    - header con logo, titolo, operator e data
    - breve descrizione (brief)
    - grafici (forniti come oggetti plotly in charts)
    - tabella di report (df_report)
    - sommario delle proprietà e delle quantità prese dalla sessione Streamlit se presenti
    - numeri di pagina

    Restituisce il percorso del file PDF generato.
    """
    session = None
    try:
        import streamlit as st
        session = st.session_state
    except Exception:
        session = {}

    # Parametri layout
    page_width, page_height = A4
    margin = 20 * mm
    usable_width = page_width - 2 * margin

    c = canvas.Canvas(output_path, pagesize=A4)
    page_num = 0

    # Helper per disegnare header
    def draw_header(canv, title_text):
        nonlocal page_num
        page_num += 1
        # Logo
        x = margin
        y = page_height - margin
        if logo_path:
            try:
                img = Image.open(logo_path)
                img.thumbnail((120, 60))
                img_buf = io.BytesIO()
                img.save(img_buf, format='PNG')
                img_buf.seek(0)
                canv.drawImage(ImageReader(img_buf), x, y - 60, width=120, height=60, preserveAspectRatio=True, mask='auto')
            except Exception:
                pass
        # Title and metadata
        canv.setFont("Helvetica-Bold", 16)
        canv.drawString(x + 140, y - 10, title_text)
        canv.setFont("Helvetica", 9)
        op = operator_name or (session.get('operator_name') if isinstance(session, dict) else None) or "Unknown Operator"
        date_str = datetime.now().strftime('%Y-%m-%d %H:%M')
        canv.drawString(x + 140, y - 26, f"Operator: {op}")
        canv.drawString(x + 140, y - 40, f"Generated: {date_str}")
        # Brief
        canv.setFont("Helvetica", 10)
        brief = "Automated distribution report: includes property distribution and quantities with charts."
        canv.drawString(x, y - 80, brief)

    # Helper per footer con numero pagina
    def draw_footer(canv):
        canv.setFont("Helvetica", 8)
        canv.setFillColor(colors.grey)
        canv.drawString(margin, 12 * mm, f"Page {page_num}")
        canv.setFillColor(colors.black)

    # 1) Page: cover / brief
    draw_header(c, title)
    c.setFont("Helvetica", 11)
    c.drawString(margin, page_height - margin - 110, "Brief:")
    c.setFont("Helvetica", 10)
    c.drawString(margin, page_height - margin - 124, "This PDF report summarizes the property distribution and quantities extracted from the IFC model.")
    draw_footer(c)
    c.showPage()

    # 2) Charts page(s)
    if charts:
        for fig in charts:
            draw_header(c, title)
            try:
                # Convert plotly fig to PNG bytes
                img_bytes = fig.to_image(format='png', width=1000, height=500)
                img_buf = io.BytesIO(img_bytes)
                img = Image.open(img_buf)
                iw, ih = img.size
                max_w = usable_width
                max_h = page_height - margin - 120 * mm
                # scale to fit
                scale = min(max_w / iw, (page_height - 2 * margin - 80) / ih)
                draw_w = iw * scale
                draw_h = ih * scale
                x = (page_width - draw_w) / 2
                y = (page_height - margin - draw_h - 60)
                c.drawImage(ImageReader(img_buf), x, y, width=draw_w, height=draw_h)
            except Exception:
                c.setFont("Helvetica", 10)
                c.drawString(margin, page_height - margin - 120, "Chart unavailable")
            draw_footer(c)
            c.showPage()

    # 3) Report table page(s) for df_report
    if df_report is not None and not df_report.empty:
        # Pagina con tabella (split in più pagine se necessario)
        rows_per_page = 25
        cols = list(df_report.columns)
        data_rows = [cols] + df_report.values.tolist()

        # Chunk rows
        for start in range(0, len(data_rows) - 1, rows_per_page):
            draw_header(c, title)
            table_chunk = data_rows[start:start + rows_per_page + 1]
            table = Table(table_chunk, colWidths=[usable_width / max(1, len(cols))] * len(cols))
            style = TableStyle([
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
            ])
            table.setStyle(style)
            w, h = table.wrapOn(c, usable_width, page_height - 2 * margin)
            table.drawOn(c, margin, page_height - margin - 140 - h)
            draw_footer(c)
            c.showPage()

    # 4) Properties and Quantities summaries from session if requested
    if include_session_data:
        try:
            df_props = None
            df_qto = None
            if isinstance(session, dict):
                df_props = session.get('DataFrame')
                df_qto = session.get('QuantitiesFrame')
            else:
                df_props = session.get('DataFrame') if 'DataFrame' in session else None
                df_qto = session.get('QuantitiesFrame') if 'QuantitiesFrame' in session else None

            if df_props is not None and not df_props.empty:
                # show a head summary (first 50 rows) across pages
                sample = df_props.head(50)
                cols = list(sample.columns)
                data_rows = [cols] + sample.values.tolist()
                rows_per_page = 25
                for start in range(0, len(data_rows) - 1, rows_per_page):
                    draw_header(c, "Properties - Sample")
                    table_chunk = data_rows[start:start + rows_per_page + 1]
                    table = Table(table_chunk, colWidths=[usable_width / max(1, len(cols))] * len(cols))
                    table.setStyle(TableStyle([
                        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                        ("FONTSIZE", (0, 0), (-1, -1), 7),
                    ]))
                    w, h = table.wrapOn(c, usable_width, page_height - 2 * margin)
                    table.drawOn(c, margin, page_height - margin - 140 - h)
                    draw_footer(c)
                    c.showPage()

            if df_qto is not None and not df_qto.empty:
                sample = df_qto.head(50)
                cols = list(sample.columns)
                data_rows = [cols] + sample.values.tolist()
                rows_per_page = 25
                for start in range(0, len(data_rows) - 1, rows_per_page):
                    draw_header(c, "Quantities - Sample")
                    table_chunk = data_rows[start:start + rows_per_page + 1]
                    table = Table(table_chunk, colWidths=[usable_width / max(1, len(cols))] * len(cols))
                    table.setStyle(TableStyle([
                        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                        ("FONTSIZE", (0, 0), (-1, -1), 7),
                    ]))
                    w, h = table.wrapOn(c, usable_width, page_height - 2 * margin)
                    table.drawOn(c, margin, page_height - margin - 140 - h)
                    draw_footer(c)
                    c.showPage()
        except Exception:
            pass

    # Finalizza PDF
    c.save()
    return output_path