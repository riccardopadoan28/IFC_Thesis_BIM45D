import streamlit as st 

# Impostazioni della pagina
st.set_page_config(page_title="Home", page_icon="🏠", layout="wide")

# --- SIDEBAR (rimane visibile in tutte le pagine) ---
st.sidebar.title("Navigation")
st.sidebar.write("Use the menu above to explore the app pages.")

# --- CONTENUTO DELLA PAGINA HOME ---

# Titolo principale
st.title("BIM45D - IFC4x3 Structural Data Management App")
st.markdown("OpenBIM platform to create, manage and export IFC4x3 data for BIM 4D/5D workflows. Configure export settings, author IDS rules, validate models, inspect health metrics and export reports from a single interface.")

st.markdown("""
---
### 🔍 Main Features

1. **IFC Export Configuration** – prepare IFC4x3 export settings and download a JSON configuration.
2. **IDS Creator** – author Information Delivery Specification (IDS) rules and export them as JSON or XML.
3. **Validation Tools** – validate loaded IFC models against IDS rules and save results for reporting.
4. **Model Health** – automated analysis using the IFC4x3 structural dictionary (counts, property-set ratio, simple verdict).
5. **IFC Import & Viewer** – upload IFC files and inspect schema, entities and properties.
6. **BIM Collaboration (BCF-like)** – dedicated page for exporting validation results as TXT/HTML for issue workflows.

---
### 🧭 How to Use

- Start with **IFC Export Configuration** to define export behavior and entity filters.
- Use **IDS Creator** to build validation rules; view XML output in the IDS page and export for reuse.
- Upload an IFC via **IFC Import**, then run **Validation Tools** or **Model Health** to analyze the model.
- Export reports from the **BIM Collaboration** page.

---
### References

- IDS specification: [buildingSMART – IDS](https://www.buildingsmart.org/standards/bsi-standards/information-delivery-specification-ids/)
- IFC4.3 docs: [IFC4.3 - buildingSMART](https://ifc43-docs.standards.buildingsmart.org/)

---
### 💡 Tips

- Create IDS rules before validating to get meaningful reports.
- Use the Export Configuration JSON to standardize exporters across projects.
- Large IFCs may require time to process; use the Model Health page for quick data-quality checks.

---
### ⚙️ Technical Note
This app is built with **Streamlit** and integrates with **IfcOpenShell** and **web-ifc** for IFC processing.
- Regularly clear the cache or restart Streamlit if the app behaves unexpectedly.
- For optimal performance, use the latest version of Google Chrome or Microsoft Edge.
- Remember: this is an OpenBIM platform — everything is meant to stay interoperable and transparent.
""")

# Footer
st.markdown("---")
st.markdown("© 2025 – BIM45D | Developed by Riccardo Padoan, RSP Group.")
st.markdown("| Visit [https://github.com/riccardopadoan28/IFC_Thesis_BIM45D] for more details.")
st.markdown("All rights reserved. | This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).")