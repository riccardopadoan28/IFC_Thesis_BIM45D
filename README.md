# IFC_Thesis_BIM45D

A Streamlit application for viewing and analyzing IFC models with 4 toolkits: Model Viewer, Health Checker, Quantity Visualiser, and DataFrame Visualiser (with Excel/CSV export).

## Getting Started

### Prerequisites
- Python 3.x installed
- pip installed
- (Optional) A virtual environment

### Installation
1) Clone this repository and navigate into it.
2) (Optional) Create and activate a virtual environment:
   - Windows:
     ```bash
     py -m venv .venv
     .venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```
3) Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Run the Application
```bash
python -m streamlit run Home.py
```

## How to Use

### Load a File
- Click Browse File and select an .ifc file.

### Navigation (Sidebar Toolkits)
1) Model Viewer
   - Explore and inspect the IFC model.
2) Model Health Checker
   - Run basic quality and consistency checks.
3) Quantity Visualiser
   - Visualize quantities derived from the model.
4) DataFrame Visualiser
   - View tabular data and export to Excel or CSV.


### High-level Steps
1) Home: Import an IFC file.
2) Validate IFC: Apply IDS rules (automatic IDS test) and export IDS XML output.
3) BCF Collaboration: Create issues and export review/issue reports.
4) Model Health Checker: Run quality and consistency checks.
5) 3D Model Viewer: Explore and inspect the model geometry.
6) Model Properties & Quantities: Inspect properties/quantities; export DataFrame to CSV/Excel and HTML reports.
7) Scheduling & Planning: Derive project timeline; export schedule to CSV/HTML.
8) Cost Estimation: Export Bill of Quantities (CSV).
9) Optional: Extract BIMQ/IFC configuration JSON.


---
If you encounter issues, ensure dependencies are installed correctly and that your Python environment is active before running the app.