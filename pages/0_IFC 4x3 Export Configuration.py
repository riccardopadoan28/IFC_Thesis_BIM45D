# ─────────────────────────────────────────────
# 📦 Imports (standardized)
# ─────────────────────────────────────────────
import streamlit as st
from tools import p0_export_config as p0  # per-page helper
from tools import p_shared as shared  # shared model info helpers
import json
from tools.ifc_432_dictionary import IFC_STRUCTURAL_DICTIONARY_4x3
from tools.pathhelper import save_text

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
# ⚙️ Pagina principale
# ─────────────────────────────────────────────
st.set_page_config(page_title="⚙️ IFC Export Configuration", layout="wide")
st.title("⚙️ IFC Export Configuration")

# Brief English summary
st.markdown("""
This page helps you create IFC4x3 export configurations for BIM authoring tools.
Configure general export settings, geometry level-of-detail, georeferencing, and which IFC entities to include.
Utilize the form below and add export rules in the sidebar.
Export a ready-to-use JSON file to import into IFC exporters.
""")

# Reference to IFC4.3 documentation
st.markdown("Reference: [IFC4.3 Documentation - buildingSMART](https://ifc43-docs.standards.buildingsmart.org/)")

# ─────────────────────────────────────────────
# 🔁 Inizializzazione session_state
# ─────────────────────────────────────────────
if "export_rules" not in st.session_state:
    st.session_state.export_rules = []

if "ifc_settings" not in st.session_state:
    st.session_state.ifc_settings = {
        "IFCVersion": 29,
        "ExchangeRequirement": 3,
        "FacilityType": 0,
        "FacilityPredefinedType": None,
        "CategoryMapping": None,
        "IFCFileType": 0,
        "ActivePhaseId": -1,
        "SpaceBoundaries": 0,
        "SplitWallsAndColumns": True,
        "IncludeSteelElements": True,
        "ProjectAddress": {
            "UpdateProjectInformation": False,
            "AssignAddressToSite": False,
            "AssignAddressToBuilding": True
        },
        "Export2DElements": False,
        "ExportLinkedFiles": 0,
        "VisibleElementsOfCurrentView": False,
        "ExportRoomsInView": False,
        "ExportInternalRevitPropertySets": True,
        "ExportIFCCommonPropertySets": True,
        "ExportBaseQuantities": True,
        "ExportCeilingGrids": False,
        "ExportMaterialPsets": True,
        "ExportSchedulesAsPsets": True,
        "ExportSpecificSchedules": True,
        "ExportUserDefinedPsets": True,
        "ExportUserDefinedPsetsFileName": "",
        "UseTypePropertiesInInstacePSets": False,
        "ExportUserDefinedParameterMapping": False,
        "ExportUserDefinedParameterMappingFileName": "",
        "ClassificationSettings": {
            "ClassificationName": None,
            "ClassificationEdition": None,
            "ClassificationSource": None,
            "ClassificationEditionDate": "/Date(-62135596800000)/",
            "ClassificationLocation": None,
            "ClassificationFieldName": None
        },
        "TessellationLevelOfDetail": 1.0,
        "ExportPartsAsBuildingElements": False,
        "ExportSolidModelRep": False,
        "UseActiveViewGeometry": False,
        "UseFamilyAndTypeNameForReference": False,
        "Use2DRoomBoundaryForVolume": False,
        "IncludeSiteElevation": False,
        "StoreIFCGUID": True,
        "ExportBoundingBox": False,
        "UseOnlyTriangulation": False,
        "UseTypeNameOnlyForIfcType": False,
        "ExportHostAsSingleEntity": False,
        "OwnerHistoryLastModified": False,
        "ExportBarsInUniformSetsAsSeparateIFCEntities": True,
        "UseVisibleRevitNameAsEntityName": True,
        "SelectedSite": "Default Site",
        "SitePlacement": 0,
        "GeoRefCRSName": "",
        "GeoRefCRSDesc": "",
        "GeoRefEPSGCode": "",
        "GeoRefGeodeticDatum": "",
        "GeoRefMapUnit": "",
        "ExcludeFilter": "",
        "COBieCompanyInfo": "",
        "COBieProjectInfo": "",
        "Name": "Configurazione IFC - IFC4x3_Prova"
    }

# ─────────────────────────────────────────────
# 📚 Funzione dizionario IFC4X3
# ─────────────────────────────────────────────
def get_dictionary():
    return IFC_STRUCTURAL_DICTIONARY_4x3

# ─────────────────────────────────────────────
# 📌 Funzione per IFC4X3
# ─────────────────────────────────────────────
def render_ifc4x3_settings():
    # ──────────────────────────────
    # Nome configurazione
    # ──────────────────────────────
    st.session_state.ifc_settings["Name"] = st.text_input(
        "Configuration Name",
        value=st.session_state.ifc_settings.get("Name","Configurazione IFC - IFC4x3_Prova"),
        help="Enter a name for this IFC export configuration."
    )

    # ──────────────────────────────
    # Sezione 1: Generale
    # ──────────────────────────────
    st.markdown("### 1️⃣ General")
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.ifc_settings["ExchangeRequirement"] = st.selectbox(
            "Exchange Requirement",
            options=[0,1,2,3],
            index=st.session_state.ifc_settings.get("ExchangeRequirement",2),
            help="Select the exchange requirement level for the IFC export."
        )
    with col2:
        st.session_state.ifc_settings["IFCFileType"] = st.selectbox(
            "IFC File Type",
            options=["IFC","IFC XML","IFC Compressed","IFC XML Compressed"],
            index=0,
            help="Select the output file type for the IFC export."
        )
    col3, col4 = st.columns(2)
    with col3:
        st.session_state.ifc_settings["ActivePhaseId"] = st.selectbox(
            "Phase to Export",
            options=["Default","Existing","New Construction"],
            index=0,
            help="Select which project phase to export."
        )
    with col4:
        st.session_state.ifc_settings["SpaceBoundaries"] = st.selectbox(
            "Space Boundaries",
            options=["None","First Level","Second Level"],
            index=0,
            help="Select the level of space boundaries to export."
        )
    st.session_state.ifc_settings["FacilityType"] = st.selectbox(
        "Facility Type",
        options=["IfcBridge","IfcBuilding","IfcMarineFacility","IfcRailway","IfcRoad"],
        index=1,
        help="Select the type of facility being exported."
    )

    # ──────────────────────────────
    # Sezione 2: Livello di dettaglio
    # ──────────────────────────────
    st.markdown("### 2️⃣ Level of Detail")
    lod_options = {"Very Coarse":0.25,"Coarse":0.50,"Medium":0.75,"Fine":1.0}
    selected_lod_name = st.selectbox(
        "Level of Detail for Geometry Elements",
        options=list(lod_options.keys()),
        index=2,
        help="Select the level of geometric detail for elements."
    )
    st.session_state.ifc_settings["TessellationLevelOfDetail"] = lod_options[selected_lod_name]

    # ──────────────────────────────
    # Sezione 3: Contenuti aggiuntivi
    # ──────────────────────────────
    st.markdown("### 3️⃣ Additional Content")

    st.session_state.ifc_settings["ExportLinkedFiles"] = st.selectbox(
            "Linked Files",
            options=["Do Not Export","Export as Separate IFC","Export in Same IfcProject","Export in Same IfcSite"],
            index=0,
            help="Choose how linked files should be exported."
        )
    
    col5, col6 = st.columns(2)
    with col5:
        st.session_state.ifc_settings["VisibleElementsOfCurrentView"] = st.checkbox(
            "Export Only Visible Elements in View",
            value=st.session_state.ifc_settings.get("VisibleElementsOfCurrentView",False),
            help="If checked, only visible elements in the current view will be exported."
        )
    st.session_state.ifc_settings["Export2DElements"] = st.checkbox(
        "Export 2D Plan View Elements",
        value=st.session_state.ifc_settings.get("Export2DElements",False),
        help="Include 2D plan view elements in the export."
    )
    st.session_state.ifc_settings["ExportCeilingGrids"] = st.checkbox(
        "Export Ceiling Grids",
        value=st.session_state.ifc_settings.get("ExportCeilingGrids",False),
        help="Include ceiling grids in the export."
    )
    with col6:
        if st.session_state.ifc_settings["VisibleElementsOfCurrentView"]:
            st.session_state.ifc_settings["ExportRoomsInView"] = st.checkbox(
                "Export Rooms, Areas and Spaces in 3D Views",
                value=st.session_state.ifc_settings.get("ExportRoomsInView",False),
                help="If checked, rooms, areas, and spaces visible in 3D views will be exported."
            )

    # ──────────────────────────────
    # Sezione 4: Riferimento geografico
    # ──────────────────────────────
    st.markdown("### 4️⃣ Georeferencing")

    # Site Placement
    site_placement_options = {
        0: "Shared Coordinates",
        1: "Survey Point",
        2: "Project Base Point",
        3: "Internal Origin",
        4: "Project Base Point Oriented to True North",
        5: "Internal Origin Oriented to True North"
    }

    st.session_state.ifc_settings["SitePlacement"] = st.selectbox(
        "Site Placement",
        options=list(site_placement_options.keys()),
        format_func=lambda x: site_placement_options[x],
        index=st.session_state.ifc_settings.get("SitePlacement", 0),
        help="Select how the project coordinates are referenced geographically."
    )

    # ──────────────────────────────
    # Sezione 5: Advanced
    # ──────────────────────────────
    st.markdown("### 5️⃣ Advanced")

    col1, col2 = st.columns(2)
    with col1:
        st.session_state.ifc_settings["UseTypeNameOnlyForIfcType"] = st.checkbox(
            "Use Type Name only for IFCType",
            value=st.session_state.ifc_settings.get("UseTypeNameOnlyForIfcType", False),
            help="If checked, only the type name will be used for the IFCType."
        )
        st.session_state.ifc_settings["UseVisibleRevitNameAsEntityName"] = st.checkbox(
            "Use Revit Visible Name as IFCEntity Name",
            value=st.session_state.ifc_settings.get("UseVisibleRevitNameAsEntityName", False),
            help="If checked, the visible name in Revit will be used as the IFCEntity name."
        )
        st.session_state.ifc_settings["ExportHostAsSingleEntity"] = st.checkbox(
            "Export Floors and Roofs as Single IFC Entity",
            value=st.session_state.ifc_settings.get("ExportHostAsSingleEntity", False),
            help="If checked, floors and roofs will always be exported as single IFC entities."
        )

    with col2:
        st.session_state.ifc_settings["OwnerHistoryLastModified"] = st.checkbox(
            "Set LastModified User to Project Author",
            value=st.session_state.ifc_settings.get("OwnerHistoryLastModified", False),
            help="If checked, the 'LastModified' user will be set to the project author."
        )
        st.session_state.ifc_settings["ExportBarsInUniformSetsAsSeparateIFCEntities"] = st.checkbox(
            "Export Bars in Uniform Sets as Separate IFC Entities",
            value=st.session_state.ifc_settings.get("ExportBarsInUniformSetsAsSeparateIFCEntities", False),
            help="If checked, bars in uniform reinforcement sets will be exported as separate IFC entities."
        )

    # Pulsante per collegamento al tab delle Export Rules
    st.markdown("### 🗂️ Entities to Export - Use the Export Rule creator in the Sidebar and scroll down to manage export rules.")


# ─────────────────────────────────────────────
# 🧩 Tabs principali
# ─────────────────────────────────────────────
tab_general, tab_json = st.tabs(["General Export Settings", "JSON Output"])

# ─────────────────────────────────────────────
# 🏗️ TAB 1: General Export Settings
# ─────────────────────────────────────────────
with tab_general:
    render_ifc4x3_settings()

# ─────────────────────────────────────────────
# 🧱 Sidebar: IFC Export Rules
# ─────────────────────────────────────────────
all_ifc_entities = [
        "IfcProduct","IfcElement","IfcBuiltElement","IfcBeam","IfcBearing","IfcBuildingElementProxy",
        "IfcChimney","IfcColumn","IfcCourse","IfcCovering","IfcCurtainWall","IfcDeepFoundation",
        "IfcCaissonFoundation","IfcPile","IfcDoor","IfcEarthworksElement","IfcEarthworksFill",
        "IfcReinforcedSoil","IfcFooting","IfcKerb","IfcMember","IfcMooringDevice","IfcNavigationElement",
        "IfcPavement","IfcPlate","IfcRail","IfcRailing","IfcRamp","IfcRampFlight","IfcRoof","IfcShadingDevice",
        "IfcSlab","IfcStair","IfcStairFlight","IfcTrackElement","IfcWall","IfcWindow","IfcCivilElement",
        "IfcDistributionElement","IfcDistributionControlElement","IfcActuator","IfcAlarm","IfcController",
        "IfcFlowInstrument","IfcProtectiveDeviceTrippingUnit","IfcSensor","IfcUnitaryControlElement",
        "IfcDistributionFlowElement","IfcDistributionChamberElement","IfcEnergyConversionDevice",
        "IfcAirToAirHeatRecovery","IfcBoiler","IfcBurner","IfcChiller","IfcCoil","IfcCondenser","IfcCooledBeam",
        "IfcCoolingTower","IfcElectricGenerator","IfcElectricMotor","IfcEngine","IfcEvaporativeCooler",
        "IfcEvaporator","IfcHeatExchanger","IfcHumidifier","IfcMotorConnection","IfcSolarDevice","IfcTransformer",
        "IfcTubeBundle","IfcUnitaryEquipment","IfcFlowController","IfcAirTerminalBox","IfcDamper",
        "IfcDistributionBoard","IfcElectricDistributionBoard","IfcElectricTimeControl","IfcFlowMeter",
        "IfcProtectiveDevice","IfcSwitchingDevice","IfcValve","IfcFlowFitting","IfcCableCarrierFitting",
        "IfcCableFitting","IfcDuctFitting","IfcJunctionBox","IfcPipeFitting","IfcFlowMovingDevice",
        "IfcCompressor","IfcFan","IfcPump","IfcFlowSegment","IfcCableCarrierSegment","IfcCableSegment",
        "IfcConveyorSegment","IfcDuctSegment","IfcPipeSegment","IfcFlowStorageDevice","IfcElectricFlowStorageDevice",
        "IfcTank","IfcFlowTerminal","IfcAirTerminal","IfcAudioVisualAppliance","IfcCommunicationsAppliance",
        "IfcElectricAppliance","IfcFireSuppressionTerminal","IfcLamp","IfcLightFixture","IfcLiquidTerminal",
        "IfcMedicalDevice","IfcMobileTelecommunicationsAppliance","IfcOutlet","IfcSanitaryTerminal","IfcSignal",
        "IfcSpaceHeater","IfcStackTerminal","IfcWasteTerminal","IfcFlowTreatmentDevice","IfcDuctSilencer",
        "IfcElectricFlowTreatmentDevice","IfcFilter","IfcInterceptor","IfcElementAssembly","IfcElementComponent",
        "IfcBuildingElementPart","IfcDiscreteAccessory","IfcFastener","IfcImpactProtectionDevice",
        "IfcMechanicalFastener","IfcReinforcingElement","IfcReinforcingBar","IfcReinforcingMesh","IfcTendonAnchor",
        "IfcTendonConduit","IfcTendon","IfcSign","IfcVibrationDamper","IfcVibrationIsolator","IfcFurnishingElement",
        "IfcFurniture","IfcSystemFurnitureElement","IfcGeographicElement","IfcTransportationDevice","IfcTransportElement",
        "IfcVehicle","IfcSpatialElement","IfcSpatialStructureElement","IfcSpace","IfcSpatialZone","IfcGroup","IfcAsset",
        "IfcInventory","IfcStructuralLoadGroup","IfcStructuralLoadCase","IfcStructuralResultGroup","IfcSystem",
        "IfcBuildingSystem","IfcBuiltSystem","IfcDistributionSystem","IfcDistributionCircuit","IfcStructuralAnalysisModel",
        "IfcZone"
]

with st.sidebar:
    st.subheader("➕ Select Entities to Export")

    # Dizionario etichette visibili → codici IFC
    ifc_entities_dict = {e: e for e in all_ifc_entities}  # Nome visibile = codice IFC

    # Multiselect: selezioni ciò che vuoi includere
    selected_labels = st.multiselect(
        "Select IFC Entities to include in export (leave empty to export all)",
        options=list(ifc_entities_dict.keys()),
        default=None,
    )

    # Calcolo delle entità da escludere
    if selected_labels:
        selected_ifc_entities = [ifc_entities_dict[label] for label in selected_labels]
        excluded_ifc_entities = [v for v in all_ifc_entities if v not in selected_ifc_entities]
        # 🔹 Non mettere virgolette: separatore ;
        exclude_filter = ';'.join(excluded_ifc_entities)
    else:
        exclude_filter = ""  # Esporta tutto

    # Aggiorna session_state
    st.session_state.ifc_settings["ExcludeFilter"] = exclude_filter

    # Mostra anteprima nel sidebar
    st.text_area("ExcludeFilter JSON Value:", exclude_filter, height=150)


# ─────────────────────────────────────────────
# 🧾 TAB 3: JSON Output
# ─────────────────────────────────────────────
with tab_json:
    st.subheader("Export Configuration JSON")
    export_config = st.session_state.ifc_settings.copy()
    export_config["ExportRules"] = st.session_state.export_rules
    json_str = json.dumps(export_config, indent=4)
    st.code(json_str, language="json")

    if st.button("Download configuration (save to temp_file)", key="btn_dl_export_config"):
        try:
            fname = f"export_config_{st.session_state.ifc_settings['Name'].replace(' ','_')}.json"
            path, url = save_text(fname, json_str)
            st.success(f"Saved in static/temp_file — {path.name}")
            st.markdown(f"[Click to download]({url})")
        except Exception as e:
            st.error(f"Unable to save: {e}")

# Uniform page structure applied. If you still have direct ifcopenshell logic here, consider moving it into the corresponding tools module (p0..p8) for consistency.
