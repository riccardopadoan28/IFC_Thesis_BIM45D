import streamlit as st 

# Impostazioni della pagina
st.set_page_config(page_title="Home", page_icon="🏠", layout="wide")

# Auto-cleanup of legacy temp folders and caches at startup (no UI)
try:
    from tools.pathhelper import cleanup_all
    cleanup_all(remove_static_temp=True, clean_caches=True)
except Exception:
    pass

# --- SIDEBAR (rimane visibile in tutte le pagine) ---
st.sidebar.title("Navigation")
st.sidebar.write("Use the menu above to explore the app pages.")

# --- CONTENUTO DELLA PAGINA HOME ---

# Titolo principale
st.title("ÅBIM45  - IFC4x3 Structural Data Management App")
st.markdown("OpenBIM platform to create, manage and export IFC4x3 data for BIM 4D/5D workflows. Configure export settings, author IDS rules, validate models, inspect health metrics and export reports from a single interface.")

st.markdown("""
---
### 🔍 Main Capabilities

1. IFC 4x3 Export Configuration — prepare and export IFC4x3 settings.
2. IFC Import & Viewer — upload and inspect schema, entities and properties.
3. IDS Creator — author and export IDS rules (JSON / XML).
4. BCF  exports, issue reporting and customizable PDF/HTML reports.
5. Validation & Model Health — run IDS validations and automated health metrics.
6. 3D Viewer — visualize IFC models with xeokit WebComponents.
7. Property & Quantity (QTO / BOQ) — extract properties, map property sets and export take-offs.
8. Scheduling (4D) — link elements to activities and create time-based sequences.
9. Cost Estimation (5D) — apply unit rates to QTO/BOQ and generate cost breakdowns.

Additional features:

- Templates & presets for exports, IDS rules and pricing tables.
- Batch processing and integration APIs for external systems.
- Multiple export formats (CSV, XLSX, JSON, XML) and session/cache management for large models.

---
### 💡 Tips

- Create IDS rules before validating to get meaningful reports.
- Use the Export Configuration JSON to standardize exporters across projects.
- Large IFCs may require time to process; use the Model Health page for quick data-quality checks.

---
### ⚙️ Technical Note
This app is built with **Streamlit** and integrates with **IfcOpenShell** and **xeokit WebComponents** for IFC processing and visualization.
- Regularly clear the cache or restart Streamlit if the app behaves unexpectedly.
- For optimal performance, use the latest version of Google Chrome or Microsoft Edge.
- Remember: this is an OpenBIM platform — everything is meant to stay interoperable and transparent.


---
### References

- Streamlit: https://streamlit.io/
- IfcOpenShell: https://ifcopenshell.org/
- xeokit WebComponents: https://github.com/xeokit/xeokit-webcomponents
- xeokit blog (building viewers): https://xeokit.io/blog/building-3d-model-viewers-with-xeokit-webcomponents/
- xeokit CDN module: https://cdn.jsdelivr.net/npm/@xeokit/xeokit-webcomponents/dist/index.min.js
- pandas: https://pandas.pydata.org/ (data handling, QTO/BOQ export)
- openpyxl / XlsxWriter: https://openpyxl.readthedocs.io/ (XLSX export)
- lxml / xml libraries: https://lxml.de/ (IDS/XML export and parsing)
- plotly: https://plotly.com/ (visualizations and timelines)
- BCF format / collaboration workflows: https://github.com/BuildingSMART/BCF-XML
- IDS specification: https://www.buildingsmart.org/standards/bsi-standards/information-delivery-specification-ids/
- IFC4.3 / IFC4x3 docs: https://ifc43-docs.standards.buildingsmart.org/
            """)

# Footer
st.markdown("---")
st.markdown("© 2025 – ÅBIM45 | Developed by RSP CONSULTING.")
st.markdown("Visit [https://github.com/riccardopadoan28/IFC_Thesis_BIM45D] for more details.")
st.markdown("All rights reserved. | This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).")