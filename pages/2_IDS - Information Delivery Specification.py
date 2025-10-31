# ─────────────────────────────────────────────
# 📦 Imports (standardized)
# ─────────────────────────────────────────────
import streamlit as st
from tools import p_shared as shared  # shared model info helpers
from tools import p2_ids as p2  # per-page helper
import json
from tools.pathhelper import save_text, save_bytes
import plotly.express as px
from datetime import datetime
import pandas as pd

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

# ─────────────────────────────────────────────
# 📚 Funzioni di supporto
# ─────────────────────────────────────────────
# Replace custom validator with parser for official validate CLI output

def _parse_validate_stdout_to_df(stdout: str) -> pd.DataFrame:
    try:
        data = json.loads(stdout)
    except Exception:
        return pd.DataFrame([{"Raw": stdout}])

    rows = []

    def walk(obj):
        if isinstance(obj, dict):
            row = {}
            for k in ("guid", "GlobalId", "globalId", "id"):
                if k in obj and isinstance(obj[k], str):
                    row["ElementID"] = obj[k]
                    break
            for k in ("ifc_class", "ifcClass", "class", "entity"):
                if k in obj and isinstance(obj[k], str):
                    row["IFCClass"] = obj[k]
                    break
            for k in ("specification", "spec", "name"):
                if k in obj and isinstance(obj[k], str):
                    row["Specification"] = obj[k]
                    break
            for k in ("requirement", "property", "rule", "description"):
                if k in obj and isinstance(obj[k], str):
                    row["Requirement"] = obj[k]
                    break
            for k in ("conforms", "result", "status", "valid", "conformant"):
                if k in obj:
                    v = obj[k]
                    row["Compliant"] = bool(v) if isinstance(v, bool) else str(v).lower() in ("true", "pass", "passed", "ok", "conformant")
                    break
            if row:
                rows.append(row)
            for v in obj.values():
                walk(v)
        elif isinstance(obj, list):
            for it in obj:
                walk(it)

    walk(data)

    if rows:
        df = pd.DataFrame(rows)
        for col in ["ElementID", "IFCClass", "Specification", "Requirement", "Compliant"]:
            if col not in df.columns:
                df[col] = None
        # Order columns
        ordered = ["ElementID", "IFCClass", "Specification", "Requirement", "Compliant"]
        others = [c for c in df.columns if c not in ordered]
        return df[ordered + others]

    # Fallback: show raw data
    if isinstance(data, list):
        return pd.DataFrame(data)
    return pd.DataFrame([data])

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

# Show availability status of official tools
if hasattr(p2, 'OFFICIAL_VALIDATOR_AVAILABLE') and hasattr(p2, 'IDS_AUDIT_AVAILABLE'):
    if p2.OFFICIAL_VALIDATOR_AVAILABLE and p2.IDS_AUDIT_AVAILABLE:
        st.success("✅ Official buildingSMART validation tools are available and will be used automatically.")
    else:
        missing = []
        if not p2.OFFICIAL_VALIDATOR_AVAILABLE:
            missing.append("[buildingSMART/validate](https://github.com/buildingSMART/validate)")
        if not p2.IDS_AUDIT_AVAILABLE:
            missing.append("[IDS-Audit-tool](https://github.com/buildingSMART/IDS-Audit-tool)")
        st.warning(
            f"⚠️ Official tools not installed: {', '.join(missing)}. "
            f"The app will fall back to CLI or custom validation. "
            f"Install these tools for the best experience: "
            f"`pip install git+https://github.com/buildingSMART/validate.git git+https://github.com/buildingSMART/IDS-Audit-tool.git`"
        )

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
# Tab 2: IDS Validation Results — use IDS-Audit + official validate CLI
# ─────────────────────────────────────────────
with tab2:
    st.markdown("This tab runs IDS validation on the loaded IFC model using the official validator. The generated IDS XML is first audited with IDS-Audit.")
    if ifc_model and session.ids_rules:
        # Generate IDS XML from current rules
        ids_xml_str = p2.ids_rules_to_xml(session.ids_rules)
        ids_xml_bytes = ids_xml_str.encode('utf-8')

        # Audit IDS XML
        ok_audit, audit_report = p2.audit_ids_xml(ids_xml_bytes)
        if ok_audit:
            st.success("IDS-Audit passed for generated IDS XML.")
        else:
            st.error("IDS-Audit reported issues for the generated IDS XML.")
            with st.expander("Audit report"):
                st.code(audit_report or "", language="json")

        # Run official validation only if audit passed
        if ok_audit:
            # Add option to use custom validator as fallback
            use_official = st.checkbox("Use official buildingSMART validator (recommended)", value=True, key="use_official_validator_tab2")
            res = p2.validate_ifc_with_ids_xml_official(ifc_model, ids_xml_bytes, use_python_api=use_official)
            if res.get("ok") and res.get("stdout"):
                df = _parse_validate_stdout_to_df(res["stdout"]) 
                session.ids_last_validation_df = df
                if not df.empty and ("Compliant" in df.columns):
                    st.subheader("✅ IDS Validation Table (official)")
                    st.dataframe(df, use_container_width=True)

                    # Summary
                    st.markdown("### Summary")
                    if "IFCClass" in df.columns:
                        for class_name, group in df.groupby("IFCClass"):
                            total = len(group)
                            passed = int(group.get("Compliant", pd.Series([False]*total)).sum()) if "Compliant" in group.columns else 0
                            st.markdown(f"**{class_name}** — 🗹 {passed}/{total} passed the requirement.")

                    if "Compliant" in df.columns:
                        compliance_rate = df["Compliant"].mean() * 100
                        st.metric("Compliance Rate", f"{compliance_rate:.1f}%")

                        chart = df.groupby("IFCClass")["Compliant"].mean().reset_index() if "IFCClass" in df.columns else pd.DataFrame()
                        if not chart.empty:
                            chart["Compliant"] = chart["Compliant"] * 100
                            fig = px.bar(
                                chart, x="IFCClass", y="Compliant", color="Compliant",
                                color_continuous_scale="RdYlGn", title="Compliance per IFC Class (%)"
                            )
                            st.plotly_chart(fig, use_container_width=True)

                    # Save CSV
                    if st.button("Save results CSV to temp_file", key="btn_save_ids_results_csv"):
                        try:
                            csv_bytes = df.to_csv(index=False).encode('utf-8')
                            path, url = save_bytes("ids_validation_results.csv", csv_bytes)
                            st.success(f"Saved in static/temp_file — {path.name}")
                            st.markdown(f"[Click to download]({url})")
                        except Exception as e:
                            st.error(f"Unable to save: {e}")
            else:
                st.error("Official validator failed. Ensure the 'validate' CLI is installed and on PATH.")
                if res.get("error"):
                    st.code(res.get("error"), language="bash")
                if res.get("stdout"):
                    st.code(res.get("stdout"), language="json")
    else:
        st.info("👈 Define at least one IDS rule and load an IFC file in Home.")


# ─────────────────────────────────────────────
# Tab 3: XML Output — show IDS-Audit status
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

        # Audit result
        ok_audit_xml, audit_report_xml = p2.audit_ids_xml(xml_bytes)
        if ok_audit_xml:
            st.success("IDS-Audit passed for current XML.")
        else:
            st.warning("IDS-Audit found issues for current XML. See report below.")
            with st.expander("Audit report"):
                st.code(audit_report_xml or "", language="json")

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
# Tab 4: Automatic IDS Test — audit uploaded IDS and use official validate
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

    ids_xml_bytes = None
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
                # We have IDS XML: keep bytes and show quick summary
                ids_xml_bytes = content
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
                    st.warning("No 'specification' found in the uploaded IDS XML.")

            else:
                # Not XML: try as JSON → normalize to rules then to IDS XML
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

                # Convert to IDS XML
                ids_xml_str = p2.ids_rules_to_xml(test_ids or [])
                ids_xml_bytes = ids_xml_str.encode('utf-8')

            # Audit any IDS XML we have
            if ids_xml_bytes:
                ok_audit_u, audit_report_u = p2.audit_ids_xml(ids_xml_bytes)
                if ok_audit_u:
                    st.success("IDS-Audit passed for uploaded/normalized IDS.")
                else:
                    st.error("IDS-Audit reported issues for the uploaded/normalized IDS.")
                    with st.expander("Audit report"):
                        st.code(audit_report_u or "", language="json")

        except Exception as e:
            st.error(f"❌ Error reading the uploaded file: {e}")
            test_ids = None
            ids_xml_bytes = None

    # Run validation and show outputs via official CLI
    if ifc_model and ids_xml_bytes:
        # Add option to use official validator
        use_official_test = st.checkbox("Use official buildingSMART validator (recommended)", value=True, key="use_official_validator_tab4")
        res_test = p2.validate_ifc_with_ids_xml_official(ifc_model, ids_xml_bytes, use_python_api=use_official_test)
        if res_test.get("ok") and res_test.get("stdout"):
            df_test = _parse_validate_stdout_to_df(res_test["stdout"]) 
            session.ids_last_validation_df = df_test

            try:
                if "Compliant" in df_test.columns:
                    df_view = df_test.sort_values(["Compliant", "IFCClass"])  # False < True
                else:
                    df_view = df_test
            except Exception:
                df_view = df_test

            st.subheader("✅ IDS test results (official)")
            st.dataframe(df_view, use_container_width=True)

            total = len(df_view)
            if total > 0 and "Compliant" in df_view.columns:
                fails = int((~df_view["Compliant"]).sum())
                passes = total - fails
                st.markdown(
                    f"- Total checks: **{total}**\n"
                    f"- Compliant: **{passes}**\n"
                    f"- Non-compliant: **{fails}**"
                )
                compliance_rate_test = df_view["Compliant"].mean() * 100
                st.metric("Compliance rate", f"{compliance_rate_test:.1f}%")

                if "IFCClass" in df_view.columns:
                    chart_test = df_view.groupby("IFCClass")["Compliant"].mean().reset_index()
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
            st.error("Official validator failed. Ensure the 'validate' CLI is installed and on PATH.")
            if res_test.get("error"):
                st.code(res_test.get("error"), language="bash")
            if res_test.get("stdout"):
                st.code(res_test.get("stdout"), language="json")
    else:
        st.info("Upload an IDS file (XML/JSON) and make sure an IFC file is loaded in Home to run the test.")

# ─────────────────────────────────────────────
# Tab 4: moved to a dedicated page
# The BCF / Reports tab has been moved to: pages/1_BIM Collaboration Specification.py
# ─────────────────────────────────────────────
