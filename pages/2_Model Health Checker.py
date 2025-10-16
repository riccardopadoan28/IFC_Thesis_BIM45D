import streamlit as st
from tools import ifchelper, graph_maker, pandashelper
from datetime import datetime
import ifcopenshell as ifc
import plotly.express as px
import base64

# Alias per accesso rapido allo stato di sessione
session = st.session_state

# =============================================================================
# 🔁 Inizializzazione dello stato della sessione
# =============================================================================
def initialize_session_state():
    session["isHealthDataLoaded"] = False
    session["HealthData"] = {}
    session["Graphs"] = {}
    session["SequenceData"] = {}
    session["CostScheduleData"] = {}
    session['summary_stats'] = None

# =============================================================================
# 📊 Caricamento dati e calcolo di TUTTE le statistiche
# =============================================================================
def load_data():
    if "ifc_file" in session:
        # --- PART 1: Dati per il Grafico di Sinistra (Elementi Strutturali) ---
        classes_by_schema = {
            "IFC2X3": ["IfcBeam", "IfcColumn", "IfcSlab", "IfcWall", "IfcWallStandardCase", "IfcFooting", "IfcMember", "IfcReinforcingBar", "IfcReinforcingMesh", "IfcTendon", "IfcTendonAnchor", "IfcStructuralConnection", "IfcStructuralCurveMember", "IfcStructuralSurfaceMember", "IfcRamp", "IfcStair"],
            "IFC4": ["IfcBeam", "IfcColumn", "IfcSlab", "IfcWall", "IfcWallStandardCase", "IfcFooting", "IfcMember", "IfcReinforcingBar", "IfcReinforcingMesh", "IfcTendon", "IfcTendonAnchor", "IfcStructuralConnection", "IfcStructuralCurveMember", "IfcStructuralSurfaceMember", "IfcRamp", "IfcStair"],
            "IFC4X3": ["IfcBeam", "IfcColumn", "IfcSlab", "IfcWall", "IfcWallStandardCase", "IfcFooting", "IfcMember", "IfcReinforcingBar", "IfcReinforcingMesh", "IfcTendon", "IfcTendonAnchor", "IfcStructuralConnection", "IfcStructuralCurveMember", "IfcStructuralSurfaceMember", "IfcRamp", "IfcStair", "IfcBearing"]
        }
        schema = session.ifc_file.schema
        target_classes = classes_by_schema.get(schema, classes_by_schema["IFC4"])

        structural_counts = {cls: len(session.ifc_file.by_type(cls)) for cls in target_classes}
        structural_counts = {k: v for k, v in structural_counts.items() if v > 0}
        structural_sorted = sorted(structural_counts.items(), key=lambda item: item[1], reverse=True)

        # --- PART 2: Dati per il Grafico di Destra (Tutte le Entità) ---
        all_entity_counts = {}
        for entity in session.ifc_file:
            class_name = entity.is_a()
            all_entity_counts[class_name] = all_entity_counts.get(class_name, 0) + 1
        
        all_entity_sorted = sorted(all_entity_counts.items(), key=lambda item: item[1], reverse=True)

        # ❗ CORREZIONE: Salva TUTTE le statistiche necessarie per evitare il KeyError
        total_structural_objects = sum(structural_counts.values())
        num_property_sets = all_entity_counts.get('IfcPropertySet', 0)
        property_ratio = num_property_sets / total_structural_objects if total_structural_objects > 0 else 0

        session['summary_stats'] = {
            'total': total_structural_objects,
            'types': len(structural_counts),
            'most_common_name': structural_sorted[0][0] if structural_sorted else "N/A",
            'most_common_count': structural_sorted[0][1] if structural_sorted else 0,
            'least_common_name': structural_sorted[-1][0] if structural_sorted else "N/A",
            'least_common_count': structural_sorted[-1][1] if structural_sorted else 0,
            'num_property_sets': num_property_sets,
            'property_ratio': property_ratio
        }

        # --- PART 3: Creazione Grafici ---
        fig1 = px.bar(
            x=[item[0] for item in structural_sorted], y=[item[1] for item in structural_sorted], 
            title="Building Objects Count", labels={'x': 'Element Class', 'y': 'Count'}
        )
        fig1.update_traces(marker_color=session.get("color1", "#00FFAA"))

        top_n = 10
        fig2 = px.bar(
            x=[item[0] for item in all_entity_sorted[:top_n]], y=[item[1] for item in all_entity_sorted[:top_n]], 
            title=f"Top {top_n} IFC Entity Types Frequency", labels={'x': 'File Entities', 'y': 'No. of Occurrences'}
        )
        fig2.update_traces(marker_color=session.get("color2", "#FF3333"))

        session["Graphs"] = {"objects_graph": fig1, "high_frquency_graph": fig2}
        session["isHealthDataLoaded"] = True

# =============================================================================
# 📈 Visualizzazione del riepilogo unificato
# =============================================================================
def draw_content():
    # Disegna i grafici
    row1_col1, row1_col2 = st.columns(2)
    with row1_col1:
        st.plotly_chart(session.Graphs["objects_graph"], use_container_width=True)
    with row1_col2:
        st.plotly_chart(session.Graphs["high_frquency_graph"], use_container_width=True)

    st.markdown("---") 

    # Sezione di analisi che unisce i dati originali e l'analisi di correlazione
    st.subheader("📝 Automated Analysis and Model Health")
    stats = session.get('summary_stats')
    
    # Controllo sicuro per evitare errori se 'stats' non è ancora stato popolato
    if stats and stats['total'] > 0:
        summary_text = f"""
        The analysis focuses on the **{stats['types']} structural element classes** found in the model, totaling **{stats['total']} objects** (visible in the **Left Chart**).

        - The most frequent element is **`{stats['most_common_name']}`** with **{stats['most_common_count']}** instances.
        - The least frequent element is **`{stats['least_common_name']}`** with only **{stats['least_common_count']}** instances.
        """
        st.markdown(summary_text)

        st.markdown("---")
        
        st.markdown(f"""
        **Correlation and Data Richness**: A BIM model's health depends on its data richness. Each physical object is described by data entities (the most common are in the **Right Chart**).
        In this file, **{stats['num_property_sets']}** property set containers (`IfcPropertySet`) were found. 
        This translates to an average of **{stats['property_ratio']:.2f} 'property sets' for each structural object**.
        """)

        if stats['property_ratio'] >= 2.0:
            st.success("**Verdict**: The model is **data-rich**. A high ratio of properties to objects indicates that the elements are well-described and informative.")
        elif stats['property_ratio'] >= 1.0:
            st.info("**Verdict**: The model is **moderately detailed**. Most objects have basic data, but there is room for data enrichment.")
        else:
            st.warning("**Verdict**: The model is **geometrically simple**. A low ratio suggests that many objects may be missing crucial data, potentially being a 'dumb model'.")
    
    else:
        st.warning("No structural elements were found to generate an analysis.")

# =============================================================================
# 🧠 Debug: Inizializzazione struttura per proprietà BIM
# =============================================================================
def initialise_debug_props(force=False):
    default_props = {
        "step_id": 0, "number_of_polygons": 0, "percentile_of_polygons": 0,
        "active_step_id": 0, "step_id_breadcrumb": [], "attributes": [],
        "inverse_attributes": [], "inverse_references": [], "express_file": None,
    }
    if "BIMDebugProperties" not in session or force:
        session["BIMDebugProperties"] = default_props.copy()

# =============================================================================
# 🔍 Estrazione dati oggetto da ID 
# =============================================================================
def get_object_data(fromId=None):
    def add_attribute(prop_list, key, value):
        if isinstance(value, tuple):
            if len(value) < 10:
                for i, item in enumerate(value):
                    add_attribute(prop_list, f"{key}[{i}]", item)
                return
            else:
                key = f"{key}({len(value)})"
        prop = {
            "name": key,
            "string_value": str(value),
            "int_value": int(value.id()) if isinstance(value, ifc.entity_instance) else None,
        }
        prop_list.append(prop)

    initialise_debug_props(force=True)
    step_id = fromId or int(session.get("object_id", 0))
    debug_props = session["BIMDebugProperties"]
    debug_props["active_step_id"] = step_id
    debug_props["step_id_breadcrumb"].append({"name": str(step_id)})
    element = session.ifc_file.by_id(step_id)
    debug_props["attributes"] = []
    debug_props["inverse_attributes"] = []
    debug_props["inverse_references"] = []
    for key, value in element.get_info().items():
        add_attribute(debug_props["attributes"], key, value)
    for key in dir(element):
        if (not key[0].isalpha() or key[0] != key[0].upper() or key in element.get_info() or not getattr(element, key)):
            continue
        add_attribute(debug_props["inverse_attributes"], key, getattr(element, key))
    for inverse in session.ifc_file.get_inverse(element):
        debug_props["inverse_references"].append({"string_value": str(inverse), "int_value": inverse.id()})

# =============================================================================
# ✏️ (placeholder) Modifica attributi oggetto
# =============================================================================
def edit_object_data(object_id, attribute):
    entity = session.ifc_file.by_id(object_id)
    print(getattr(entity, attribute))

# =============================================================================
# 🚀 Esecuzione dell'app Streamlit
# =============================================================================
def execute():
    initialise_debug_props()
    st.set_page_config(page_title="Health", layout="wide")
    st.header("❓ Model Health")
    st.markdown("Automated analysis of BIM model health based on structural elements and data richness.")

    if "isHealthDataLoaded" not in session:
        initialize_session_state()

    tab1, = st.tabs(["📈 Charts"])
    # ============================================
    # TAB 1: Charts
    # ============================================
    with tab1:
        # Layout per centrare i controlli
        spacer1, col1, col2, col3, spacer2 = st.columns([1.5, 1, 1, 2, 1.5])
        with col1:
            color1 = st.color_picker("Color Graph 1", session.get("color1", "#00FFAA"), label_visibility="collapsed")
        with col2:
            color2 = st.color_picker("Color Graph 2", session.get("color2", "#FF3333"), label_visibility="collapsed")
        with col3:
            st.markdown('<div style="height: 4px;"></div>', unsafe_allow_html=True) 
            if st.button("🔄 Update graphs"):
                session["color1"] = color1
                session["color2"] = color2
                load_data()

        # Logica per caricamento e visualizzazione
        if "ifc_file" in session and not session.get("isHealthDataLoaded"):
            session["color1"] = color1
            session["color2"] = color2
            load_data()

        if session.get("isHealthDataLoaded"):
            draw_content()
        else:
            st.info("📂 To begin, load an IFC file from the Home page.")

# Esecuzione dell'app
execute()