# ─────────────────────────────────────────────
# 📦 Importazioni
# ─────────────────────────────────────────────
import streamlit as st  # UI e layout dell'app
import json  # lettura/scrittura file IDS/Config
import pandas as pd  # tabelle risultati e aggregazioni
import plotly.express as px  # grafici di conformità
import io  # buffer file (supporto ad esportazioni)
import zipfile  # pacchetti BCF (altra pagina)
import tempfile  # gestione file temporanei
from datetime import datetime  # timestamp in XML e report
from fpdf import FPDF  # report PDF (altra pagina)
import textwrap  # formattazione testi per report PDF
import re  # semplici controlli/normalizzazioni testuali
from tools import ifchelper  # helper IFC condivisi
from tools.pathhelper import save_text, save_bytes  # funzioni per salvare file temporanei
# Import validate function from helper (moved to tools.ifchelper to centralize IFC logic)
from tools.ifchelper import validate_ifc_with_ids  # validazione IFC rispetto alle regole IDS

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
    Valida un modello IFC rispetto alle regole IDS usando l'API ufficiale ifcopenshell.
    Restituisce un DataFrame Pandas con:
    ElementID, ElementName, IFCClass, PropertySet, PropertyName, Value, Compliant
    """
    import pandas as pd
    import ifcopenshell
    from ifcopenshell.util import element as ifc_element

    results = []

    # Accept either an opened model or a file path
    try:
        model = ifc_file if hasattr(ifc_file, "by_type") else ifcopenshell.open(ifc_file)
    except Exception:
        # fallback: if opening fails, try treating as already-opened model
        model = ifc_file

    for rule in ids_rules:
        class_name = rule.get("ifc_class")
        if not class_name:
            continue

        try:
            elements = model.by_type(class_name) or []
        except Exception:
            elements = []

        if not elements:
            continue  # nessun oggetto di questa classe

        for obj in elements:
            # get property sets using official util
            try:
                psets = ifc_element.get_psets(obj) or {}
            except Exception:
                psets = {}

            for prop_rule in rule.get("properties", []):
                pset_name = prop_rule.get("property_set", "")
                prop_name = prop_rule.get("property_name", "")
                mandatory = prop_rule.get("mandatory", False)

                val = None

                if pset_name:
                    # look for the specified property set
                    pset_props = psets.get(pset_name)
                    if pset_props is not None:
                        if prop_name == "ALL":
                            val = pset_props
                        else:
                            val = pset_props.get(prop_name)
                    else:
                        # try case-insensitive match for PSet name
                        for pn, props in psets.items():
                            if pn.lower() == pset_name.lower():
                                if prop_name == "ALL":
                                    val = props
                                else:
                                    val = props.get(prop_name)
                                pset_name = pn
                                break
                else:
                    # no property set specified: search across all PSets
                    for pn, props in psets.items():
                        if prop_name == "ALL":
                            val = props
                            pset_name = pn
                            break
                        if prop_name in props:
                            val = props.get(prop_name)
                            pset_name = pn
                            break

                # final fallback: try direct attribute on the IFC entity
                if val is None and prop_name and hasattr(obj, prop_name):
                    try:
                        val = getattr(obj, prop_name)
                    except Exception:
                        val = None

                is_valid = (val is not None) if mandatory else True

                # try to get a stable element identifier
                element_id = None
                if hasattr(obj, "GlobalId"):
                    element_id = getattr(obj, "GlobalId", None)
                elif hasattr(obj, "GlobalID"):
                    element_id = getattr(obj, "GlobalID", None)
                else:
                    try:
                        element_id = obj.id()
                    except Exception:
                        element_id = None

                results.append({
                    "ElementID": element_id,
                    "ElementName": getattr(obj, "Name", None) or "(Unnamed)",
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
    "Create rules based on IFC classes and their properties, then validate your loaded IFC file against these rules. "
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
tab1, tab2, tab3, tab_xml = st.tabs(["📝 Current IDS Rules", "✅ IDS Validation Results", "🗎 XML Output", "🧪 Automatic IDS Test"])

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
        if st.button("Save IDS JSON to temp_file", key="btn_save_ids_json"):
            try:
                path, url = save_text("ids_rules.json", ids_json)
                st.success(f"Saved in static/temp_file — {path.name}")
                st.markdown(f"[Click to download]({url})")
            except Exception as e:
                st.error(f"Unable to save: {e}")
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

            # Quick textual summary per IFC class
            st.markdown("### Summary")
            for class_name, group in df.groupby("IFCClass"):
                total = len(group)
                passed = int(group["Compliant"].sum())
                st.markdown(f"**{class_name}** — 🗹 {passed}/{total} passed the requirement.")

                # Missing properties (Compliant == False and Value is None)
                missing_df = group[(~group["Compliant"]) & (group["Value"].isnull())]
                if not missing_df.empty:
                    miss_counts = missing_df.groupby("PropertyName").size().reset_index(name="count")
                    for _, row_m in miss_counts.iterrows():
                        pname = row_m['PropertyName'] or '(Unnamed)'
                        st.markdown(f"🗷 {row_m['count']}/{total} {class_name} don't have a *{pname}* property.")

                # Invalid values (Compliant == False but Value present)
                invalid_df = group[(~group["Compliant"]) & (~group["Value"].isnull())]
                if not invalid_df.empty:
                    inval_counts = invalid_df.groupby(["PropertyName", "Value"]).size().reset_index(name="count")
                    for _, row_i in inval_counts.iterrows():
                        pname = row_i['PropertyName'] or '(Unnamed)'
                        val = str(row_i['Value'])
                        st.markdown(f"🗷 {row_i['count']}/{total} {class_name} have *{pname}* value '{val}' which is not allowed.")

            compliance_rate = df["Compliant"].mean() * 100
            st.metric("Compliance Rate", f"{compliance_rate:.1f}%")

            chart = df.groupby("IFCClass")["Compliant"].mean().reset_index()
            chart["Compliant"] = chart["Compliant"] * 100
            fig = px.bar(
                chart, x="IFCClass", y="Compliant", color="Compliant",
                color_continuous_scale="RdYlGn", title="Compliance per IFC Class (%)"
            )
            st.plotly_chart(fig, use_container_width=True)
            # Optional explicit save to temp_file on user action
            if st.button("Save results CSV to temp_file", key="btn_save_ids_results_csv"):
                try:
                    csv_bytes = df.to_csv(index=False).encode('utf-8')
                    path, url = save_bytes("ids_validation_results.csv", csv_bytes)
                    st.success(f"Saved in static/temp_file — {path.name}")
                    st.markdown(f"[Click to download]({url})")
                except Exception as e:
                    st.error(f"Unable to save: {e}")
        else:
            st.info("⚠️ IDS rules defined, but no IFC data available.")
    else:
        st.info("👈 Define at least one IDS rule and load an IFC file in Home.")


# ─────────────────────────────────────────────
# Tab 3: XML Output
# ─────────────────────────────────────────────
with tab3:
    st.subheader("🗎 IDS XML Output")
    if "ids_rules" not in session or not session.ids_rules:
        st.info("No IDS rules defined. Create rules in the sidebar to generate XML.")
    else:
        import xml.etree.ElementTree as ET
        from xml.dom import minidom

        # Register namespaces
        ET.register_namespace('xs', 'http://www.w3.org/2001/XMLSchema')
        ET.register_namespace('xsi', 'http://www.w3.org/2001/XMLSchema-instance')
        ET.register_namespace('ids', 'http://standards.buildingsmart.org/IDS')

        ns = {
            'xs': 'http://www.w3.org/2001/XMLSchema',
            'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
            'ids': 'http://standards.buildingsmart.org/IDS'
        }

        # Root element with schemaLocation attribute
        root = ET.Element(f"{{{ns['ids']}}}ids", {
            f"{{{ns['xsi']}}}schemaLocation": "http://standards.buildingsmart.org/IDS http://standards.buildingsmart.org/IDS/1.0/ids.xsd"
        })

        # Info block
        info = ET.SubElement(root, f"{{{ns['ids']}}}info")
        title = ET.SubElement(info, f"{{{ns['ids']}}}title")
        title.text = "Dynamic IDS"
        version = ET.SubElement(info, f"{{{ns['ids']}}}version")
        version.text = "1.0"
        author = ET.SubElement(info, f"{{{ns['ids']}}}author")
        author.text = "generated@bim45d.local"
        date_el = ET.SubElement(info, f"{{{ns['ids']}}}date")
        date_el.text = datetime.now().date().isoformat()

        # Specifications container
        specs = ET.SubElement(root, f"{{{ns['ids']}}}specifications")

        # Build one specification per IDS rule
        for idx, rule in enumerate(session.ids_rules):
            spec = ET.SubElement(specs, f"{{{ns['ids']}}}specification", {
                'ifcVersion': 'IFC4X3',
                'name': f"Requirement for {rule.get('ifc_class', '')}",
                'identifier': f"S{idx+1}"
            })

            # applicability -> entity -> name -> simpleValue
            appl = ET.SubElement(spec, f"{{{ns['ids']}}}applicability", {
                'minOccurs': '0', 'maxOccurs': 'unbounded'
            })
            entity = ET.SubElement(appl, f"{{{ns['ids']}}}entity")
            name_el = ET.SubElement(entity, f"{{{ns['ids']}}}name")
            simple_val = ET.SubElement(name_el, f"{{{ns['ids']}}}simpleValue")
            simple_val.text = rule.get('ifc_class', '')

            # requirements
            reqs = ET.SubElement(spec, f"{{{ns['ids']}}}requirements")

            for prop in rule.get('properties', []):
                prop_name = prop.get('property_name', '')
                pset = prop.get('property_set', '')

                prop_el = ET.SubElement(reqs, f"{{{ns['ids']}}}property", {
                    'dataType': 'IFCLABEL',
                    'uri': f"https://identifier.buildingsmart.org/uri/buildingsmart/ifc/4.3/prop/{prop_name}",
                    'cardinality': 'required' if prop.get('mandatory', False) else 'optional'
                })

                pset_el = ET.SubElement(prop_el, f"{{{ns['ids']}}}propertySet")
                sv_pset = ET.SubElement(pset_el, f"{{{ns['ids']}}}simpleValue")
                sv_pset.text = pset

                basename = ET.SubElement(prop_el, f"{{{ns['ids']}}}baseName")
                sv_base = ET.SubElement(basename, f"{{{ns['ids']}}}simpleValue")
                sv_base.text = prop_name

                # Optional allowed values -> produce xs:restriction with xs:enumeration entries
                allowed = prop.get('allowed_values') or prop.get('values')
                if allowed:
                    value_el = ET.SubElement(prop_el, f"{{{ns['ids']}}}value")
                    restriction = ET.SubElement(value_el, f"{{{ns['xs']}}}restriction", {'base': 'xs:string'})
                    for v in allowed:
                        ET.SubElement(restriction, f"{{{ns['xs']}}}enumeration", {'value': str(v)})

        # Pretty print and output
        xml_bytes = ET.tostring(root, encoding='utf-8')
        pretty_xml = minidom.parseString(xml_bytes).toprettyxml(indent='  ')
        st.code(pretty_xml, language='xml')
        st.download_button("💾 Download IDS XML", pretty_xml, "ids_rules.xml", "application/xml")
        if st.button("Save IDS XML to temp_file", key="btn_save_ids_xml"):
            try:
                path, url = save_text("ids_rules.xml", pretty_xml)
                st.success(f"Saved in static/temp_file — {path.name}")
                st.markdown(f"[Click to download]({url})")
            except Exception as e:
                st.error(f"Unable to save: {e}")

# ─────────────────────────────────────────────
# Tab 4: Automatic IDS Test
# ─────────────────────────────────────────────
with tab_xml:
    st.markdown("This tab lets you automatically test an IFC file against IDS rules loaded from a file.")
    st.subheader("🧪 Test IDS on IFC file")

    st.info(
        "What you can upload:\n"
        "- IDS XML compliant with buildingSMART.\n"
        "- IDS JSON exported from this page.\n"
        "- Export Configuration JSON (it will be normalized into IDS rules).\n\n"
        "What you get:\n"
        "- clear summary of loaded rules (specifications/properties count, involved classes);\n"
        "- results table sorted with non-compliant first;\n"
        "- concise metrics and compliance-by-class chart;\n"
        "- CSV download of results."
    )

    uploaded_ids = st.file_uploader(
        "Upload IDS JSON / Export Configuration JSON / IDS XML",
        type=["json", "xml"],
        key="upload_ids"
    )

    test_ids = None
    if uploaded_ids is not None:
        try:
            # Try as XML first
            content = uploaded_ids.read()
            parsed_xml = None
            try:
                import xml.etree.ElementTree as ET
                parsed_xml = ET.fromstring(content)
            except Exception:
                parsed_xml = None

            if parsed_xml is not None:
                # Parse IDS XML into internal format
                ns = {
                    'ids': 'http://standards.buildingsmart.org/IDS',
                    'xs': 'http://www.w3.org/2001/XMLSchema'
                }
                test_ids = []
                specs = parsed_xml.findall('.//{http://standards.buildingsmart.org/IDS}specification') or parsed_xml.findall('.//specification')

                for spec in specs:
                    ifc_class = ''
                    appl = spec.find('.//{http://standards.buildingsmart.org/IDS}applicability') or spec.find('.//applicability')
                    if appl is not None:
                        sv = appl.find('.//{http://standards.buildingsmart.org/IDS}simpleValue') or appl.find('.//simpleValue')
                        if sv is not None and sv.text:
                            ifc_class = sv.text.strip()
                    if not ifc_class:
                        ifc_class = spec.get('name', '').replace('Requirement for ', '')

                    props = []
                    for prop_el in spec.findall('.//{http://standards.buildingsmart.org/IDS}property') or spec.findall('.//property'):
                        pname = ''
                        pset = ''
                        mandatory = False
                        allowed_vals = None

                        card = prop_el.get('cardinality')
                        if card and card.lower().startswith('required'):
                            mandatory = True

                        pset_el = prop_el.find('.//{http://standards.buildingsmart.org/IDS}propertySet/{http://standards.buildingsmart.org/IDS}simpleValue') or prop_el.find('.//propertySet/simpleValue')
                        if pset_el is not None and pset_el.text:
                            pset = pset_el.text.strip()

                        base_el = prop_el.find('.//{http://standards.buildingsmart.org/IDS}baseName/{http://standards.buildingsmart.org/IDS}simpleValue') or prop_el.find('.//baseName/simpleValue')
                        if base_el is not None and base_el.text:
                            pname = base_el.text.strip()

                        allowed = []
                        val_block = prop_el.find('.//{http://standards.buildingsmart.org/IDS}value') or prop_el.find('.//value')
                        if val_block is not None:
                            restr = val_block.find('.//{http://www.w3.org/2001/XMLSchema}restriction') or val_block.find('.//restriction')
                            if restr is not None:
                                enums = restr.findall('.//{http://www.w3.org/2001/XMLSchema}enumeration') or restr.findall('.//enumeration')
                                for e in enums:
                                    v = e.get('value') or (e.text if e.text else None)
                                    if v:
                                        allowed.append(v)
                        if allowed:
                            allowed_vals = allowed

                        props.append({
                            'property_set': pset,
                            'property_name': pname,
                            'mandatory': mandatory,
                            'allowed_values': allowed_vals
                        })

                    test_ids.append({'ifc_class': ifc_class, 'properties': props})

                if test_ids:
                    n_specs = len(test_ids)
                    n_props = sum(len(r.get('properties', [])) for r in test_ids)
                    classes = sorted({r.get('ifc_class', '') for r in test_ids if r.get('ifc_class')})
                    preview = ", ".join(classes[:8]) + ("…" if len(classes) > 8 else "")
                    st.success(f"✅ IDS XML loaded: {n_specs} specifications, {n_props} properties. Classes: {preview}")
                else:
                    st.error("❌ No valid 'specification' found in the uploaded IDS XML.")

            else:
                # Not XML: try as JSON
                uploaded_ids.seek(0)
                loaded_json = json.load(uploaded_ids)

                if isinstance(loaded_json, dict) and "ExportRules" in loaded_json:
                    raw_rules = loaded_json["ExportRules"]
                elif isinstance(loaded_json, list):
                    raw_rules = loaded_json
                else:
                    st.error("❌ Invalid JSON structure. Expected an IDS list or an object with 'ExportRules'.")
                    raw_rules = []

                test_ids = []
                for rule in raw_rules:
                    if "properties" in rule:
                        test_ids.append(rule)
                    else:
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
                    n_specs = len(test_ids)
                    n_props = sum(len(r.get('properties', [])) for r in test_ids)
                    classes = sorted({r.get('ifc_class', '') for r in test_ids if r.get('ifc_class')})
                    preview = ", ".join(classes[:8]) + ("…" if len(classes) > 8 else "")
                    st.success(f"✅ IDS JSON loaded: {n_specs} specifications, {n_props} properties. Classes: {preview}")

        except Exception as e:
            st.error(f"❌ Error reading the uploaded file: {e}")
            test_ids = None

    # Run validation and show clearer outputs
    if ifc_model and test_ids:
        df_test = validate_ifc_with_ids(ifc_model, test_ids)
        session.ids_last_validation_df = df_test

        # Sort: non-compliant first, then by class/pset/property
        try:
            df_view = df_test.sort_values(["Compliant", "IFCClass", "PropertySet", "PropertyName"])  # False < True
        except Exception:
            df_view = df_test

        st.subheader("✅ IDS test results")
        st.dataframe(df_view, use_container_width=True)

        total = len(df_view)
        fails = int((~df_view["Compliant"]).sum()) if "Compliant" in df_view.columns else 0
        passes = total - fails
        missing = int((df_view["Value"].isnull() & (~df_view["Compliant"])).sum()) if "Value" in df_view.columns and "Compliant" in df_view.columns else 0
        invalid = fails - missing

        st.markdown(
            f"- Total checks: **{total}**\n"
            f"- Compliant: **{passes}**\n"
            f"- Non-compliant: **{fails}** (missing: {missing}, disallowed values: {invalid})"
        )

        compliance_rate_test = df_view["Compliant"].mean() * 100 if "Compliant" in df_view.columns else 0.0
        st.metric("Compliance rate", f"{compliance_rate_test:.1f}%")

        chart_test = df_view.groupby("IFCClass")["Compliant"].mean().reset_index() if "Compliant" in df_view.columns else pd.DataFrame()
        if not chart_test.empty:
            chart_test["Compliant"] = chart_test["Compliant"] * 100
            fig_test = px.bar(
                chart_test,
                x="IFCClass",
                y="Compliant",
                color="Compliant",
                color_continuous_scale="RdYlGn",
                title="Compliance by IFC class (%)"
            )
            st.plotly_chart(fig_test, use_container_width=True)

        csv_test = df_view.to_csv(index=False)
        st.download_button("💾 Download results CSV", csv_test, "ids_test_results.csv", "text/csv")
        if st.button("Save test results CSV to temp_file", key="btn_save_ids_test_csv"):
            try:
                path, url = save_text("ids_test_results.csv", csv_test)
                st.success(f"Saved in static/temp_file — {path.name}")
                st.markdown(f"[Click to download]({url})")
            except Exception as e:
                st.error(f"Unable to save: {e}")
    else:
        st.info("Upload an IDS file (XML/JSON) and make sure an IFC file is loaded in Home to run the test.")

# ─────────────────────────────────────────────
# Tab 4: moved to a dedicated page
# The BCF / Reports tab has been moved to: pages/1_BIM Collaboration Specification.py
# ─────────────────────────────────────────────
