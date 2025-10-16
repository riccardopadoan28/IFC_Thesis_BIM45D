from tools import ifchelper
import plotly.express as px
import pandas as pd

# ========================================================
# 🎨 Stile matplotlib dark mode
# ========================================================
style = {
    "figure.figsize": (8, 4.5),
    "axes.facecolor": (0.0, 0.0, 0.0, 0),
    "axes.edgecolor": "white",
    "axes.labelcolor": "white",
    "figure.facecolor": (0.0, 0.0, 0.0, 0),
    "savefig.facecolor": (0.0, 0.0, 0.0, 0),
    "patch.edgecolor": "#0e1117",
    "text.color": "white",
    "xtick.color": "white",
    "ytick.color": "white",
    "grid.color": "white",
    "font.size": 12,
    "axes.labelsize": 12,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
}

# ========================================================
# 📈 Grafico: Conteggio elementi di IfcBuildingElement
# ========================================================
def get_elements_graph(file, color="#00FFAA", title="Building Objects Count"):
    types = ifchelper.get_types(file, "IfcBuildingElement")
    types_count = ifchelper.get_type_occurence(file, types)
    x_values, y_values = ifchelper.get_x_and_y(types_count)

    if not x_values or not y_values:
        fig = px.bar(title=title)
        fig.add_annotation(
            text="No building elements found.",
            xref="paper", yref="paper", showarrow=False,
            font=dict(color="white", size=14)
        )
        return fig

    df = pd.DataFrame({"Element Class": x_values, "Count": y_values})
    fig = px.bar(
        df,
        x="Element Class",
        y="Count",
        title=title,
        color_discrete_sequence=[color]
    )

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        xaxis_tickangle=-45,
        margin=dict(l=40, r=20, t=50, b=100)
    )

    return fig

# ========================================================
# 📊 Grafico: Entità con occorrenza superiore a soglia
# ========================================================
def get_high_frequency_entities_graph(
    file, threshold=400, color="#FF3333", title="IFC Entity Types Frequency"
):
    types = ifchelper.get_types(file)
    types_count = ifchelper.get_type_occurence(file, types)
    x_values, y_values = ifchelper.get_x_and_y(types_count, higher_then=threshold)

    if not x_values or not y_values:
        fig = px.bar(title=title)
        fig.add_annotation(
            text="No entities above threshold.",
            xref="paper", yref="paper", showarrow=False,
            font=dict(color="white", size=14)
        )
        return fig

    df = pd.DataFrame({"File Entities": x_values, "No. of Occurrences": y_values})
    fig = px.bar(
        df,
        x="File Entities",
        y="No. of Occurrences",
        title=title,
        color_discrete_sequence=[color]
    )

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        xaxis_tickangle=-45,
        margin=dict(l=40, r=20, t=50, b=100)
    )

    return fig

# ========================================================
# 🧮 Grafico a torta per QuantitySet (Plotly Pie Chart)
# ========================================================
def load_graph(dataframe, quantity_set, quantity, user_option, title=None, color_discrete_sequence=None):
    """
    Crea un grafico a torta (pie chart) per una determinata quantity del Qto selezionato.

    Args:
        dataframe: DataFrame filtrato
        quantity_set: Nome del QuantitySet (es. QtoWallBaseQuantities)
        quantity: Nome della quantity (es. Length, Width)
        user_option: Colonna su cui raggruppare i dati (es. "Level", "Type")
        title: Titolo del grafico (opzionale)
        color_discrete_sequence: Lista di colori per le fette (opzionale)
    """
    if quantity != "Count":
        column_name = f"{quantity_set}.{quantity}"
        figure_pie_chart = px.pie(
            dataframe,
            names=user_option,
            values=column_name,
            title=title,
            color_discrete_sequence=color_discrete_sequence or px.colors.sequential.Reds,
        )
        # Aggiungi questa riga per mostrare percentuale + valore assoluto
        figure_pie_chart.update_traces(textinfo='percent+value')
        return figure_pie_chart
