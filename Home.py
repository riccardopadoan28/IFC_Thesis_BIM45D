import streamlit as st 

# Impostazioni della pagina
st.set_page_config(page_title="Home", page_icon="🏠", layout="wide")

# --- SIDEBAR (rimane visibile in tutte le pagine) ---
st.sidebar.title("Navigation")
st.sidebar.write("Use the menu below to explore the app pages.")

# --- CONTENUTO DELLA PAGINA HOME ---

# Titolo principale
st.title("BIM45D - IFC Structural Data Management Application")
st.text("OpenBIM platform to help you create, manage, and export Industry Foundation Classes data for your BIM 4D and 5D workflows. You can configure custom rules, inspect models, and generate IFC files directly through an intuitive interface.")

st.markdown("""
---
### 🔍 Main Features

1. **IFC Export Configuration** – Set up and save export settings for your IFC through the creation of a JSON file.  
2. **IDS Creator** – Create and manage Information Delivery Specification (IDS) rules for IFC data validation.  
3. **Validation Tools** – Verify IFC files against IDS rules to ensure compliance.  
4. **IFC Viewer** – Upload and visualize IFC models in 3D directly in your browser.  
5. **Dynamic Property Mapping** – Automatically map IFC properties based on your configurations.  
6. **Model Inspection** – Explore and analyze the properties and quantities of your IFC models.  
7. **Create Project timeline** – Create project schedules directly IFC model for 4D simulations.  
8. **Draft Bill of Quantities** – Extract quantities and measurements from your IFC models for cost estimation.  
9. **Export to Excel** – Export your configurations, rules, and model data to Excel for further analysis.  
10. **Reports** – Generate reports summarizing your model and rule information.  
11. **User-Friendly Interface** – Navigate through the app with an intuitive and easy-to-use design.

---
### 🧭 How to Use

- Use the **sidebar navigation menù** to move between different pages of the application.  
- Each page corresponds to a `.py` file in your `/pages` directory.  
- Any updates or rules you create are automatically stored and can be exported for reuse.

---
### 💡 Tips
            
- Start with IFC Export Configuration to define your export rules before creating or validating models.
- The IDS Creator and Validation Tools work best together — create your IDS rules first, then validate your IFC models against them.
- Keep IFC file names short and descriptive (e.g., Structure_Model_IFC4.ifc).
- Large IFC files (>100MB) may take longer to load — consider simplifying your model first.
- When exporting, check that your property sets (Psets) and quantities (Qto) are properly mapped in your configuration.
- Keep your browser window wide open for the best display experience.

---
### ⚙️ Technical Note
This app is built with **Streamlit** and integrates with **IfcOpenShell** and **web-ifc** for IFC processing.
- Regularly clear the cache or restart Streamlit if the app behaves unexpectedly.
- For optimal performance, use the latest version of Google Chrome or Microsoft Edge.
- Remember: this is an OpenBIM platform — everything is meant to stay interoperable and transparent.
""")

# Footer
st.markdown("---")
st.markdown("© 2025 – BIM45D | Developed by Riccardo Padoan, RSP Group. | Visit [https://github.com/riccardopadoan28/THESIS.git] for more details.")
st.markdown("All rights reserved. | This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).")