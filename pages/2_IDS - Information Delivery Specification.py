# ─────────────────────────────────────────────
# 📦 Importazioni
# ─────────────────────────────────────────────
import streamlit as st
import json
import pandas as pd
import plotly.express as px
import io
import zipfile
import tempfile
from datetime import datetime
from fpdf import FPDF
import textwrap
import re
from tools import ifchelper

# ─────────────────────────────────────────────
# 🧠 Alias per lo stato della sessione Streamlit
# ─────────────────────────────────────────────
session = st.session_state

# -----------------------------
# ORGANIZZAZIONE DELLA PAGINA
# -----------------------------
# Panoramica funzioni/aree (in italiano):
# - validate_ifc_with_ids -> USATA: Tab IDS Validation Results e Automatic Test; SCOPO: valida IFC rispetto a regole IDS
# - Sidebar rule creator -> USATA: Sidebar; SCOPO: creare regole IDS
# - Tab outputs -> USATA: vari tab; SCOPO: mostrare regole, risultati, test e XML


# ─────────────────────────────────────────────
# 📚 Funzioni di supporto
# ─────────────────────────────────────────────
def validate_ifc_with_ids(ifc_file, ids_rules):
    """
    Valida un modello IFC rispetto alle regole IDS.
    Restituisce un DataFrame Pandas con:
    ElementID, ElementName, IFCClass, PropertySet, PropertyName, Value, Compliant
    """
    import pandas as pd
    results = []

    for rule in ids_rules:
        class_name = rule["ifc_class"]
        # Estrai i dati dell'IFC tramite ifchelper
        objects_data, _ = ifchelper.get_objects_data_by_class(ifc_file, class_name)

        if not objects_data:
            continue  # nessun oggetto di questa classe

        for obj_data in objects_data:
            for prop_rule in rule["properties"]:
                pset_name = prop_rule["property_set"]
                prop_name = prop_rule["property_name"]
                mandatory = prop_rule.get("mandatory", False)

                # Usa ifchelper.get_attribute_value per leggere i valori reali
                attr = f"{pset_name}.{prop_name}"
                val = ifchelper.get_attribute_value(obj_data, attr)

                is_valid = val is not None if mandatory else True

                results.append({
                    "ElementID": obj_data["GlobalId"],
                    "ElementName": obj_data.get("Name") or "(Unnamed)",
                    "IFCClass": class_name,
                    "PropertySet": pset_name,
                    "PropertyName": prop_name,
                    "Value": val,
                    "Compliant": is_valid
                })

    return pd.DataFrame(results)

# ─────────────────────────────────────────────
# ⚙️ Pagina IDS
# ─────────────────────────────────────────────
st.set_page_config(page_title="IDS", layout="wide")
st.title("🏗️ Information Delivery Specification")
st.markdown(
    "Create and manage IDS rules for validating your IFC4x3 models. "
    "Create rules based on IFC classes and their properties, then validate your loaded IFC file against these rules."
    "Check information quality and consistency easily."
)
# Reference to buildingSMART IDS
st.markdown("Reference: [buildingSMART - Information Delivery Specification (IDS)](https://www.buildingsmart.org/standards/bsi-standards/information-delivery-specification-ids/)")

# ─────────────────────────────────────────────
# ✅ Inizializza IDS rules in sessione
# ─────────────────────────────────────────────
if "ids_rules" not in session:
    session.ids_rules = []

# ─────────────────────────────────────────────
# 🧱 Sidebar – Creazione regole IDS con dizionario statico
# ─────────────────────────────────────────────
from tools.ifc_432_dictionary import IFC_STRUCTURAL_DICTIONARY_4x3

with st.sidebar:
    st.subheader("➕ Create IDS Rule")

    # IFC Class
    class_suggestions = sorted(list(IFC_STRUCTURAL_DICTIONARY_4x3.keys()))
    ifc_class = st.selectbox(
        "Select IFC Class",
        options=class_suggestions,
        index=0,
        help="Select an IFC Class or type your own"
    )
    ifc_class_custom = st.text_input(
        "Type IFC Class",
        value=ifc_class
    )
    ifc_class = ifc_class_custom.strip() or ifc_class

    # Property Set
    pset_suggestions = sorted(list(IFC_STRUCTURAL_DICTIONARY_4x3.get(ifc_class, {}).keys()))
    pset = st.selectbox(
        "Select IFC PropertySet",
        options=pset_suggestions or ["N/A"],
        index=0,
        help="Select an IFC PropertySet or type your own"
    )
    pset_custom = st.text_input(
        "Type IFC Property Set",
        value=pset if pset != "N/A" else ""
    )
    pset = pset_custom.strip() or pset

    # Property Name
    prop_suggestions = sorted(IFC_STRUCTURAL_DICTIONARY_4x3.get(ifc_class, {}).get(pset, []))
    prop_name = st.selectbox(
        "Select IFC PropertyName",
        options=prop_suggestions or ["N/A"],
        index=0,
        help="Select an IFC PropertyName or type your own"
    )
    prop_custom = st.text_input(
        "Type IFC PropertyName",
        value=prop_name if prop_name != "N/A" else ""
    )
    prop_name = prop_custom.strip() or prop_name

    # Mandatory checkbox e pulsanti
    mandatory = st.checkbox("Mandatory", value=True, key="checkbox_mandatory_schema")
    add_rule = st.button("Add Rule", key="btn_add_rule_schema")

    if add_rule and ifc_class and pset and prop_name:
        new_rule = {
            "ifc_class": ifc_class,
            "properties": [
                dict(property_set=pset, property_name=prop_name, mandatory=mandatory)
            ]
        }
        session.ids_rules.append(new_rule)
        st.success("✅ Rule added!")

    if st.button("🗑️ Remove All Rules"):
        session.ids_rules = []
        st.success("🗑️ All rules removed!")


# ─────────────────────────────────────────────
# ℹ️ Info IFC
# ─────────────────────────────────────────────
if "ifc_file" in session:
    ifc_model = session["ifc_file"]
    schema_obj = ifc_model.schema
    schema_name = getattr(schema_obj, "schema_identifier", str(schema_obj))
    st.info(f"📐 IFC Schema Detected: **{schema_name}**")
else:
    ifc_model = None
    st.warning("⚠️ No IFC file loaded. Please upload a file first in Home.")

# ─────────────────────────────────────────────
# Tabs principali
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab_xml = st.tabs(["📝 Current IDS Rules", "✅ IDS Validation Results", "🧪 Automatic IDS Test", "🗎 XML Output"])

# ─────────────────────────────────────────────
# Tab 1: Current IDS Rules
# ─────────────────────────────────────────────
with tab1:
    st.markdown("Create IDS rules in the sidebar. Each rule consists of an IFC class and one property set + with the associated property name. You can specify if each property is mandatory or optional. Once defined, you can export your IDS as a JSON file or you can validate the loaded IFC model in the 'IDS Validation Results' tab.")
    st.subheader("📝 Current IDS Rules Table")
    st.markdown("This tab lets you create and export IDS rules. Detected issues from validations are exported from the 'BCF / Reports' tab as CSV, HTML, PDF or a minimal BCF ZIP.")
    if session.ids_rules:
        cols = st.columns([1, 2, 2, 2, 1, 1])
        headers = ["Rule#", "IFC Class", "Property Set", "Property Name", "Mandatory", "Remove"]
        for col, header in zip(cols, headers):
            col.markdown(f"**{header}**")

        remove_indices = []
        for i, rule in enumerate(session.ids_rules):
            cols = st.columns([1, 2, 2, 2, 1, 1])
            cols[0].markdown(str(i+1))
            cols[1].markdown(rule["ifc_class"])
            cols[2].markdown(rule["properties"][0]["property_set"])
            cols[3].markdown(rule["properties"][0]["property_name"])
            cols[4].markdown(str(rule["properties"][0]["mandatory"]))

            if cols[5].button("🗑️", key=f"remove_{i}"):
                remove_indices.append(i)

        if remove_indices:
            for idx in sorted(remove_indices, reverse=True):
                session.ids_rules.pop(idx)

        ids_json = json.dumps(session.ids_rules, indent=2)
        st.download_button("💾 Export IDS JSON", ids_json, "dynamic_ids.json", "application/json")
    else:
        st.info("👈 No IDS rules defined yet. Use the sidebar to add rules.")

# ─────────────────────────────────────────────
# Tab 2: IDS Validation Results
# ─────────────────────────────────────────────
with tab2:
    st.markdown("This tab runs IDS validation on the loaded IFC model. Validation results are saved and can be exported from the 'BCF / Reports' tab as CSV, HTML, PDF or a minimal BCF ZIP.")
    if ifc_model and session.ids_rules:
        df = validate_ifc_with_ids(ifc_model, session.ids_rules)
        # salva l'ultimo risultato di validazione in sessione per l'esportazione
        session.ids_last_validation_df = df
        if not df.empty and "Compliant" in df.columns:
            st.subheader("✅ IDS Validation Table")
            st.dataframe(df, use_container_width=True)

            compliance_rate = df["Compliant"].mean() * 100
            st.metric("Compliance Rate", f"{compliance_rate:.1f}%")

            chart = df.groupby("IFCClass")["Compliant"].mean().reset_index()
            chart["Compliant"] = chart["Compliant"] * 100
            fig = px.bar(
                chart, x="IFCClass", y="Compliant", color="Compliant",
                color_continuous_scale="RdYlGn", title="Compliance per IFC Class (%)"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("⚠️ IDS rules defined, but no IFC data available.")
    else:
        st.info("👈 Define at least one IDS rule and load an IFC file in Home.")


# ─────────────────────────────────────────────
# Tab 3: Automatic IDS Test
# ─────────────────────────────────────────────
with tab3:
    st.markdown("This tab allows you to upload IDS or export-configuration JSON files for automated testing. Test results are stored and can be exported from the 'BCF / Reports' tab.")
    st.subheader("🧪 Test IDS on IFC File")

    st.info(
        "ℹ️ You can upload either:\n"
        "- **IDS JSON**: exported from the IDS page, containing explicit `properties` per rule.\n"
        "- **Export Configuration JSON**: exported from the Export Configuration page. "
        "Rules will be automatically normalized for testing.\n\n"
        "✅ Both formats are supported."
    )

    uploaded_ids = st.file_uploader(
        "Upload IDS JSON or Export Configuration JSON",
        type=["json"],
        key="upload_ids"
    )
    test_ids = None
    if uploaded_ids is not None:
        try:
            loaded_json = json.load(uploaded_ids)

            # Determina se è Export Configuration o IDS list
            if isinstance(loaded_json, dict) and "ExportRules" in loaded_json:
                raw_rules = loaded_json["ExportRules"]
            elif isinstance(loaded_json, list):
                raw_rules = loaded_json
            else:
                st.error(
                    "❌ IDS JSON has invalid structure. "
                    "Ensure it is exported from the IDS page or Export Configuration."
                )
                raw_rules = []

            # Trasforma tutte le regole in formato IDS
            test_ids = []
            for rule in raw_rules:
                if "properties" in rule:
                    # già in formato IDS
                    test_ids.append(rule)
                else:
                    # regola proveniente da Export Configuration
                    props = []
                    if rule.get("include_all_properties", False):
                        props.append({
                            "property_set": rule.get("property_set"),
                            "property_name": "ALL",
                            "mandatory": rule.get("mandatory", True)
                        })
                    else:
                        for pname in rule.get("property_name", []):
                            props.append({
                                "property_set": rule.get("property_set"),
                                "property_name": pname,
                                "mandatory": rule.get("mandatory", True)
                            })
                    test_ids.append({
                        "ifc_class": rule.get("ifc_class"),
                        "properties": props
                    })

            if test_ids:
                st.success("✅ IDS JSON loaded and normalized successfully")

        except Exception as e:
            st.error(f"❌ Error reading JSON: {e}")
            test_ids = None

    if ifc_model and test_ids:
        df_test = validate_ifc_with_ids(ifc_model, test_ids)
        # salva l'ultimo risultato di validazione in sessione per l'esportazione
        session.ids_last_validation_df = df_test
        st.subheader("✅ IDS Test Results")
        st.dataframe(df_test, use_container_width=True)

        compliance_rate_test = df_test["Compliant"].mean() * 100
        st.metric("Compliance Rate", f"{compliance_rate_test:.1f}%")

        chart_test = df_test.groupby("IFCClass")["Compliant"].mean().reset_index()
        chart_test["Compliant"] = chart_test["Compliant"] * 100
        fig_test = px.bar(
            chart_test, x="IFCClass", y="Compliant", color="Compliant",
            color_continuous_scale="RdYlGn",
            title="Compliance per IFC Class (%)"
        )
        st.plotly_chart(fig_test, use_container_width=True)

        csv_test = df_test.to_csv(index=False)
        st.download_button("💾 Export Test Results CSV", csv_test, "ids_test_results.csv", "text/csv")
    else:
        st.info(
            "👈 Upload IDS JSON or Export Configuration to run the test; "
            "IFC file must be loaded in Home."
        )

# ─────────────────────────────────────────────
# Tab 4: XML Output
# ─────────────────────────────────────────────
with tab_xml:
    st.subheader("🗎 IDS XML Output")
    if "ids_rules" not in session or not session.ids_rules:
        st.info("No IDS rules defined. Create rules in the sidebar to generate XML.")
    else:
        import xml.etree.ElementTree as ET
        from xml.dom import minidom

        root = ET.Element('IDS')
        for rule in session.ids_rules:
            rule_el = ET.SubElement(root, 'Rule')
            rule_el.set('ifc_class', str(rule.get('ifc_class', '')))
            props_el = ET.SubElement(rule_el, 'Properties')
            for prop in rule.get('properties', []):
                p = ET.SubElement(props_el, 'Property')
                p.set('property_set', str(prop.get('property_set', '')))
                p.set('name', str(prop.get('property_name', '')))
                p.set('mandatory', str(bool(prop.get('mandatory', False))).lower())
                # placeholder value if needed
                if prop.get('property_name') and prop.get('property_name') != 'ALL':
                    p.text = ''

        xml_bytes = ET.tostring(root, encoding='utf-8')
        pretty_xml = minidom.parseString(xml_bytes).toprettyxml(indent='  ')
        st.code(pretty_xml, language='xml')
        st.download_button("💾 Download IDS XML", pretty_xml, "ids_rules.xml", "application/xml")

# ─────────────────────────────────────────────
# Tab 4: moved to a dedicated page
# The BCF / Reports tab has been moved to: pages/1_BIM Collaboration Specification.py
# ─────────────────────────────────────────────
