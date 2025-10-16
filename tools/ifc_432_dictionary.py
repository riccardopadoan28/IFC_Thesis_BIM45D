# utils/ifc_structural_dictionary.py
# Dizionario IFC strutturale completo (IFC4.3.2)
# Serve come riferimento per menu a tendina e suggerimenti, senza limitare la ricerca effettiva

IFC_STRUCTURAL_DICTIONARY_4x3= {

    "IfcBeam": {
        "Pset_BeamCommon": [
            "Reference","Status","Span","Slope","Roll","IsExternal","ThermalTransmittance",
            "LoadBearing","FireRating"
        ],
        "Pset_ConcreteElementGeneral": [
            "AssemblyPlace","CastingMethod","StructuralClass","StrengthClass","ExposureClass",
            "ReinforcementVolumeRatio","ReinforcementAreaRatio","DimensionalAccuracyClass",
            "ConstructionToleranceClass","ConcreteCover","ConcreteCoverAtMainBars","ConcreteCoverAtLinks",
            "ReinforcementStrengthClass"
        ],
        "Pset_Condition": [
            "AssessmentDate","AssessmentCondition","AssessmentDescription","AssessmentType",
            "AssessmentMethod","LastAssessmentReport","NextAssessmentDate","AssessmentFrequency"
        ],
        "Pset_ConstructionAdministration": ["ProcurementMethod","SpecificationSectionNumber","SubmittalIdentifer"],
        "Pset_ConstructionOccurence": ["InstallationDate","ModelNumber","TagNumber","AssetIdentifier"],
        "Pset_ElementKinematics": ["CyclicPath","CyclicRange","LinearPath","LinearRange","MaximumAngularVelocity","MaximumConstantSpeed","MinimumTime"],
        "Pset_EnvironmentalCondition": [
            "ReferenceAirRelativeHumidity","ReferenceEnvironmentTemperature","MaximumAtmosphericPressure",
            "StorageTemperatureRange","MaximumWindSpeed","OperationalTemperatureRange","MaximumRainIntensity",
            "SaltMistLevel","SeismicResistance","SmokeLevel","MaximumSolarRadiation"
        ],
        "Pset_EnvironmentalImpactIndicators": [
            "Reference","FunctionalUnitReference","IndicatorsUnit","LifeCyclePhase","ExpectedServiceLife",
            "TotalPrimaryEnergyConsumptionPerUnit","WaterConsumptionPerUnit","HazardousWastePerUnit",
            "NonHazardousWastePerUnit","ClimateChangePerUnit","AtmosphericAcidificationPerUnit",
            "RenewableEnergyConsumptionPerUnit","NonRenewableEnergyConsumptionPerUnit","ResourceDepletionPerUnit",
            "InertWastePerUnit","RadioactiveWastePerUnit","StratosphericOzoneLayerDestructionPerUnit",
            "PhotochemicalOzoneFormationPerUnit","EutrophicationPerUnit"
        ],
        "Pset_EnvironmentalImpactValues": [
            "TotalPrimaryEnergyConsumption","WaterConsumption","HazardousWaste","NonHazardousWaste",
            "ClimateChange","AtmosphericAcidification","RenewableEnergyConsumption","NonRenewableEnergyConsumption",
            "ResourceDepletion","InertWaste","RadioactiveWaste","StratosphericOzoneLayerDestruction",
            "PhotochemicalOzoneFormation","Eutrophication","LeadInTime","Duration","LeadOutTime"
        ],
        "Pset_InstallationOccurrence": ["InstallationDate","AcceptanceDate","PutIntoOperationDate"],
        "Pset_MaintenanceStrategy": ["AssetCriticality","AssetFrailty","AssetPriority","MonitoringType","AccidentResponse"],
        "Pset_MaintenanceTriggerCondition": ["ConditionTargetPerformance","ConditionMaintenanceLevel","ConditionReplacementLevel","ConditionDisposalLevel"],
        "Pset_MaintenanceTriggerDuration": ["DurationTargetPerformance","DurationMaintenanceLevel","DurationReplacementLevel","DurationDisposalLevel"],
        "Pset_MaintenanceTriggerPerformance": ["TargetPerformance","PerformanceMaintenanceLevel","ReplacementLevel","DisposalLevel"],
        "Pset_ManufacturerOccurrence": ["AcquisitionDate","BarCode","SerialNumber","BatchReference","AssemblyPlace","ManufacturingDate"],
        "Pset_ManufacturerTypeInformation": ["GlobalTradeItemNumber","ArticleNumber","ModelReference","ModelLabel","Manufacturer","ProductionYear","AssemblyPlace","OperationalDocument","SafetyDocument","PerformanceCertificate"],
        "Pset_PrecastConcreteElementFabrication": ["TypeDesignation","ProductionLotId","SerialNumber","PieceMark","AsBuiltLocationNumber","ActualProductionDate","ActualErectionDate"],
        "Pset_PrecastConcreteElementGeneral": [
            "TypeDesignation","CornerChamfer","ManufacturingToleranceClass","FormStrippingStrength",
            "LiftingStrength","ReleaseStrength","MinimumAllowableSupportLength","InitialTension",
            "TendonRelaxation","TransportationStrength","SupportDuringTransportDescription",
            "SupportDuringTransportDocReference","HollowCorePlugging","CamberAtMidspan","BatterAtStart",
            "BatterAtEnd","Twisting","Shortening","PieceMark","DesignLocationNumber"
        ],
        "Pset_ReinforcementBarPitchOfBeam": ["Description","Reference","StirrupBarPitch","SpacingBarPitch"],
        "Pset_RepairOccurrence": ["RepairContent","RepairDate","MeanTimeToRepair"],
        "Pset_Risk": [
            "RiskName","RiskType","NatureOfRisk","RiskAssessmentMethodology","UnmitigatedRiskLikelihood",
            "UnmitigatedRiskConsequence","UnmitigatedRiskSignificance","MitigationPlanned","MitigatedRiskLikelihood",
            "MitigatedRiskConsequence","MitigatedRiskSignificance","MitigationProposed","AssociatedProduct",
            "AssociatedActivity","AssociatedLocation"
        ],
        "Pset_ServiceLife": ["ServiceLifeDuration","MeanTimeBetweenFailure"],
        "Pset_Tolerance": [
            "ToleranceDescription","ToleranceBasis","OverallTolerance","HorizontalTolerance","OrthogonalTolerance",
            "VerticalTolerance","PlanarFlatness","HorizontalFlatness","ElevationalFlatness","SideFlatness",
            "OverallOrthogonality","HorizontalOrthogonality","OrthogonalOrthogonality","VerticalOrthogonality",
            "OverallStraightness","HorizontalStraightness","OrthogonalStraightness","VerticalStraightness"
        ],
        "Pset_Uncertainty": ["UncertaintyBasis","UncertaintyDescription","HorizontalUncertainty","LinearUncertainty","OrthogonalUncertainty","VerticalUncertainty"],
        "Pset_Warranty": ["WarrantyIdentifier","WarrantyStartDate","IsExtendedWarranty","WarrantyPeriod","WarrantyContent","PointOfContact","Exclusions"],
        "Qto_BeamBaseQuantities": ["Length","CrossSectionArea","OuterSurfaceArea","GrossSurfaceArea","NetSurfaceArea","GrossVolume","NetVolume","GrossWeight","NetWeight"],
        "Qto_BodyGeometryValidation": ["GrossSurfaceArea","NetSurfaceArea","GrossVolume"]
    },


    "IfcColumn": {
        "Pset_ColumnCommon": [
            "Reference", "Status", "Slope", "Roll", "IsExternal", 
            "ThermalTransmittance", "LoadBearing", "FireRating"
        ],
        "Pset_ConcreteElementGeneral": [
            "AssemblyPlace", "CastingMethod", "StructuralClass", "StrengthClass",
            "ExposureClass", "ReinforcementVolumeRatio", "ReinforcementAreaRatio",
            "DimensionalAccuracyClass", "ConstructionToleranceClass", "ConcreteCover",
            "ConcreteCoverAtMainBars", "ConcreteCoverAtLinks", "ReinforcementStrengthClass"
        ],
        "Pset_Condition": [
            "AssessmentDate", "AssessmentCondition", "AssessmentDescription",
            "AssessmentType", "AssessmentMethod", "LastAssessmentReport",
            "NextAssessmentDate", "AssessmentFrequency"
        ],
        "Pset_ConstructionAdministration": [
            "ProcurementMethod", "SpecificationSectionNumber", "SubmittalIdentifer"
        ],
        "Pset_ConstructionOccurence": [
            "InstallationDate", "ModelNumber", "TagNumber", "AssetIdentifier"
        ],
        "Pset_ElementKinematics": [
            "CyclicPath", "CyclicRange", "LinearPath", "LinearRange", 
            "MaximumAngularVelocity", "MaximumConstantSpeed", "MinimumTime"
        ],
        "Pset_EnvironmentalCondition": [
            "ReferenceAirRelativeHumidity", "ReferenceEnvironmentTemperature", 
            "MaximumAtmosphericPressure", "StorageTemperatureRange", 
            "MaximumWindSpeed", "OperationalTemperatureRange", 
            "MaximumRainIntensity", "SaltMistLevel", "SeismicResistance",
            "SmokeLevel", "MaximumSolarRadiation"
        ],
        "Pset_EnvironmentalImpactIndicators": [
            "Reference", "FunctionalUnitReference", "IndicatorsUnit", "LifeCyclePhase",
            "ExpectedServiceLife", "TotalPrimaryEnergyConsumptionPerUnit", "WaterConsumptionPerUnit",
            "HazardousWastePerUnit", "NonHazardousWastePerUnit", "ClimateChangePerUnit",
            "AtmosphericAcidificationPerUnit", "RenewableEnergyConsumptionPerUnit",
            "NonRenewableEnergyConsumptionPerUnit", "ResourceDepletionPerUnit", "InertWastePerUnit",
            "RadioactiveWastePerUnit", "StratosphericOzoneLayerDestructionPerUnit",
            "PhotochemicalOzoneFormationPerUnit", "EutrophicationPerUnit"
        ],
        "Pset_EnvironmentalImpactValues": [
            "TotalPrimaryEnergyConsumption", "WaterConsumption", "HazardousWaste",
            "NonHazardousWaste", "ClimateChange", "AtmosphericAcidification",
            "RenewableEnergyConsumption", "NonRenewableEnergyConsumption", "ResourceDepletion",
            "InertWaste", "RadioactiveWaste", "StratosphericOzoneLayerDestruction",
            "PhotochemicalOzoneFormation", "Eutrophication", "LeadInTime", "Duration", "LeadOutTime"
        ],
        "Pset_InstallationOccurrence": [
            "InstallationDate", "AcceptanceDate", "PutIntoOperationDate"
        ],
        "Pset_MaintenanceStrategy": [
            "AssetCriticality", "AssetFrailty", "AssetPriority", "MonitoringType", "AccidentResponse"
        ],
        "Pset_MaintenanceTriggerCondition": [
            "ConditionTargetPerformance", "ConditionMaintenanceLevel", "ConditionReplacementLevel", "ConditionDisposalLevel"
        ],
        "Pset_MaintenanceTriggerDuration": [
            "DurationTargetPerformance", "DurationMaintenanceLevel", "DurationReplacementLevel", "DurationDisposalLevel"
        ],
        "Pset_MaintenanceTriggerPerformance": [
            "TargetPerformance", "PerformanceMaintenanceLevel", "ReplacementLevel", "DisposalLevel"
        ],
        "Pset_ManufacturerOccurrence": [
            "AcquisitionDate", "BarCode", "SerialNumber", "BatchReference",
            "AssemblyPlace", "ManufacturingDate"
        ],
        "Pset_ManufacturerTypeInformation": [
            "GlobalTradeItemNumber", "ArticleNumber", "ModelReference", "ModelLabel",
            "Manufacturer", "ProductionYear", "AssemblyPlace", "OperationalDocument",
            "SafetyDocument", "PerformanceCertificate"
        ],
        "Pset_PrecastConcreteElementFabrication": [
            "TypeDesignation", "ProductionLotId", "SerialNumber", "PieceMark",
            "AsBuiltLocationNumber", "ActualProductionDate", "ActualErectionDate"
        ],
        "Pset_PrecastConcreteElementGeneral": [
            "TypeDesignation", "CornerChamfer", "ManufacturingToleranceClass", "FormStrippingStrength",
            "LiftingStrength", "ReleaseStrength", "MinimumAllowableSupportLength", "InitialTension",
            "TendonRelaxation", "TransportationStrength", "SupportDuringTransportDescription",
            "SupportDuringTransportDocReference", "HollowCorePlugging", "CamberAtMidspan",
            "BatterAtStart", "BatterAtEnd", "Twisting", "Shortening", "PieceMark", "DesignLocationNumber"
        ],
        "Pset_ReinforcementBarPitchOfColumn": [
            "Description", "Reference", "ReinforcementBarType", "HoopBarPitch",
            "XDirectionTieHoopBarPitch", "XDirectionTieHoopCount", "YDirectionTieHoopBarPitch",
            "YDirectionTieHoopCount"
        ],
        "Pset_RepairOccurrence": [
            "RepairContent", "RepairDate", "MeanTimeToRepair"
        ],
        "Pset_Risk": [
            "RiskName", "RiskType", "NatureOfRisk", "RiskAssessmentMethodology",
            "UnmitigatedRiskLikelihood", "UnmitigatedRiskConsequence", "UnmitigatedRiskSignificance",
            "MitigationPlanned", "MitigatedRiskLikelihood", "MitigatedRiskConsequence",
            "MitigatedRiskSignificance", "MitigationProposed", "AssociatedProduct",
            "AssociatedActivity", "AssociatedLocation"
        ],
        "Pset_ServiceLife": [
            "ServiceLifeDuration", "MeanTimeBetweenFailure"
        ],
        "Pset_Tolerance": [
            "ToleranceDescription", "ToleranceBasis", "OverallTolerance", "HorizontalTolerance",
            "OrthogonalTolerance", "VerticalTolerance", "PlanarFlatness", "HorizontalFlatness",
            "ElevationalFlatness", "SideFlatness", "OverallOrthogonality", "HorizontalOrthogonality",
            "OrthogonalOrthogonality", "VerticalOrthogonality", "OverallStraightness",
            "HorizontalStraightness", "OrthogonalStraightness", "VerticalStraightness"
        ],
        "Pset_Uncertainty": [
            "UncertaintyBasis", "UncertaintyDescription", "HorizontalUncertainty",
            "LinearUncertainty", "OrthogonalUncertainty", "VerticalUncertainty"
        ],
        "Pset_Warranty": [
            "WarrantyIdentifier", "WarrantyStartDate", "IsExtendedWarranty",
            "WarrantyPeriod", "WarrantyContent", "PointOfContact", "Exclusions"
        ],
        "Qto_BodyGeometryValidation": [
            "GrossSurfaceArea", "NetSurfaceArea", "GrossVolume", "NetVolume",
            "SurfaceGenusBeforeFeatures", "SurfaceGenusAfterFeatures"
        ],
        "Qto_ColumnBaseQuantities": [
            "Length", "CrossSectionArea", "OuterSurfaceArea"
        ]
    },


    "IfcMember": {
        "Pset_ConcreteElementGeneral": [
            "AssemblyPlace", "CastingMethod", "StructuralClass", "StrengthClass",
            "ExposureClass", "ReinforcementVolumeRatio", "ReinforcementAreaRatio",
            "DimensionalAccuracyClass", "ConstructionToleranceClass", "ConcreteCover",
            "ConcreteCoverAtMainBars", "ConcreteCoverAtLinks", "ReinforcementStrengthClass"
        ],
        "Pset_Condition": [
            "AssessmentDate", "AssessmentCondition", "AssessmentDescription",
            "AssessmentType", "AssessmentMethod", "LastAssessmentReport",
            "NextAssessmentDate", "AssessmentFrequency"
        ],
        "Pset_ConstructionAdministration": [
            "ProcurementMethod", "SpecificationSectionNumber", "SubmittalIdentifer"
        ],
        "Pset_ConstructionOccurence": [
            "InstallationDate", "ModelNumber", "TagNumber", "AssetIdentifier"
        ],
        "Pset_DoorLiningProperties": [
            "LiningDepth", "LiningThickness", "ThresholdDepth", "ThresholdThickness",
            "TransomThickness", "TransomOffset", "LiningOffset", "ThresholdOffset",
            "CasingThickness", "CasingDepth", "LiningToPanelOffsetX", "LiningToPanelOffsetY"
        ],
        "Pset_ElementKinematics": [
            "CyclicPath", "CyclicRange", "LinearPath", "LinearRange",
            "MaximumAngularVelocity", "MaximumConstantSpeed", "MinimumTime"
        ],
        "Pset_EnvironmentalCondition": [
            "ReferenceAirRelativeHumidity", "ReferenceEnvironmentTemperature",
            "MaximumAtmosphericPressure", "StorageTemperatureRange", "MaximumWindSpeed",
            "OperationalTemperatureRange", "MaximumRainIntensity", "SaltMistLevel",
            "SeismicResistance", "SmokeLevel", "MaximumSolarRadiation"
        ],
        "Pset_EnvironmentalImpactIndicators": [
            "Reference", "FunctionalUnitReference", "IndicatorsUnit", "LifeCyclePhase",
            "ExpectedServiceLife", "TotalPrimaryEnergyConsumptionPerUnit", "WaterConsumptionPerUnit",
            "HazardousWastePerUnit", "NonHazardousWastePerUnit", "ClimateChangePerUnit",
            "AtmosphericAcidificationPerUnit", "RenewableEnergyConsumptionPerUnit",
            "NonRenewableEnergyConsumptionPerUnit", "ResourceDepletionPerUnit", "InertWastePerUnit",
            "RadioactiveWastePerUnit", "StratosphericOzoneLayerDestructionPerUnit",
            "PhotochemicalOzoneFormationPerUnit", "EutrophicationPerUnit"
        ],
        "Pset_EnvironmentalImpactValues": [
            "TotalPrimaryEnergyConsumption", "WaterConsumption", "HazardousWaste",
            "NonHazardousWaste", "ClimateChange", "AtmosphericAcidification",
            "RenewableEnergyConsumption", "NonRenewableEnergyConsumption", "ResourceDepletion",
            "InertWaste", "RadioactiveWaste", "StratosphericOzoneLayerDestruction",
            "PhotochemicalOzoneFormation", "Eutrophication", "LeadInTime", "Duration", "LeadOutTime"
        ],
        "Pset_InstallationOccurrence": [
            "InstallationDate", "AcceptanceDate", "PutIntoOperationDate"
        ],
        "Pset_MaintenanceStrategy": [
            "AssetCriticality", "AssetFrailty", "AssetPriority", "MonitoringType", "AccidentResponse"
        ],
        "Pset_MaintenanceTriggerCondition": [
            "ConditionTargetPerformance", "ConditionMaintenanceLevel", "ConditionReplacementLevel",
            "ConditionDisposalLevel"
        ],
        "Pset_MaintenanceTriggerDuration": [
            "DurationTargetPerformance", "DurationMaintenanceLevel", "DurationReplacementLevel",
            "DurationDisposalLevel"
        ],
        "Pset_MaintenanceTriggerPerformance": [
            "TargetPerformance", "PerformanceMaintenanceLevel", "ReplacementLevel", "DisposalLevel"
        ],
        "Pset_ManufacturerOccurrence": [
            "AcquisitionDate", "BarCode", "SerialNumber", "BatchReference", "AssemblyPlace", "ManufacturingDate"
        ],
        "Pset_ManufacturerTypeInformation": [
            "GlobalTradeItemNumber", "ArticleNumber", "ModelReference", "ModelLabel", "Manufacturer",
            "ProductionYear", "AssemblyPlace", "OperationalDocument", "SafetyDocument", "PerformanceCertificate"
        ],
        "Pset_MemberCommon": [
            "Reference", "Status", "Span", "Slope", "Roll", "IsExternal",
            "ThermalTransmittance", "LoadBearing", "FireRating"
        ],
        "Pset_MemberTypeAnchoringBar": [
            "MechanicalStressType", "HasLightningRod"
        ],
        "Pset_MemberTypeCatenaryStay": [
            "AssemblyInstruction", "NominalLength", "CatenaryStayType", "NominalHeight"
        ],
        "Pset_MemberTypeOCSRigidSupport": [
            "AssemblyInstruction", "ContactWireStagger"
        ],
        "Pset_MemberTypePost": [
            "NominalHeight", "ConicityRatio", "LoadBearingCapacity", "WindLoadRating",
            "TorsionalStrength", "BendingStrength"
        ],
        "Pset_MemberTypeTieBar": [
            "IsTemporaryInstallation"
        ],
        "Pset_PermeableCoveringProperties": [
            "OperationType", "PanelPosition", "FrameDepth", "FrameThickness"
        ],
        "Pset_PrecastConcreteElementFabrication": [
            "TypeDesignation", "ProductionLotId", "SerialNumber", "PieceMark",
            "AsBuiltLocationNumber", "ActualProductionDate", "ActualErectionDate"
        ],
        "Pset_PrecastConcreteElementGeneral": [
            "TypeDesignation", "CornerChamfer", "ManufacturingToleranceClass", "FormStrippingStrength",
            "LiftingStrength", "ReleaseStrength", "MinimumAllowableSupportLength", "InitialTension",
            "TendonRelaxation", "TransportationStrength", "SupportDuringTransportDescription",
            "SupportDuringTransportDocReference", "HollowCorePlugging", "CamberAtMidspan",
            "BatterAtStart", "BatterAtEnd", "Twisting", "Shortening", "PieceMark", "DesignLocationNumber"
        ],
        "Pset_RepairOccurrence": [
            "RepairContent", "RepairDate", "MeanTimeToRepair"
        ],
        "Pset_Risk": [
            "RiskName", "RiskType", "NatureOfRisk", "RiskAssessmentMethodology",
            "UnmitigatedRiskLikelihood", "UnmitigatedRiskConsequence", "UnmitigatedRiskSignificance",
            "MitigationPlanned", "MitigatedRiskLikelihood", "MitigatedRiskConsequence",
            "MitigatedRiskSignificance", "MitigationProposed", "AssociatedProduct",
            "AssociatedActivity", "AssociatedLocation"
        ],
        "Pset_ServiceLife": [
            "ServiceLifeDuration", "MeanTimeBetweenFailure"
        ],
        "Pset_Tolerance": [
            "ToleranceDescription", "ToleranceBasis", "OverallTolerance", "HorizontalTolerance",
            "OrthogonalTolerance", "VerticalTolerance", "PlanarFlatness", "HorizontalFlatness",
            "ElevationalFlatness", "SideFlatness", "OverallOrthogonality", "HorizontalOrthogonality",
            "OrthogonalOrthogonality", "VerticalOrthogonality", "OverallStraightness",
            "HorizontalStraightness", "OrthogonalStraightness", "VerticalStraightness"
        ],
        "Pset_Uncertainty": [
            "UncertaintyBasis", "UncertaintyDescription", "HorizontalUncertainty",
            "LinearUncertainty", "OrthogonalUncertainty", "VerticalUncertainty"
        ],
        "Pset_Warranty": [
            "WarrantyIdentifier", "WarrantyStartDate", "IsExtendedWarranty",
            "WarrantyPeriod", "WarrantyContent", "PointOfContact", "Exclusions"
        ],
        "Pset_WindowLiningProperties": [
            "LiningDepth", "LiningThickness", "TransomThickness", "MullionThickness",
            "FirstTransomOffset", "SecondTransomOffset", "FirstMullionOffset", "SecondMullionOffset",
            "LiningOffset", "LiningToPanelOffsetX", "LiningToPanelOffsetY"
        ],
        "Qto_BodyGeometryValidation": [
            "GrossSurfaceArea", "NetSurfaceArea", "GrossVolume", "NetVolume",
            "SurfaceGenusBeforeFeatures", "SurfaceGenusAfterFeatures"
        ],
        "Qto_MemberBaseQuantities": [
            "Length", "CrossSectionArea", "OuterSurfaceArea"
        ]
    },


    "IfcSlab": {
        "Pset_CessBetweenRails": [
            "JointRelativePosition", "CheckRailType", "LoadCapacity", "UsagePurpose"
        ],
        "Pset_ConcreteElementGeneral": [
            "AssemblyPlace", "CastingMethod", "StructuralClass", "StrengthClass",
            "ExposureClass", "ReinforcementVolumeRatio", "ReinforcementAreaRatio",
            "DimensionalAccuracyClass", "ConstructionToleranceClass", "ConcreteCover",
            "ConcreteCoverAtMainBars", "ConcreteCoverAtLinks", "ReinforcementStrengthClass"
        ],
        "Pset_Condition": [
            "AssessmentDate", "AssessmentCondition", "AssessmentDescription",
            "AssessmentType", "AssessmentMethod", "LastAssessmentReport",
            "NextAssessmentDate", "AssessmentFrequency"
        ],
        "Pset_ConstructionAdministration": [
            "ProcurementMethod", "SpecificationSectionNumber", "SubmittalIdentifer"
        ],
        "Pset_ConstructionOccurence": [
            "InstallationDate", "ModelNumber", "TagNumber", "AssetIdentifier"
        ],
        "Pset_ElementKinematics": [
            "CyclicPath", "CyclicRange", "LinearPath", "LinearRange",
            "MaximumAngularVelocity", "MaximumConstantSpeed", "MinimumTime"
        ],
        "Pset_EmbeddedTrack": [
            "IsAccessibleByVehicle", "HasDrainage", "PermissibleRoadLoad"
        ],
        "Pset_EnvironmentalCondition": [
            "ReferenceAirRelativeHumidity", "ReferenceEnvironmentTemperature",
            "MaximumAtmosphericPressure", "StorageTemperatureRange", "MaximumWindSpeed",
            "OperationalTemperatureRange", "MaximumRainIntensity", "SaltMistLevel",
            "SeismicResistance", "SmokeLevel", "MaximumSolarRadiation"
        ],
        "Pset_EnvironmentalImpactIndicators": [
            "Reference", "FunctionalUnitReference", "IndicatorsUnit", "LifeCyclePhase",
            "ExpectedServiceLife", "TotalPrimaryEnergyConsumptionPerUnit", "WaterConsumptionPerUnit",
            "HazardousWastePerUnit", "NonHazardousWastePerUnit", "ClimateChangePerUnit",
            "AtmosphericAcidificationPerUnit", "RenewableEnergyConsumptionPerUnit",
            "NonRenewableEnergyConsumptionPerUnit", "ResourceDepletionPerUnit", "InertWastePerUnit",
            "RadioactiveWastePerUnit", "StratosphericOzoneLayerDestructionPerUnit",
            "PhotochemicalOzoneFormationPerUnit", "EutrophicationPerUnit"
        ],
        "Pset_EnvironmentalImpactValues": [
            "TotalPrimaryEnergyConsumption", "WaterConsumption", "HazardousWaste",
            "NonHazardousWaste", "ClimateChange", "AtmosphericAcidification",
            "RenewableEnergyConsumption", "NonRenewableEnergyConsumption", "ResourceDepletion",
            "InertWaste", "RadioactiveWaste", "StratosphericOzoneLayerDestruction",
            "PhotochemicalOzoneFormation", "Eutrophication", "LeadInTime", "Duration", "LeadOutTime"
        ],
        "Pset_InstallationOccurrence": [
            "InstallationDate", "AcceptanceDate", "PutIntoOperationDate"
        ],
        "Pset_MaintenanceStrategy": [
            "AssetCriticality", "AssetFrailty", "AssetPriority", "MonitoringType", "AccidentResponse"
        ],
        "Pset_MaintenanceTriggerCondition": [
            "ConditionTargetPerformance", "ConditionMaintenanceLevel", "ConditionReplacementLevel",
            "ConditionDisposalLevel"
        ],
        "Pset_MaintenanceTriggerDuration": [
            "DurationTargetPerformance", "DurationMaintenanceLevel", "DurationReplacementLevel",
            "DurationDisposalLevel"
        ],
        "Pset_MaintenanceTriggerPerformance": [
            "TargetPerformance", "PerformanceMaintenanceLevel", "ReplacementLevel", "DisposalLevel"
        ],
        "Pset_ManufacturerOccurrence": [
            "AcquisitionDate", "BarCode", "SerialNumber", "BatchReference", "AssemblyPlace", "ManufacturingDate"
        ],
        "Pset_ManufacturerTypeInformation": [
            "GlobalTradeItemNumber", "ArticleNumber", "ModelReference", "ModelLabel", "Manufacturer",
            "ProductionYear", "AssemblyPlace", "OperationalDocument", "SafetyDocument", "PerformanceCertificate"
        ],
        "Pset_PrecastConcreteElementFabrication": [
            "TypeDesignation", "ProductionLotId", "SerialNumber", "PieceMark",
            "AsBuiltLocationNumber", "ActualProductionDate", "ActualErectionDate"
        ],
        "Pset_PrecastConcreteElementGeneral": [
            "TypeDesignation", "CornerChamfer", "ManufacturingToleranceClass", "FormStrippingStrength",
            "LiftingStrength", "ReleaseStrength", "MinimumAllowableSupportLength", "InitialTension",
            "TendonRelaxation", "TransportationStrength", "SupportDuringTransportDescription",
            "SupportDuringTransportDocReference", "HollowCorePlugging", "CamberAtMidspan",
            "BatterAtStart", "BatterAtEnd", "Twisting", "Shortening", "PieceMark", "DesignLocationNumber"
        ],
        "Pset_PrecastSlab": [
            "TypeDesignation", "ToppingType", "EdgeDistanceToFirstAxis", "DistanceBetweenComponentAxes",
            "AngleToFirstAxis", "AngleBetweenComponentAxes", "NominalThickness", "NominalToppingThickness"
        ],
        "Pset_ReinforcementBarPitchOfSlab": [
            "Description", "Reference", "LongOutsideTopBarPitch", "LongInsideCenterTopBarPitch",
            "LongInsideEndTopBarPitch", "ShortOutsideTopBarPitch", "ShortInsideCenterTopBarPitch",
            "ShortInsideEndTopBarPitch", "LongOutsideLowerBarPitch", "LongInsideCenterLowerBarPitch",
            "LongInsideEndLowerBarPitch", "ShortOutsideLowerBarPitch", "ShortInsideCenterLowerBarPitch",
            "ShortInsideEndLowerBarPitch"
        ],
        "Pset_RepairOccurrence": [
            "RepairContent", "RepairDate", "MeanTimeToRepair"
        ],
        "Pset_Risk": [
            "RiskName", "RiskType", "NatureOfRisk", "RiskAssessmentMethodology",
            "UnmitigatedRiskLikelihood", "UnmitigatedRiskConsequence", "UnmitigatedRiskSignificance",
            "MitigationPlanned", "MitigatedRiskLikelihood", "MitigatedRiskConsequence",
            "MitigatedRiskSignificance", "MitigationProposed", "AssociatedProduct",
            "AssociatedActivity", "AssociatedLocation"
        ],
        "Pset_ServiceLife": [
            "ServiceLifeDuration", "MeanTimeBetweenFailure"
        ],
        "Pset_SlabCommon": [
            "Reference", "Status", "AcousticRating", "FireRating", "PitchAngle", "Combustible",
            "SurfaceSpreadOfFlame", "Compartmentation", "IsExternal", "ThermalTransmittance", "LoadBearing"
        ],
        "Pset_SlabTypeTrackSlab": [
            "TechnicalStandard"
        ],
        "Pset_Tolerance": [
            "ToleranceDescription", "ToleranceBasis", "OverallTolerance", "HorizontalTolerance",
            "OrthogonalTolerance", "VerticalTolerance", "PlanarFlatness", "HorizontalFlatness",
            "ElevationalFlatness", "SideFlatness", "OverallOrthogonality", "HorizontalOrthogonality",
            "OrthogonalOrthogonality", "VerticalOrthogonality", "OverallStraightness",
            "HorizontalStraightness", "OrthogonalStraightness", "VerticalStraightness"
        ],
        "Pset_TrackBase": [
            "IsSurfaceGalling", "SurfaceGallingArea"
        ],
        "Pset_Uncertainty": [
            "UncertaintyBasis", "UncertaintyDescription", "HorizontalUncertainty",
            "LinearUncertainty", "OrthogonalUncertainty", "VerticalUncertainty"
        ],
        "Pset_Warranty": [
            "WarrantyIdentifier", "WarrantyStartDate", "IsExtendedWarranty",
            "WarrantyPeriod", "WarrantyContent", "PointOfContact", "Exclusions"
        ],
        "Qto_BodyGeometryValidation": [
            "GrossSurfaceArea", "NetSurfaceArea", "GrossVolume", "NetVolume",
            "SurfaceGenusBeforeFeatures", "SurfaceGenusAfterFeatures"
        ],
        "Qto_SlabBaseQuantities": [
            "Width", "Length", "Depth"
        ]
    },


    "IfcWall": {
        "Pset_ConcreteElementGeneral": [
            "AssemblyPlace", "CastingMethod", "StructuralClass", "StrengthClass",
            "ExposureClass", "ReinforcementVolumeRatio", "ReinforcementAreaRatio",
            "DimensionalAccuracyClass", "ConstructionToleranceClass", "ConcreteCover",
            "ConcreteCoverAtMainBars", "ConcreteCoverAtLinks", "ReinforcementStrengthClass"
        ],
        "Pset_Condition": [
            "AssessmentDate", "AssessmentCondition", "AssessmentDescription",
            "AssessmentType", "AssessmentMethod", "LastAssessmentReport",
            "NextAssessmentDate", "AssessmentFrequency"
        ],
        "Pset_ConstructionAdministration": [
            "ProcurementMethod", "SpecificationSectionNumber", "SubmittalIdentifer"
        ],
        "Pset_ConstructionOccurence": [
            "InstallationDate", "ModelNumber", "TagNumber", "AssetIdentifier"
        ],
        "Pset_ElementKinematics": [
            "CyclicPath", "CyclicRange", "LinearPath", "LinearRange",
            "MaximumAngularVelocity", "MaximumConstantSpeed", "MinimumTime"
        ],
        "Pset_EnvironmentalCondition": [
            "ReferenceAirRelativeHumidity", "ReferenceEnvironmentTemperature",
            "MaximumAtmosphericPressure", "StorageTemperatureRange", "MaximumWindSpeed",
            "OperationalTemperatureRange", "MaximumRainIntensity", "SaltMistLevel",
            "SeismicResistance", "SmokeLevel", "MaximumSolarRadiation"
        ],
        "Pset_EnvironmentalImpactIndicators": [
            "Reference", "FunctionalUnitReference", "IndicatorsUnit", "LifeCyclePhase",
            "ExpectedServiceLife", "TotalPrimaryEnergyConsumptionPerUnit", "WaterConsumptionPerUnit",
            "HazardousWastePerUnit", "NonHazardousWastePerUnit", "ClimateChangePerUnit",
            "AtmosphericAcidificationPerUnit", "RenewableEnergyConsumptionPerUnit",
            "NonRenewableEnergyConsumptionPerUnit", "ResourceDepletionPerUnit", "InertWastePerUnit",
            "RadioactiveWastePerUnit", "StratosphericOzoneLayerDestructionPerUnit",
            "PhotochemicalOzoneFormationPerUnit", "EutrophicationPerUnit"
        ],
        "Pset_EnvironmentalImpactValues": [
            "TotalPrimaryEnergyConsumption", "WaterConsumption", "HazardousWaste",
            "NonHazardousWaste", "ClimateChange", "AtmosphericAcidification",
            "RenewableEnergyConsumption", "NonRenewableEnergyConsumption", "ResourceDepletion",
            "InertWaste", "RadioactiveWaste", "StratosphericOzoneLayerDestruction",
            "PhotochemicalOzoneFormation", "Eutrophication", "LeadInTime", "Duration", "LeadOutTime"
        ],
        "Pset_InstallationOccurrence": [
            "InstallationDate", "AcceptanceDate", "PutIntoOperationDate"
        ],
        "Pset_MaintenanceStrategy": [
            "AssetCriticality", "AssetFrailty", "AssetPriority", "MonitoringType", "AccidentResponse"
        ],
        "Pset_MaintenanceTriggerCondition": [
            "ConditionTargetPerformance", "ConditionMaintenanceLevel", "ConditionReplacementLevel",
            "ConditionDisposalLevel"
        ],
        "Pset_MaintenanceTriggerDuration": [
            "DurationTargetPerformance", "DurationMaintenanceLevel", "DurationReplacementLevel",
            "DurationDisposalLevel"
        ],
        "Pset_MaintenanceTriggerPerformance": [
            "TargetPerformance", "PerformanceMaintenanceLevel", "ReplacementLevel", "DisposalLevel"
        ],
        "Pset_ManufacturerOccurrence": [
            "AcquisitionDate", "BarCode", "SerialNumber", "BatchReference", "AssemblyPlace", "ManufacturingDate"
        ],
        "Pset_ManufacturerTypeInformation": [
            "GlobalTradeItemNumber", "ArticleNumber", "ModelReference", "ModelLabel", "Manufacturer",
            "ProductionYear", "AssemblyPlace", "OperationalDocument", "SafetyDocument", "PerformanceCertificate"
        ],
        "Pset_PrecastConcreteElementFabrication": [
            "TypeDesignation", "ProductionLotId", "SerialNumber", "PieceMark",
            "AsBuiltLocationNumber", "ActualProductionDate", "ActualErectionDate"
        ],
        "Pset_PrecastConcreteElementGeneral": [
            "TypeDesignation", "CornerChamfer", "ManufacturingToleranceClass", "FormStrippingStrength",
            "LiftingStrength", "ReleaseStrength", "MinimumAllowableSupportLength", "InitialTension",
            "TendonRelaxation", "TransportationStrength", "SupportDuringTransportDescription",
            "SupportDuringTransportDocReference", "HollowCorePlugging", "CamberAtMidspan",
            "BatterAtStart", "BatterAtEnd", "Twisting", "Shortening", "PieceMark", "DesignLocationNumber"
        ],
        "Pset_ReinforcementBarPitchOfWall": [
            "Description", "Reference", "BarAllocationType", "VerticalBarPitch",
            "HorizontalBarPitch", "SpacingBarPitch"
        ],
        "Pset_RepairOccurrence": [
            "RepairContent", "RepairDate", "MeanTimeToRepair"
        ],
        "Pset_Risk": [
            "RiskName", "RiskType", "NatureOfRisk", "RiskAssessmentMethodology",
            "UnmitigatedRiskLikelihood", "UnmitigatedRiskConsequence", "UnmitigatedRiskSignificance",
            "MitigationPlanned", "MitigatedRiskLikelihood", "MitigatedRiskConsequence",
            "MitigatedRiskSignificance", "MitigationProposed", "AssociatedProduct",
            "AssociatedActivity", "AssociatedLocation"
        ],
        "Pset_RoadGuardElement": [
            "IsMoveable", "IsTerminal", "IsTransition", "TerminalType"
        ],
        "Pset_ServiceLife": [
            "ServiceLifeDuration", "MeanTimeBetweenFailure"
        ],
        "Pset_Tolerance": [
            "ToleranceDescription", "ToleranceBasis", "OverallTolerance", "HorizontalTolerance",
            "OrthogonalTolerance", "VerticalTolerance", "PlanarFlatness", "HorizontalFlatness",
            "ElevationalFlatness", "SideFlatness", "OverallOrthogonality", "HorizontalOrthogonality",
            "OrthogonalOrthogonality", "VerticalOrthogonality", "OverallStraightness",
            "HorizontalStraightness", "OrthogonalStraightness", "VerticalStraightness"
        ],
        "Pset_Uncertainty": [
            "UncertaintyBasis", "UncertaintyDescription", "HorizontalUncertainty",
            "LinearUncertainty", "OrthogonalUncertainty", "VerticalUncertainty"
        ],
        "Pset_WallCommon": [
            "Reference", "Status", "AcousticRating", "FireRating", "Combustible",
            "SurfaceSpreadOfFlame", "ThermalTransmittance", "IsExternal", "LoadBearing",
            "ExtendToStructure", "Compartmentation"
        ],
        "Pset_Warranty": [
            "WarrantyIdentifier", "WarrantyStartDate", "IsExtendedWarranty",
            "WarrantyPeriod", "WarrantyContent", "PointOfContact", "Exclusions"
        ],
        "Qto_BodyGeometryValidation": [
            "GrossSurfaceArea", "NetSurfaceArea", "GrossVolume", "NetVolume",
            "SurfaceGenusBeforeFeatures", "SurfaceGenusAfterFeatures"
        ],
        "Qto_WallBaseQuantities": [
            "Length", "Width", "Height", "GrossFootPrintArea", "NetFootPrintArea",
            "GrossSideArea", "NetSideArea", "GrossVolume", "NetVolume", "GrossWeight", "NetWeight"
        ]
    }, 


    "IfcPlate": {
        "Pset_ConcreteElementGeneral": [
            "AssemblyPlace", "CastingMethod", "StructuralClass", "StrengthClass",
            "ExposureClass", "ReinforcementVolumeRatio", "ReinforcementAreaRatio",
            "DimensionalAccuracyClass", "ConstructionToleranceClass", "ConcreteCover",
            "ConcreteCoverAtMainBars", "ConcreteCoverAtLinks", "ReinforcementStrengthClass"
        ],
        "Pset_Condition": [
            "AssessmentDate", "AssessmentCondition", "AssessmentDescription",
            "AssessmentType", "AssessmentMethod", "LastAssessmentReport",
            "NextAssessmentDate", "AssessmentFrequency"
        ],
        "Pset_ConstructionAdministration": [
            "ProcurementMethod", "SpecificationSectionNumber", "SubmittalIdentifer"
        ],
        "Pset_ConstructionOccurence": [
            "InstallationDate", "ModelNumber", "TagNumber", "AssetIdentifier"
        ],
        "Pset_DoorPanelProperties": [
            "PanelDepth", "PanelOperation", "PanelWidth", "PanelPosition"
        ],
        "Pset_ElementKinematics": [
            "CyclicPath", "CyclicRange", "LinearPath", "LinearRange",
            "MaximumAngularVelocity", "MaximumConstantSpeed", "MinimumTime"
        ],
        "Pset_EnvironmentalCondition": [
            "ReferenceAirRelativeHumidity", "ReferenceEnvironmentTemperature",
            "MaximumAtmosphericPressure", "StorageTemperatureRange", "MaximumWindSpeed",
            "OperationalTemperatureRange", "MaximumRainIntensity", "SaltMistLevel",
            "SeismicResistance", "SmokeLevel", "MaximumSolarRadiation"
        ],
        "Pset_EnvironmentalImpactIndicators": [
            "Reference", "FunctionalUnitReference", "IndicatorsUnit", "LifeCyclePhase",
            "ExpectedServiceLife", "TotalPrimaryEnergyConsumptionPerUnit", "WaterConsumptionPerUnit",
            "HazardousWastePerUnit", "NonHazardousWastePerUnit", "ClimateChangePerUnit",
            "AtmosphericAcidificationPerUnit", "RenewableEnergyConsumptionPerUnit",
            "NonRenewableEnergyConsumptionPerUnit", "ResourceDepletionPerUnit", "InertWastePerUnit",
            "RadioactiveWastePerUnit", "StratosphericOzoneLayerDestructionPerUnit",
            "PhotochemicalOzoneFormationPerUnit", "EutrophicationPerUnit"
        ],
        "Pset_EnvironmentalImpactValues": [
            "TotalPrimaryEnergyConsumption", "WaterConsumption", "HazardousWaste",
            "NonHazardousWaste", "ClimateChange", "AtmosphericAcidification",
            "RenewableEnergyConsumption", "NonRenewableEnergyConsumption", "ResourceDepletion",
            "InertWaste", "RadioactiveWaste", "StratosphericOzoneLayerDestruction",
            "PhotochemicalOzoneFormation", "Eutrophication", "LeadInTime", "Duration", "LeadOutTime"
        ],
        "Pset_InstallationOccurrence": [
            "InstallationDate", "AcceptanceDate", "PutIntoOperationDate"
        ],
        "Pset_MaintenanceStrategy": [
            "AssetCriticality", "AssetFrailty", "AssetPriority", "MonitoringType", "AccidentResponse"
        ],
        "Pset_MaintenanceTriggerCondition": [
            "ConditionTargetPerformance", "ConditionMaintenanceLevel", "ConditionReplacementLevel",
            "ConditionDisposalLevel"
        ],
        "Pset_MaintenanceTriggerDuration": [
            "DurationTargetPerformance", "DurationMaintenanceLevel", "DurationReplacementLevel",
            "DurationDisposalLevel"
        ],
        "Pset_MaintenanceTriggerPerformance": [
            "TargetPerformance", "PerformanceMaintenanceLevel", "ReplacementLevel", "DisposalLevel"
        ],
        "Pset_ManufacturerOccurrence": [
            "AcquisitionDate", "BarCode", "SerialNumber", "BatchReference", "AssemblyPlace", "ManufacturingDate"
        ],
        "Pset_ManufacturerTypeInformation": [
            "GlobalTradeItemNumber", "ArticleNumber", "ModelReference", "ModelLabel", "Manufacturer",
            "ProductionYear", "AssemblyPlace", "OperationalDocument", "SafetyDocument", "PerformanceCertificate"
        ],
        "Pset_PlateCommon": [
            "Reference", "Status", "AcousticRating", "IsExternal", "ThermalTransmittance",
            "LoadBearing", "FireRating"
        ],
        "Pset_PrecastConcreteElementFabrication": [
            "TypeDesignation", "ProductionLotId", "SerialNumber", "PieceMark",
            "AsBuiltLocationNumber", "ActualProductionDate", "ActualErectionDate"
        ],
        "Pset_PrecastConcreteElementGeneral": [
            "TypeDesignation", "CornerChamfer", "ManufacturingToleranceClass", "FormStrippingStrength",
            "LiftingStrength", "ReleaseStrength", "MinimumAllowableSupportLength", "InitialTension",
            "TendonRelaxation", "TransportationStrength", "SupportDuringTransportDescription",
            "SupportDuringTransportDocReference", "HollowCorePlugging", "CamberAtMidspan",
            "BatterAtStart", "BatterAtEnd", "Twisting", "Shortening", "PieceMark", "DesignLocationNumber"
        ],
        "Pset_RepairOccurrence": [
            "RepairContent", "RepairDate", "MeanTimeToRepair"
        ],
        "Pset_Risk": [
            "RiskName", "RiskType", "NatureOfRisk", "RiskAssessmentMethodology",
            "UnmitigatedRiskLikelihood", "UnmitigatedRiskConsequence", "UnmitigatedRiskSignificance",
            "MitigationPlanned", "MitigatedRiskLikelihood", "MitigatedRiskConsequence",
            "MitigatedRiskSignificance", "MitigationProposed", "AssociatedProduct",
            "AssociatedActivity", "AssociatedLocation"
        ],
        "Pset_ServiceLife": [
            "ServiceLifeDuration", "MeanTimeBetweenFailure"
        ],
        "Pset_Tolerance": [
            "ToleranceDescription", "ToleranceBasis", "OverallTolerance", "HorizontalTolerance",
            "OrthogonalTolerance", "VerticalTolerance", "PlanarFlatness", "HorizontalFlatness",
            "ElevationalFlatness", "SideFlatness", "OverallOrthogonality", "HorizontalOrthogonality",
            "OrthogonalOrthogonality", "VerticalOrthogonality", "OverallStraightness",
            "HorizontalStraightness", "OrthogonalStraightness", "VerticalStraightness"
        ],
        "Pset_Uncertainty": [
            "UncertaintyBasis", "UncertaintyDescription", "HorizontalUncertainty",
            "LinearUncertainty", "OrthogonalUncertainty", "VerticalUncertainty"
        ],
        "Pset_Warranty": [
            "WarrantyIdentifier", "WarrantyStartDate", "IsExtendedWarranty",
            "WarrantyPeriod", "WarrantyContent", "PointOfContact", "Exclusions"
        ],
        "Pset_WindowPanelProperties": [
            "OperationType", "PanelPosition", "FrameDepth", "FrameThickness"
        ],
        "Qto_BodyGeometryValidation": [
            "GrossSurfaceArea", "NetSurfaceArea", "GrossVolume", "NetVolume",
            "SurfaceGenusBeforeFeatures", "SurfaceGenusAfterFeatures"
        ],
        "Qto_PlateBaseQuantities": [
            "Width", "Perimeter", "GrossArea"
        ]
    },


    "IfcFooting": {
        "Pset_ConcreteElementGeneral": [
            "AssemblyPlace", "CastingMethod", "StructuralClass", "StrengthClass",
            "ExposureClass", "ReinforcementVolumeRatio", "ReinforcementAreaRatio",
            "DimensionalAccuracyClass", "ConstructionToleranceClass", "ConcreteCover",
            "ConcreteCoverAtMainBars", "ConcreteCoverAtLinks", "ReinforcementStrengthClass"
        ],
        "Pset_Condition": [
            "AssessmentDate", "AssessmentCondition", "AssessmentDescription",
            "AssessmentType", "AssessmentMethod", "LastAssessmentReport",
            "NextAssessmentDate", "AssessmentFrequency"
        ],
        "Pset_ConstructionAdministration": [
            "ProcurementMethod", "SpecificationSectionNumber", "SubmittalIdentifer"
        ],
        "Pset_ConstructionOccurence": [
            "InstallationDate", "ModelNumber", "TagNumber", "AssetIdentifier"
        ],
        "Pset_ElementKinematics": [
            "CyclicPath", "CyclicRange", "LinearPath", "LinearRange",
            "MaximumAngularVelocity", "MaximumConstantSpeed", "MinimumTime"
        ],
        "Pset_EnvironmentalCondition": [
            "ReferenceAirRelativeHumidity", "ReferenceEnvironmentTemperature",
            "MaximumAtmosphericPressure", "StorageTemperatureRange", "MaximumWindSpeed",
            "OperationalTemperatureRange", "MaximumRainIntensity", "SaltMistLevel",
            "SeismicResistance", "SmokeLevel", "MaximumSolarRadiation"
        ],
        "Pset_EnvironmentalImpactIndicators": [
            "Reference", "FunctionalUnitReference", "IndicatorsUnit", "LifeCyclePhase",
            "ExpectedServiceLife", "TotalPrimaryEnergyConsumptionPerUnit", "WaterConsumptionPerUnit",
            "HazardousWastePerUnit", "NonHazardousWastePerUnit", "ClimateChangePerUnit",
            "AtmosphericAcidificationPerUnit", "RenewableEnergyConsumptionPerUnit",
            "NonRenewableEnergyConsumptionPerUnit", "ResourceDepletionPerUnit", "InertWastePerUnit",
            "RadioactiveWastePerUnit", "StratosphericOzoneLayerDestructionPerUnit",
            "PhotochemicalOzoneFormationPerUnit", "EutrophicationPerUnit"
        ],
        "Pset_EnvironmentalImpactValues": [
            "TotalPrimaryEnergyConsumption", "WaterConsumption", "HazardousWaste",
            "NonHazardousWaste", "ClimateChange", "AtmosphericAcidification",
            "RenewableEnergyConsumption", "NonRenewableEnergyConsumption", "ResourceDepletion",
            "InertWaste", "RadioactiveWaste", "StratosphericOzoneLayerDestruction",
            "PhotochemicalOzoneFormation", "Eutrophication", "LeadInTime", "Duration", "LeadOutTime"
        ],
        "Pset_FootingCommon": [
            "Reference", "Status", "LoadBearing"
        ],
        "Pset_FootingTypePadFooting": [
            "LoadBearingCapacity", "IsReinforced"
        ],
        "Pset_InstallationOccurrence": [
            "InstallationDate", "AcceptanceDate", "PutIntoOperationDate"
        ],
        "Pset_MaintenanceStrategy": [
            "AssetCriticality", "AssetFrailty", "AssetPriority", "MonitoringType", "AccidentResponse"
        ],
        "Pset_MaintenanceTriggerCondition": [
            "ConditionTargetPerformance", "ConditionMaintenanceLevel", "ConditionReplacementLevel",
            "ConditionDisposalLevel"
        ],
        "Pset_MaintenanceTriggerDuration": [
            "DurationTargetPerformance", "DurationMaintenanceLevel", "DurationReplacementLevel",
            "DurationDisposalLevel"
        ],
        "Pset_MaintenanceTriggerPerformance": [
            "TargetPerformance", "PerformanceMaintenanceLevel", "ReplacementLevel", "DisposalLevel"
        ],
        "Pset_ManufacturerOccurrence": [
            "AcquisitionDate", "BarCode", "SerialNumber", "BatchReference", "AssemblyPlace", "ManufacturingDate"
        ],
        "Pset_ManufacturerTypeInformation": [
            "GlobalTradeItemNumber", "ArticleNumber", "ModelReference", "ModelLabel", "Manufacturer",
            "ProductionYear", "AssemblyPlace", "OperationalDocument", "SafetyDocument", "PerformanceCertificate"
        ],
        "Pset_PrecastConcreteElementFabrication": [
            "TypeDesignation", "ProductionLotId", "SerialNumber", "PieceMark",
            "AsBuiltLocationNumber", "ActualProductionDate", "ActualErectionDate"
        ],
        "Pset_PrecastConcreteElementGeneral": [
            "TypeDesignation", "CornerChamfer", "ManufacturingToleranceClass", "FormStrippingStrength",
            "LiftingStrength", "ReleaseStrength", "MinimumAllowableSupportLength", "InitialTension",
            "TendonRelaxation", "TransportationStrength", "SupportDuringTransportDescription",
            "SupportDuringTransportDocReference", "HollowCorePlugging", "CamberAtMidspan",
            "BatterAtStart", "BatterAtEnd", "Twisting", "Shortening", "PieceMark", "DesignLocationNumber"
        ],
        "Pset_ReinforcementBarCountOfIndependentFooting": [
            "Description", "Reference", "XDirectionLowerBarCount", "YDirectionLowerBarCount",
            "XDirectionUpperBarCount", "YDirectionUpperBarCount"
        ],
        "Pset_ReinforcementBarPitchOfContinuousFooting": [
            "Description", "Reference", "CrossingUpperBarPitch", "CrossingLowerBarPitch"
        ],
        "Pset_RepairOccurrence": [
            "RepairContent", "RepairDate", "MeanTimeToRepair"
        ],
        "Pset_Risk": [
            "RiskName", "RiskType", "NatureOfRisk", "RiskAssessmentMethodology",
            "UnmitigatedRiskLikelihood", "UnmitigatedRiskConsequence", "UnmitigatedRiskSignificance",
            "MitigationPlanned", "MitigatedRiskLikelihood", "MitigatedRiskConsequence",
            "MitigatedRiskSignificance", "MitigationProposed", "AssociatedProduct",
            "AssociatedActivity", "AssociatedLocation"
        ],
        "Pset_ServiceLife": [
            "ServiceLifeDuration", "MeanTimeBetweenFailure"
        ],
        "Pset_Tolerance": [
            "ToleranceDescription", "ToleranceBasis", "OverallTolerance", "HorizontalTolerance",
            "OrthogonalTolerance", "VerticalTolerance", "PlanarFlatness", "HorizontalFlatness",
            "ElevationalFlatness", "SideFlatness", "OverallOrthogonality", "HorizontalOrthogonality",
            "OrthogonalOrthogonality", "VerticalOrthogonality", "OverallStraightness",
            "HorizontalStraightness", "OrthogonalStraightness", "VerticalStraightness"
        ],
        "Pset_Uncertainty": [
            "UncertaintyBasis", "UncertaintyDescription", "HorizontalUncertainty",
            "LinearUncertainty", "OrthogonalUncertainty", "VerticalUncertainty"
        ],
        "Pset_Warranty": [
            "WarrantyIdentifier", "WarrantyStartDate", "IsExtendedWarranty",
            "WarrantyPeriod", "WarrantyContent", "PointOfContact", "Exclusions"
        ],
        "Qto_BodyGeometryValidation": [
            "GrossSurfaceArea", "NetSurfaceArea", "GrossVolume", "NetVolume",
            "SurfaceGenusBeforeFeatures", "SurfaceGenusAfterFeatures"
        ],
        "Qto_FootingBaseQuantities": [
            "Length", "Width", "Height"
        ]
    },


    "IfcRoof":  {
        "Pset_ConcreteElementGeneral": [
            "AssemblyPlace", "CastingMethod", "StructuralClass", "StrengthClass",
            "ExposureClass", "ReinforcementVolumeRatio", "ReinforcementAreaRatio",
            "DimensionalAccuracyClass", "ConstructionToleranceClass", "ConcreteCover",
            "ConcreteCoverAtMainBars", "ConcreteCoverAtLinks", "ReinforcementStrengthClass"
        ],
        "Pset_Condition": [
            "AssessmentDate", "AssessmentCondition", "AssessmentDescription",
            "AssessmentType", "AssessmentMethod", "LastAssessmentReport",
            "NextAssessmentDate", "AssessmentFrequency"
        ],
        "Pset_ConstructionAdministration": [
            "ProcurementMethod", "SpecificationSectionNumber", "SubmittalIdentifer"
        ],
        "Pset_ConstructionOccurence": [
            "InstallationDate", "ModelNumber", "TagNumber", "AssetIdentifier"
        ],
        "Pset_ElementKinematics": [
            "CyclicPath", "CyclicRange", "LinearPath", "LinearRange",
            "MaximumAngularVelocity", "MaximumConstantSpeed", "MinimumTime"
        ],
        "Pset_EnvironmentalCondition": [
            "ReferenceAirRelativeHumidity", "ReferenceEnvironmentTemperature",
            "MaximumAtmosphericPressure", "StorageTemperatureRange", "MaximumWindSpeed",
            "OperationalTemperatureRange", "MaximumRainIntensity", "SaltMistLevel",
            "SeismicResistance", "SmokeLevel", "MaximumSolarRadiation"
        ],
        "Pset_EnvironmentalImpactIndicators": [
            "Reference", "FunctionalUnitReference", "IndicatorsUnit", "LifeCyclePhase",
            "ExpectedServiceLife", "TotalPrimaryEnergyConsumptionPerUnit", "WaterConsumptionPerUnit",
            "HazardousWastePerUnit", "NonHazardousWastePerUnit", "ClimateChangePerUnit",
            "AtmosphericAcidificationPerUnit", "RenewableEnergyConsumptionPerUnit",
            "NonRenewableEnergyConsumptionPerUnit", "ResourceDepletionPerUnit", "InertWastePerUnit",
            "RadioactiveWastePerUnit", "StratosphericOzoneLayerDestructionPerUnit",
            "PhotochemicalOzoneFormationPerUnit", "EutrophicationPerUnit"
        ],
        "Pset_EnvironmentalImpactValues": [
            "TotalPrimaryEnergyConsumption", "WaterConsumption", "HazardousWaste",
            "NonHazardousWaste", "ClimateChange", "AtmosphericAcidification",
            "RenewableEnergyConsumption", "NonRenewableEnergyConsumption", "ResourceDepletion",
            "InertWaste", "RadioactiveWaste", "StratosphericOzoneLayerDestruction",
            "PhotochemicalOzoneFormation", "Eutrophication", "LeadInTime", "Duration", "LeadOutTime"
        ],
        "Pset_InstallationOccurrence": [
            "InstallationDate", "AcceptanceDate", "PutIntoOperationDate"
        ],
        "Pset_MaintenanceStrategy": [
            "AssetCriticality", "AssetFrailty", "AssetPriority", "MonitoringType", "AccidentResponse"
        ],
        "Pset_MaintenanceTriggerCondition": [
            "ConditionTargetPerformance", "ConditionMaintenanceLevel", "ConditionReplacementLevel",
            "ConditionDisposalLevel"
        ],
        "Pset_MaintenanceTriggerDuration": [
            "DurationTargetPerformance", "DurationMaintenanceLevel", "DurationReplacementLevel",
            "DurationDisposalLevel"
        ],
        "Pset_MaintenanceTriggerPerformance": [
            "TargetPerformance", "PerformanceMaintenanceLevel", "ReplacementLevel", "DisposalLevel"
        ],
        "Pset_ManufacturerOccurrence": [
            "AcquisitionDate", "BarCode", "SerialNumber", "BatchReference", "AssemblyPlace", "ManufacturingDate"
        ],
        "Pset_ManufacturerTypeInformation": [
            "GlobalTradeItemNumber", "ArticleNumber", "ModelReference", "ModelLabel", "Manufacturer",
            "ProductionYear", "AssemblyPlace", "OperationalDocument", "SafetyDocument", "PerformanceCertificate"
        ],
        "Pset_PrecastConcreteElementFabrication": [
            "TypeDesignation", "ProductionLotId", "SerialNumber", "PieceMark",
            "AsBuiltLocationNumber", "ActualProductionDate", "ActualErectionDate"
        ],
        "Pset_PrecastConcreteElementGeneral": [
            "TypeDesignation", "CornerChamfer", "ManufacturingToleranceClass", "FormStrippingStrength",
            "LiftingStrength", "ReleaseStrength", "MinimumAllowableSupportLength", "InitialTension",
            "TendonRelaxation", "TransportationStrength", "SupportDuringTransportDescription",
            "SupportDuringTransportDocReference", "HollowCorePlugging", "CamberAtMidspan",
            "BatterAtStart", "BatterAtEnd", "Twisting", "Shortening", "PieceMark", "DesignLocationNumber"
        ],
        "Pset_RepairOccurrence": [
            "RepairContent", "RepairDate", "MeanTimeToRepair"
        ],
        "Pset_Risk": [
            "RiskName", "RiskType", "NatureOfRisk", "RiskAssessmentMethodology",
            "UnmitigatedRiskLikelihood", "UnmitigatedRiskConsequence", "UnmitigatedRiskSignificance",
            "MitigationPlanned", "MitigatedRiskLikelihood", "MitigatedRiskConsequence",
            "MitigatedRiskSignificance", "MitigationProposed", "AssociatedProduct",
            "AssociatedActivity", "AssociatedLocation"
        ],
        "Pset_RoofCommon": [
            "Reference", "Status", "AcousticRating", "IsExternal",
            "ThermalTransmittance", "FireRating", "LoadBearing"
        ],
        "Pset_ServiceLife": [
            "ServiceLifeDuration", "MeanTimeBetweenFailure"
        ],
        "Pset_Tolerance": [
            "ToleranceDescription", "ToleranceBasis", "OverallTolerance", "HorizontalTolerance",
            "OrthogonalTolerance", "VerticalTolerance", "PlanarFlatness", "HorizontalFlatness",
            "ElevationalFlatness", "SideFlatness", "OverallOrthogonality", "HorizontalOrthogonality",
            "OrthogonalOrthogonality", "VerticalOrthogonality", "OverallStraightness",
            "HorizontalStraightness", "OrthogonalStraightness", "VerticalStraightness"
        ],
        "Pset_Uncertainty": [
            "UncertaintyBasis", "UncertaintyDescription", "HorizontalUncertainty",
            "LinearUncertainty", "OrthogonalUncertainty", "VerticalUncertainty"
        ],
        "Pset_Warranty": [
            "WarrantyIdentifier", "WarrantyStartDate", "IsExtendedWarranty",
            "WarrantyPeriod", "WarrantyContent", "PointOfContact", "Exclusions"
        ],
        "Qto_BodyGeometryValidation": [
            "GrossSurfaceArea", "NetSurfaceArea", "GrossVolume", "NetVolume",
            "SurfaceGenusBeforeFeatures", "SurfaceGenusAfterFeatures"
        ],
        "Qto_RoofBaseQuantities": [
            "GrossArea", "NetArea", "ProjectedArea"
        ]
    },


    "IfcCovering": {
        "Pset_Condition": [
            "AssessmentDate", "AssessmentCondition", "AssessmentDescription",
            "AssessmentType", "AssessmentMethod", "LastAssessmentReport",
            "NextAssessmentDate", "AssessmentFrequency"
        ],
        "Pset_ConstructionAdministration": [
            "ProcurementMethod", "SpecificationSectionNumber", "SubmittalIdentifer"
        ],
        "Pset_ConstructionOccurence": [
            "InstallationDate", "ModelNumber", "TagNumber", "AssetIdentifier"
        ],
        "Pset_CoveringCommon": [
            "Reference", "Status", "AcousticRating", "FlammabilityRating", "FragilityRating",
            "Combustible", "SurfaceSpreadOfFlame", "Finish", "IsExternal", "ThermalTransmittance",
            "FireRating"
        ],
        "Pset_CoveringFlooring": [
            "HasNonSkidSurface", "HasAntiStaticSurface"
        ],
        "Pset_CoveringTypeMembrane": [
            "NominalInstallationDepth", "NominalTransverseInclination"
        ],
        "Pset_ElementKinematics": [
            "CyclicPath", "CyclicRange", "LinearPath", "LinearRange",
            "MaximumAngularVelocity", "MaximumConstantSpeed", "MinimumTime"
        ],
        "Pset_EnvironmentalCondition": [
            "ReferenceAirRelativeHumidity", "ReferenceEnvironmentTemperature",
            "MaximumAtmosphericPressure", "StorageTemperatureRange", "MaximumWindSpeed",
            "OperationalTemperatureRange", "MaximumRainIntensity", "SaltMistLevel",
            "SeismicResistance", "SmokeLevel", "MaximumSolarRadiation"
        ],
        "Pset_EnvironmentalImpactIndicators": [
            "Reference", "FunctionalUnitReference", "IndicatorsUnit", "LifeCyclePhase",
            "ExpectedServiceLife", "TotalPrimaryEnergyConsumptionPerUnit", "WaterConsumptionPerUnit",
            "HazardousWastePerUnit", "NonHazardousWastePerUnit", "ClimateChangePerUnit",
            "AtmosphericAcidificationPerUnit", "RenewableEnergyConsumptionPerUnit",
            "NonRenewableEnergyConsumptionPerUnit", "ResourceDepletionPerUnit", "InertWastePerUnit",
            "RadioactiveWastePerUnit", "StratosphericOzoneLayerDestructionPerUnit",
            "PhotochemicalOzoneFormationPerUnit", "EutrophicationPerUnit"
        ],
        "Pset_EnvironmentalImpactValues": [
            "TotalPrimaryEnergyConsumption", "WaterConsumption", "HazardousWaste",
            "NonHazardousWaste", "ClimateChange", "AtmosphericAcidification",
            "RenewableEnergyConsumption", "NonRenewableEnergyConsumption", "ResourceDepletion",
            "InertWaste", "RadioactiveWaste", "StratosphericOzoneLayerDestruction",
            "PhotochemicalOzoneFormation", "Eutrophication", "LeadInTime", "Duration", "LeadOutTime"
        ],
        "Pset_InstallationOccurrence": [
            "InstallationDate", "AcceptanceDate", "PutIntoOperationDate"
        ],
        "Pset_MaintenanceStrategy": [
            "AssetCriticality", "AssetFrailty", "AssetPriority", "MonitoringType", "AccidentResponse"
        ],
        "Pset_MaintenanceTriggerCondition": [
            "ConditionTargetPerformance", "ConditionMaintenanceLevel", "ConditionReplacementLevel",
            "ConditionDisposalLevel"
        ],
        "Pset_MaintenanceTriggerDuration": [
            "DurationTargetPerformance", "DurationMaintenanceLevel", "DurationReplacementLevel",
            "DurationDisposalLevel"
        ],
        "Pset_MaintenanceTriggerPerformance": [
            "TargetPerformance", "PerformanceMaintenanceLevel", "ReplacementLevel", "DisposalLevel"
        ],
        "Pset_ManufacturerOccurrence": [
            "AcquisitionDate", "BarCode", "SerialNumber", "BatchReference", "AssemblyPlace", "ManufacturingDate"
        ],
        "Pset_ManufacturerTypeInformation": [
            "GlobalTradeItemNumber", "ArticleNumber", "ModelReference", "ModelLabel", "Manufacturer",
            "ProductionYear", "AssemblyPlace", "OperationalDocument", "SafetyDocument", "PerformanceCertificate"
        ],
        "Pset_RepairOccurrence": [
            "RepairContent", "RepairDate", "MeanTimeToRepair"
        ],
        "Pset_Risk": [
            "RiskName", "RiskType", "NatureOfRisk", "RiskAssessmentMethodology",
            "UnmitigatedRiskLikelihood", "UnmitigatedRiskConsequence", "UnmitigatedRiskSignificance",
            "MitigationPlanned", "MitigatedRiskLikelihood", "MitigatedRiskConsequence",
            "MitigatedRiskSignificance", "MitigationProposed", "AssociatedProduct",
            "AssociatedActivity", "AssociatedLocation"
        ],
        "Pset_ServiceLife": [
            "ServiceLifeDuration", "MeanTimeBetweenFailure"
        ],
        "Pset_Tiling": [
            "Permeability", "TileLength", "TileWidth"
        ],
        "Pset_Tolerance": [
            "ToleranceDescription", "ToleranceBasis", "OverallTolerance", "HorizontalTolerance",
            "OrthogonalTolerance", "VerticalTolerance", "PlanarFlatness", "HorizontalFlatness",
            "ElevationalFlatness", "SideFlatness", "OverallOrthogonality", "HorizontalOrthogonality",
            "OrthogonalOrthogonality", "VerticalOrthogonality", "OverallStraightness",
            "HorizontalStraightness", "OrthogonalStraightness", "VerticalStraightness"
        ],
        "Pset_Uncertainty": [
            "UncertaintyBasis", "UncertaintyDescription", "HorizontalUncertainty",
            "LinearUncertainty", "OrthogonalUncertainty", "VerticalUncertainty"
        ],
        "Pset_Warranty": [
            "WarrantyIdentifier", "WarrantyStartDate", "IsExtendedWarranty",
            "WarrantyPeriod", "WarrantyContent", "PointOfContact", "Exclusions"
        ],
        "Qto_BodyGeometryValidation": [
            "GrossSurfaceArea", "NetSurfaceArea", "GrossVolume", "NetVolume",
            "SurfaceGenusBeforeFeatures", "SurfaceGenusAfterFeatures"
        ],
        "Qto_CoveringBaseQuantities": [
            "Width", "GrossArea", "NetArea"
        ]
    } ,    


    "IfcOpeningElement": {
        "Pset_Condition": [
            "AssessmentDate", "AssessmentCondition", "AssessmentDescription",
            "AssessmentType", "AssessmentMethod", "LastAssessmentReport",
            "NextAssessmentDate", "AssessmentFrequency"
        ],
        "Pset_ConstructionAdministration": [
            "ProcurementMethod", "SpecificationSectionNumber", "SubmittalIdentifer"
        ],
        "Pset_ConstructionOccurence": [
            "InstallationDate", "ModelNumber", "TagNumber", "AssetIdentifier"
        ],
        "Pset_ElementKinematics": [
            "CyclicPath", "CyclicRange", "LinearPath", "LinearRange",
            "MaximumAngularVelocity", "MaximumConstantSpeed", "MinimumTime"
        ],
        "Pset_EnvironmentalCondition": [
            "ReferenceAirRelativeHumidity", "ReferenceEnvironmentTemperature",
            "MaximumAtmosphericPressure", "StorageTemperatureRange", "MaximumWindSpeed",
            "OperationalTemperatureRange", "MaximumRainIntensity", "SaltMistLevel",
            "SeismicResistance", "SmokeLevel", "MaximumSolarRadiation"
        ],
        "Pset_EnvironmentalImpactIndicators": [
            "Reference", "FunctionalUnitReference", "IndicatorsUnit", "LifeCyclePhase",
            "ExpectedServiceLife", "TotalPrimaryEnergyConsumptionPerUnit", "WaterConsumptionPerUnit",
            "HazardousWastePerUnit", "NonHazardousWastePerUnit", "ClimateChangePerUnit",
            "AtmosphericAcidificationPerUnit", "RenewableEnergyConsumptionPerUnit",
            "NonRenewableEnergyConsumptionPerUnit", "ResourceDepletionPerUnit", "InertWastePerUnit",
            "RadioactiveWastePerUnit", "StratosphericOzoneLayerDestructionPerUnit",
            "PhotochemicalOzoneFormationPerUnit", "EutrophicationPerUnit"
        ],
        "Pset_EnvironmentalImpactValues": [
            "TotalPrimaryEnergyConsumption", "WaterConsumption", "HazardousWaste",
            "NonHazardousWaste", "ClimateChange", "AtmosphericAcidification",
            "RenewableEnergyConsumption", "NonRenewableEnergyConsumption", "ResourceDepletion",
            "InertWaste", "RadioactiveWaste", "StratosphericOzoneLayerDestruction",
            "PhotochemicalOzoneFormation", "Eutrophication", "LeadInTime", "Duration", "LeadOutTime"
        ],
        "Pset_InstallationOccurrence": [
            "InstallationDate", "AcceptanceDate", "PutIntoOperationDate"
        ],
        "Pset_MaintenanceStrategy": [
            "AssetCriticality", "AssetFrailty", "AssetPriority", "MonitoringType", "AccidentResponse"
        ],
        "Pset_MaintenanceTriggerCondition": [
            "ConditionTargetPerformance", "ConditionMaintenanceLevel", "ConditionReplacementLevel",
            "ConditionDisposalLevel"
        ],
        "Pset_MaintenanceTriggerDuration": [
            "DurationTargetPerformance", "DurationMaintenanceLevel", "DurationReplacementLevel",
            "DurationDisposalLevel"
        ],
        "Pset_MaintenanceTriggerPerformance": [
            "TargetPerformance", "PerformanceMaintenanceLevel", "ReplacementLevel", "DisposalLevel"
        ],
        "Pset_ManufacturerOccurrence": [
            "AcquisitionDate", "BarCode", "SerialNumber", "BatchReference", "AssemblyPlace", "ManufacturingDate"
        ],
        "Pset_ManufacturerTypeInformation": [
            "GlobalTradeItemNumber", "ArticleNumber", "ModelReference", "ModelLabel", "Manufacturer",
            "ProductionYear", "AssemblyPlace", "OperationalDocument", "SafetyDocument", "PerformanceCertificate"
        ],
        "Pset_OpeningElementCommon": [
            "Reference", "Status", "Purpose", "FireExit", "FireRating", "AcousticRating"
        ],
        "Pset_RepairOccurrence": [
            "RepairContent", "RepairDate", "MeanTimeToRepair"
        ],
        "Pset_Risk": [
            "RiskName", "RiskType", "NatureOfRisk", "RiskAssessmentMethodology",
            "UnmitigatedRiskLikelihood", "UnmitigatedRiskConsequence", "UnmitigatedRiskSignificance",
            "MitigationPlanned", "MitigatedRiskLikelihood", "MitigatedRiskConsequence",
            "MitigatedRiskSignificance", "MitigationProposed", "AssociatedProduct",
            "AssociatedActivity", "AssociatedLocation"
        ],
        "Pset_ServiceLife": [
            "ServiceLifeDuration", "MeanTimeBetweenFailure"
        ],
        "Pset_Tolerance": [
            "ToleranceDescription", "ToleranceBasis", "OverallTolerance", "HorizontalTolerance",
            "OrthogonalTolerance", "VerticalTolerance", "PlanarFlatness", "HorizontalFlatness",
            "ElevationalFlatness", "SideFlatness", "OverallOrthogonality", "HorizontalOrthogonality",
            "OrthogonalOrthogonality", "VerticalOrthogonality", "OverallStraightness",
            "HorizontalStraightness", "OrthogonalStraightness", "VerticalStraightness"
        ],
        "Pset_Uncertainty": [
            "UncertaintyBasis", "UncertaintyDescription", "HorizontalUncertainty",
            "LinearUncertainty", "OrthogonalUncertainty", "VerticalUncertainty"
        ],
        "Pset_Warranty": [
            "WarrantyIdentifier", "WarrantyStartDate", "IsExtendedWarranty",
            "WarrantyPeriod", "WarrantyContent", "PointOfContact", "Exclusions"
        ],
        "Qto_BodyGeometryValidation": [
            "GrossSurfaceArea", "NetSurfaceArea", "GrossVolume", "NetVolume",
            "SurfaceGenusBeforeFeatures", "SurfaceGenusAfterFeatures"
        ],
        "Qto_OpeningElementBaseQuantities": [
            "Width", "Height", "Depth", "Area"
        ]
    },


    "IfcDoor": {
        "Pset_Condition": [
            "AssessmentDate", "AssessmentCondition", "AssessmentDescription",
            "AssessmentType", "AssessmentMethod", "LastAssessmentReport",
            "NextAssessmentDate", "AssessmentFrequency"
        ],
        "Pset_ConstructionAdministration": [
            "ProcurementMethod", "SpecificationSectionNumber", "SubmittalIdentifer"
        ],
        "Pset_ConstructionOccurence": [
            "InstallationDate", "ModelNumber", "TagNumber", "AssetIdentifier"
        ],
        "Pset_DoorCommon": [
            "Reference", "Status", "FireRating", "AcousticRating", "SecurityRating",
            "DurabilityRating", "HygrothermalRating", "WaterTightnessRating", "MechanicalLoadRating",
            "WindLoadRating", "Infiltration", "IsExternal", "ThermalTransmittance",
            "GlazingAreaFraction", "HandicapAccessible", "FireExit", "HasDrive",
            "SelfClosing", "SmokeStop"
        ],
        "Pset_DoorLiningProperties": [
            "LiningDepth", "LiningThickness", "ThresholdDepth", "ThresholdThickness",
            "TransomThickness", "TransomOffset", "LiningOffset", "ThresholdOffset",
            "CasingThickness", "CasingDepth", "LiningToPanelOffsetX", "LiningToPanelOffsetY"
        ],
        "Pset_DoorPanelProperties": [
            "PanelDepth", "PanelOperation", "PanelWidth", "PanelPosition"
        ],
        "Pset_DoorTypeTurnstile": [
            "IsBidirectional", "TurnstileType", "NarrowChannelWidth", "WideChannelWidth"
        ],
        "Pset_DoorWindowGlazingType": [
            "GlassLayers", "GlassThickness1", "GlassThickness2", "GlassThickness3",
            "FillGas", "GlassColour", "IsTempered", "IsLaminated", "IsCoated",
            "IsWired", "VisibleLightReflectance", "VisibleLightTransmittance",
            "SolarAbsorption", "SolarReflectance", "SolarTransmittance", "SolarHeatGainTransmittance",
            "ShadingCoefficient", "ThermalTransmittanceSummer", "ThermalTransmittanceWinter"
        ],
        "Pset_ElementKinematics": [
            "CyclicPath", "CyclicRange", "LinearPath", "LinearRange",
            "MaximumAngularVelocity", "MaximumConstantSpeed", "MinimumTime"
        ],
        "Pset_EnvironmentalCondition": [
            "ReferenceAirRelativeHumidity", "ReferenceEnvironmentTemperature",
            "MaximumAtmosphericPressure", "StorageTemperatureRange", "MaximumWindSpeed",
            "OperationalTemperatureRange", "MaximumRainIntensity", "SaltMistLevel",
            "SeismicResistance", "SmokeLevel", "MaximumSolarRadiation"
        ],
        "Pset_EnvironmentalImpactIndicators": [
            "Reference", "FunctionalUnitReference", "IndicatorsUnit", "LifeCyclePhase",
            "ExpectedServiceLife", "TotalPrimaryEnergyConsumptionPerUnit", "WaterConsumptionPerUnit",
            "HazardousWastePerUnit", "NonHazardousWastePerUnit", "ClimateChangePerUnit",
            "AtmosphericAcidificationPerUnit", "RenewableEnergyConsumptionPerUnit",
            "NonRenewableEnergyConsumptionPerUnit", "ResourceDepletionPerUnit", "InertWastePerUnit",
            "RadioactiveWastePerUnit", "StratosphericOzoneLayerDestructionPerUnit",
            "PhotochemicalOzoneFormationPerUnit", "EutrophicationPerUnit"
        ],
        "Pset_EnvironmentalImpactValues": [
            "TotalPrimaryEnergyConsumption", "WaterConsumption", "HazardousWaste",
            "NonHazardousWaste", "ClimateChange", "AtmosphericAcidification",
            "RenewableEnergyConsumption", "NonRenewableEnergyConsumption", "ResourceDepletion",
            "InertWaste", "RadioactiveWaste", "StratosphericOzoneLayerDestruction",
            "PhotochemicalOzoneFormation", "Eutrophication", "LeadInTime", "Duration", "LeadOutTime"
        ],
        "Pset_InstallationOccurrence": [
            "InstallationDate", "AcceptanceDate", "PutIntoOperationDate"
        ],
        "Pset_MaintenanceStrategy": [
            "AssetCriticality", "AssetFrailty", "AssetPriority", "MonitoringType", "AccidentResponse"
        ],
        "Pset_MaintenanceTriggerCondition": [
            "ConditionTargetPerformance", "ConditionMaintenanceLevel", "ConditionReplacementLevel",
            "ConditionDisposalLevel"
        ],
        "Pset_MaintenanceTriggerDuration": [
            "DurationTargetPerformance", "DurationMaintenanceLevel", "DurationReplacementLevel",
            "DurationDisposalLevel"
        ],
        "Pset_MaintenanceTriggerPerformance": [
            "TargetPerformance", "PerformanceMaintenanceLevel", "ReplacementLevel", "DisposalLevel"
        ],
        "Pset_ManufacturerOccurrence": [
            "AcquisitionDate", "BarCode", "SerialNumber", "BatchReference", "AssemblyPlace", "ManufacturingDate"
        ],
        "Pset_ManufacturerTypeInformation": [
            "GlobalTradeItemNumber", "ArticleNumber", "ModelReference", "ModelLabel", "Manufacturer",
            "ProductionYear", "AssemblyPlace", "OperationalDocument", "SafetyDocument", "PerformanceCertificate"
        ],
        "Pset_PermeableCoveringProperties": [
            "OperationType", "PanelPosition", "FrameDepth", "FrameThickness"
        ],
        "Pset_ProcessCapacity": [
            "ProcessItem", "ProcessCapacity", "ProcessPerformance", "DownstreamConnections", "UpstreamConnections"
        ],
        "Pset_RepairOccurrence": [
            "RepairContent", "RepairDate", "MeanTimeToRepair"
        ],
        "Pset_Risk": [
            "RiskName", "RiskType", "NatureOfRisk", "RiskAssessmentMethodology",
            "UnmitigatedRiskLikelihood", "UnmitigatedRiskConsequence", "UnmitigatedRiskSignificance",
            "MitigationPlanned", "MitigatedRiskLikelihood", "MitigatedRiskConsequence",
            "MitigatedRiskSignificance", "MitigationProposed", "AssociatedProduct",
            "AssociatedActivity", "AssociatedLocation"
        ],
        "Pset_ServiceLife": [
            "ServiceLifeDuration", "MeanTimeBetweenFailure"
        ],
        "Pset_TicketProcessing_BOOM_BARRIER": [
            "TicketProcessingTime", "TicketStuckRatio"
        ],
        "Pset_TicketProcessing_TURNSTILE": [
            "TicketProcessingTime", "TicketStuckRatio"
        ],
        "Pset_Tolerance": [
            "ToleranceDescription", "ToleranceBasis", "OverallTolerance", "HorizontalTolerance",
            "OrthogonalTolerance", "VerticalTolerance", "PlanarFlatness", "HorizontalFlatness",
            "ElevationalFlatness", "SideFlatness", "OverallOrthogonality", "HorizontalOrthogonality",
            "OrthogonalOrthogonality", "VerticalOrthogonality", "OverallStraightness",
            "HorizontalStraightness", "OrthogonalStraightness", "VerticalStraightness"
        ],
        "Pset_Uncertainty": [
            "UncertaintyBasis", "UncertaintyDescription", "HorizontalUncertainty",
            "LinearUncertainty", "OrthogonalUncertainty", "VerticalUncertainty"
        ],
        "Pset_Warranty": [
            "WarrantyIdentifier", "WarrantyStartDate", "IsExtendedWarranty",
            "WarrantyPeriod", "WarrantyContent", "PointOfContact", "Exclusions"
        ],
        "Qto_BodyGeometryValidation": [
            "GrossSurfaceArea", "NetSurfaceArea", "GrossVolume", "NetVolume",
            "SurfaceGenusBeforeFeatures", "SurfaceGenusAfterFeatures"
        ],
        "Qto_DoorBaseQuantities": [
            "Width", "Height", "Perimeter", "Area"
        ]
    },    


    "IfcWindow": {
        "Pset_Condition": [
            "AssessmentDate", "AssessmentCondition", "AssessmentDescription",
            "AssessmentType", "AssessmentMethod", "LastAssessmentReport",
            "NextAssessmentDate", "AssessmentFrequency"
        ],
        "Pset_ConstructionAdministration": [
            "ProcurementMethod", "SpecificationSectionNumber", "SubmittalIdentifer"
        ],
        "Pset_ConstructionOccurence": [
            "InstallationDate", "ModelNumber", "TagNumber", "AssetIdentifier"
        ],
        "Pset_DoorWindowGlazingType": [
            "GlassLayers", "GlassThickness1", "GlassThickness2", "GlassThickness3",
            "FillGas", "GlassColour", "IsTempered", "IsLaminated", "IsCoated",
            "IsWired", "VisibleLightReflectance", "VisibleLightTransmittance",
            "SolarAbsorption", "SolarReflectance", "SolarTransmittance", 
            "SolarHeatGainTransmittance", "ShadingCoefficient",
            "ThermalTransmittanceSummer", "ThermalTransmittanceWinter"
        ],
        "Pset_ElementKinematics": [
            "CyclicPath", "CyclicRange", "LinearPath", "LinearRange",
            "MaximumAngularVelocity", "MaximumConstantSpeed", "MinimumTime"
        ],
        "Pset_EnvironmentalCondition": [
            "ReferenceAirRelativeHumidity", "ReferenceEnvironmentTemperature",
            "MaximumAtmosphericPressure", "StorageTemperatureRange", "MaximumWindSpeed",
            "OperationalTemperatureRange", "MaximumRainIntensity", "SaltMistLevel",
            "SeismicResistance", "SmokeLevel", "MaximumSolarRadiation"
        ],
        "Pset_EnvironmentalImpactIndicators": [
            "Reference", "FunctionalUnitReference", "IndicatorsUnit", "LifeCyclePhase",
            "ExpectedServiceLife", "TotalPrimaryEnergyConsumptionPerUnit",
            "WaterConsumptionPerUnit", "HazardousWastePerUnit", "NonHazardousWastePerUnit",
            "ClimateChangePerUnit", "AtmosphericAcidificationPerUnit",
            "RenewableEnergyConsumptionPerUnit", "NonRenewableEnergyConsumptionPerUnit",
            "ResourceDepletionPerUnit", "InertWastePerUnit", "RadioactiveWastePerUnit",
            "StratosphericOzoneLayerDestructionPerUnit", "PhotochemicalOzoneFormationPerUnit",
            "EutrophicationPerUnit"
        ],
        "Pset_EnvironmentalImpactValues": [
            "TotalPrimaryEnergyConsumption", "WaterConsumption", "HazardousWaste",
            "NonHazardousWaste", "ClimateChange", "AtmosphericAcidification",
            "RenewableEnergyConsumption", "NonRenewableEnergyConsumption", "ResourceDepletion",
            "InertWaste", "RadioactiveWaste", "StratosphericOzoneLayerDestruction",
            "PhotochemicalOzoneFormation", "Eutrophication", "LeadInTime", "Duration", "LeadOutTime"
        ],
        "Pset_InstallationOccurrence": [
            "InstallationDate", "AcceptanceDate", "PutIntoOperationDate"
        ],
        "Pset_MaintenanceStrategy": [
            "AssetCriticality", "AssetFrailty", "AssetPriority", "MonitoringType", "AccidentResponse"
        ],
        "Pset_MaintenanceTriggerCondition": [
            "ConditionTargetPerformance", "ConditionMaintenanceLevel", "ConditionReplacementLevel",
            "ConditionDisposalLevel"
        ],
        "Pset_MaintenanceTriggerDuration": [
            "DurationTargetPerformance", "DurationMaintenanceLevel", "DurationReplacementLevel",
            "DurationDisposalLevel"
        ],
        "Pset_MaintenanceTriggerPerformance": [
            "TargetPerformance", "PerformanceMaintenanceLevel", "ReplacementLevel", "DisposalLevel"
        ],
        "Pset_ManufacturerOccurrence": [
            "AcquisitionDate", "BarCode", "SerialNumber", "BatchReference", "AssemblyPlace", "ManufacturingDate"
        ],
        "Pset_ManufacturerTypeInformation": [
            "GlobalTradeItemNumber", "ArticleNumber", "ModelReference", "ModelLabel", "Manufacturer",
            "ProductionYear", "AssemblyPlace", "OperationalDocument", "SafetyDocument", "PerformanceCertificate"
        ],
        "Pset_PermeableCoveringProperties": [
            "OperationType", "PanelPosition", "FrameDepth", "FrameThickness"
        ],
        "Pset_RepairOccurrence": [
            "RepairContent", "RepairDate", "MeanTimeToRepair"
        ],
        "Pset_Risk": [
            "RiskName", "RiskType", "NatureOfRisk", "RiskAssessmentMethodology",
            "UnmitigatedRiskLikelihood", "UnmitigatedRiskConsequence", "UnmitigatedRiskSignificance",
            "MitigationPlanned", "MitigatedRiskLikelihood", "MitigatedRiskConsequence",
            "MitigatedRiskSignificance", "MitigationProposed", "AssociatedProduct",
            "AssociatedActivity", "AssociatedLocation"
        ],
        "Pset_ServiceLife": [
            "ServiceLifeDuration", "MeanTimeBetweenFailure"
        ],
        "Pset_Tolerance": [
            "ToleranceDescription", "ToleranceBasis", "OverallTolerance", "HorizontalTolerance",
            "OrthogonalTolerance", "VerticalTolerance", "PlanarFlatness", "HorizontalFlatness",
            "ElevationalFlatness", "SideFlatness", "OverallOrthogonality", "HorizontalOrthogonality",
            "OrthogonalOrthogonality", "VerticalOrthogonality", "OverallStraightness",
            "HorizontalStraightness", "OrthogonalStraightness", "VerticalStraightness"
        ],
        "Pset_Uncertainty": [
            "UncertaintyBasis", "UncertaintyDescription", "HorizontalUncertainty",
            "LinearUncertainty", "OrthogonalUncertainty", "VerticalUncertainty"
        ],
        "Pset_Warranty": [
            "WarrantyIdentifier", "WarrantyStartDate", "IsExtendedWarranty",
            "WarrantyPeriod", "WarrantyContent", "PointOfContact", "Exclusions"
        ],
        "Pset_WindowCommon": [
            "Reference", "Status", "AcousticRating", "FireRating", "SecurityRating", "IsExternal",
            "Infiltration", "ThermalTransmittance", "GlazingAreaFraction", "HasSillExternal",
            "HasSillInternal", "HasDrive", "SmokeStop", "FireExit", "WaterTightnessRating",
            "MechanicalLoadRating", "WindLoadRating"
        ],
        "Pset_WindowLiningProperties": [
            "LiningDepth", "LiningThickness", "TransomThickness", "MullionThickness",
            "FirstTransomOffset", "SecondTransomOffset", "FirstMullionOffset", "SecondMullionOffset",
            "LiningOffset", "LiningToPanelOffsetX", "LiningToPanelOffsetY"
        ],
        "Pset_WindowPanelProperties": [
            "OperationType", "PanelPosition", "FrameDepth", "FrameThickness"
        ],
        "Qto_BodyGeometryValidation": [
            "GrossSurfaceArea", "NetSurfaceArea", "GrossVolume", "NetVolume",
            "SurfaceGenusBeforeFeatures", "SurfaceGenusAfterFeatures"
        ],
        "Qto_WindowBaseQuantities": [
            "Width", "Height", "Perimeter"
        ]
    },    


    # Collegamenti e rinforzi
    "IfcReinforcingBar": {
        "Pset_Condition": [
            "AssessmentDate", "AssessmentCondition", "AssessmentDescription",
            "AssessmentType", "AssessmentMethod", "LastAssessmentReport",
            "NextAssessmentDate", "AssessmentFrequency"
        ],
        "Pset_ConstructionAdministration": [
            "ProcurementMethod", "SpecificationSectionNumber", "SubmittalIdentifer"
        ],
        "Pset_ConstructionOccurence": [
            "InstallationDate", "ModelNumber", "TagNumber", "AssetIdentifier"
        ],
        "Pset_ElementComponentCommon": [
            "Reference", "Status", "DeliveryType", "CorrosionTreatment"
        ],
        "Pset_ElementKinematics": [
            "CyclicPath", "CyclicRange", "LinearPath", "LinearRange",
            "MaximumAngularVelocity", "MaximumConstantSpeed", "MinimumTime"
        ],
        "Pset_EnvironmentalCondition": [
            "ReferenceAirRelativeHumidity", "ReferenceEnvironmentTemperature",
            "MaximumAtmosphericPressure", "StorageTemperatureRange", "MaximumWindSpeed",
            "OperationalTemperatureRange", "MaximumRainIntensity", "SaltMistLevel",
            "SeismicResistance", "SmokeLevel", "MaximumSolarRadiation"
        ],
        "Pset_EnvironmentalImpactIndicators": [
            "Reference", "FunctionalUnitReference", "IndicatorsUnit", "LifeCyclePhase",
            "ExpectedServiceLife", "TotalPrimaryEnergyConsumptionPerUnit",
            "WaterConsumptionPerUnit", "HazardousWastePerUnit", "NonHazardousWastePerUnit",
            "ClimateChangePerUnit", "AtmosphericAcidificationPerUnit",
            "RenewableEnergyConsumptionPerUnit", "NonRenewableEnergyConsumptionPerUnit",
            "ResourceDepletionPerUnit", "InertWastePerUnit", "RadioactiveWastePerUnit",
            "StratosphericOzoneLayerDestructionPerUnit", "PhotochemicalOzoneFormationPerUnit",
            "EutrophicationPerUnit"
        ],
        "Pset_EnvironmentalImpactValues": [
            "TotalPrimaryEnergyConsumption", "WaterConsumption", "HazardousWaste",
            "NonHazardousWaste", "ClimateChange", "AtmosphericAcidification",
            "RenewableEnergyConsumption", "NonRenewableEnergyConsumption", "ResourceDepletion",
            "InertWaste", "RadioactiveWaste", "StratosphericOzoneLayerDestruction",
            "PhotochemicalOzoneFormation", "Eutrophication", "LeadInTime", "Duration", "LeadOutTime"
        ],
        "Pset_InstallationOccurrence": [
            "InstallationDate", "AcceptanceDate", "PutIntoOperationDate"
        ],
        "Pset_MaintenanceStrategy": [
            "AssetCriticality", "AssetFrailty", "AssetPriority", "MonitoringType", "AccidentResponse"
        ],
        "Pset_MaintenanceTriggerCondition": [
            "ConditionTargetPerformance", "ConditionMaintenanceLevel", "ConditionReplacementLevel",
            "ConditionDisposalLevel"
        ],
        "Pset_MaintenanceTriggerDuration": [
            "DurationTargetPerformance", "DurationMaintenanceLevel", "DurationReplacementLevel",
            "DurationDisposalLevel"
        ],
        "Pset_MaintenanceTriggerPerformance": [
            "TargetPerformance", "PerformanceMaintenanceLevel", "ReplacementLevel", "DisposalLevel"
        ],
        "Pset_ManufacturerOccurrence": [
            "AcquisitionDate", "BarCode", "SerialNumber", "BatchReference", "AssemblyPlace", "ManufacturingDate"
        ],
        "Pset_ManufacturerTypeInformation": [
            "GlobalTradeItemNumber", "ArticleNumber", "ModelReference", "ModelLabel", "Manufacturer",
            "ProductionYear", "AssemblyPlace", "OperationalDocument", "SafetyDocument", "PerformanceCertificate"
        ],
        "Pset_RepairOccurrence": [
            "RepairContent", "RepairDate", "MeanTimeToRepair"
        ],
        "Pset_Risk": [
            "RiskName", "RiskType", "NatureOfRisk", "RiskAssessmentMethodology",
            "UnmitigatedRiskLikelihood", "UnmitigatedRiskConsequence", "UnmitigatedRiskSignificance",
            "MitigationPlanned", "MitigatedRiskLikelihood", "MitigatedRiskConsequence",
            "MitigatedRiskSignificance", "MitigationProposed", "AssociatedProduct",
            "AssociatedActivity", "AssociatedLocation"
        ],
        "Pset_ServiceLife": [
            "ServiceLifeDuration", "MeanTimeBetweenFailure"
        ],
        "Pset_Tolerance": [
            "ToleranceDescription", "ToleranceBasis", "OverallTolerance", "HorizontalTolerance",
            "OrthogonalTolerance", "VerticalTolerance", "PlanarFlatness", "HorizontalFlatness",
            "ElevationalFlatness", "SideFlatness", "OverallOrthogonality", "HorizontalOrthogonality",
            "OrthogonalOrthogonality", "VerticalOrthogonality", "OverallStraightness",
            "HorizontalStraightness", "OrthogonalStraightness", "VerticalStraightness"
        ],
        "Pset_Uncertainty": [
            "UncertaintyBasis", "UncertaintyDescription", "HorizontalUncertainty",
            "LinearUncertainty", "OrthogonalUncertainty", "VerticalUncertainty"
        ],
        "Pset_Warranty": [
            "WarrantyIdentifier", "WarrantyStartDate", "IsExtendedWarranty",
            "WarrantyPeriod", "WarrantyContent", "PointOfContact", "Exclusions"
        ],
        "Qto_BodyGeometryValidation": [
            "GrossSurfaceArea", "NetSurfaceArea", "GrossVolume", "NetVolume",
            "SurfaceGenusBeforeFeatures", "SurfaceGenusAfterFeatures"
        ],
        "Qto_ReinforcingElementBaseQuantities": [
            "Count", "Length", "Weight"
        ]
    }, 


    "IfcReinforcingMesh": {
        "Pset_Condition": [
            "AssessmentDate", "AssessmentCondition", "AssessmentDescription",
            "AssessmentType", "AssessmentMethod", "LastAssessmentReport",
            "NextAssessmentDate", "AssessmentFrequency"
        ],
        "Pset_ConstructionAdministration": [
            "ProcurementMethod", "SpecificationSectionNumber", "SubmittalIdentifer"
        ],
        "Pset_ConstructionOccurence": [
            "InstallationDate", "ModelNumber", "TagNumber", "AssetIdentifier"
        ],
        "Pset_ElementComponentCommon": [
            "Reference", "Status", "DeliveryType", "CorrosionTreatment"
        ],
        "Pset_ElementKinematics": [
            "CyclicPath", "CyclicRange", "LinearPath", "LinearRange",
            "MaximumAngularVelocity", "MaximumConstantSpeed", "MinimumTime"
        ],
        "Pset_EnvironmentalCondition": [
            "ReferenceAirRelativeHumidity", "ReferenceEnvironmentTemperature",
            "MaximumAtmosphericPressure", "StorageTemperatureRange", "MaximumWindSpeed",
            "OperationalTemperatureRange", "MaximumRainIntensity", "SaltMistLevel",
            "SeismicResistance", "SmokeLevel", "MaximumSolarRadiation"
        ],
        "Pset_EnvironmentalImpactIndicators": [
            "Reference", "FunctionalUnitReference", "IndicatorsUnit", "LifeCyclePhase",
            "ExpectedServiceLife", "TotalPrimaryEnergyConsumptionPerUnit",
            "WaterConsumptionPerUnit", "HazardousWastePerUnit", "NonHazardousWastePerUnit",
            "ClimateChangePerUnit", "AtmosphericAcidificationPerUnit",
            "RenewableEnergyConsumptionPerUnit", "NonRenewableEnergyConsumptionPerUnit",
            "ResourceDepletionPerUnit", "InertWastePerUnit", "RadioactiveWastePerUnit",
            "StratosphericOzoneLayerDestructionPerUnit", "PhotochemicalOzoneFormationPerUnit",
            "EutrophicationPerUnit"
        ],
        "Pset_EnvironmentalImpactValues": [
            "TotalPrimaryEnergyConsumption", "WaterConsumption", "HazardousWaste",
            "NonHazardousWaste", "ClimateChange", "AtmosphericAcidification",
            "RenewableEnergyConsumption", "NonRenewableEnergyConsumption", "ResourceDepletion",
            "InertWaste", "RadioactiveWaste", "StratosphericOzoneLayerDestruction",
            "PhotochemicalOzoneFormation", "Eutrophication", "LeadInTime", "Duration", "LeadOutTime"
        ],
        "Pset_InstallationOccurrence": [
            "InstallationDate", "AcceptanceDate", "PutIntoOperationDate"
        ],
        "Pset_MaintenanceStrategy": [
            "AssetCriticality", "AssetFrailty", "AssetPriority", "MonitoringType", "AccidentResponse"
        ],
        "Pset_MaintenanceTriggerCondition": [
            "ConditionTargetPerformance", "ConditionMaintenanceLevel", "ConditionReplacementLevel",
            "ConditionDisposalLevel"
        ],
        "Pset_MaintenanceTriggerDuration": [
            "DurationTargetPerformance", "DurationMaintenanceLevel", "DurationReplacementLevel",
            "DurationDisposalLevel"
        ],
        "Pset_MaintenanceTriggerPerformance": [
            "TargetPerformance", "PerformanceMaintenanceLevel", "ReplacementLevel", "DisposalLevel"
        ],
        "Pset_ManufacturerOccurrence": [
            "AcquisitionDate", "BarCode", "SerialNumber", "BatchReference", "AssemblyPlace", "ManufacturingDate"
        ],
        "Pset_ManufacturerTypeInformation": [
            "GlobalTradeItemNumber", "ArticleNumber", "ModelReference", "ModelLabel", "Manufacturer",
            "ProductionYear", "AssemblyPlace", "OperationalDocument", "SafetyDocument", "PerformanceCertificate"
        ],
        "Pset_RepairOccurrence": [
            "RepairContent", "RepairDate", "MeanTimeToRepair"
        ],
        "Pset_Risk": [
            "RiskName", "RiskType", "NatureOfRisk", "RiskAssessmentMethodology",
            "UnmitigatedRiskLikelihood", "UnmitigatedRiskConsequence", "UnmitigatedRiskSignificance",
            "MitigationPlanned", "MitigatedRiskLikelihood", "MitigatedRiskConsequence",
            "MitigatedRiskSignificance", "MitigationProposed", "AssociatedProduct",
            "AssociatedActivity", "AssociatedLocation"
        ],
        "Pset_ServiceLife": [
            "ServiceLifeDuration", "MeanTimeBetweenFailure"
        ],
        "Pset_Tolerance": [
            "ToleranceDescription", "ToleranceBasis", "OverallTolerance", "HorizontalTolerance",
            "OrthogonalTolerance", "VerticalTolerance", "PlanarFlatness", "HorizontalFlatness",
            "ElevationalFlatness", "SideFlatness", "OverallOrthogonality", "HorizontalOrthogonality",
            "OrthogonalOrthogonality", "VerticalOrthogonality", "OverallStraightness",
            "HorizontalStraightness", "OrthogonalStraightness", "VerticalStraightness"
        ],
        "Pset_Uncertainty": [
            "UncertaintyBasis", "UncertaintyDescription", "HorizontalUncertainty",
            "LinearUncertainty", "OrthogonalUncertainty", "VerticalUncertainty"
        ],
        "Pset_Warranty": [
            "WarrantyIdentifier", "WarrantyStartDate", "IsExtendedWarranty",
            "WarrantyPeriod", "WarrantyContent", "PointOfContact", "Exclusions"
        ],
        "Qto_BodyGeometryValidation": [
            "GrossSurfaceArea", "NetSurfaceArea", "GrossVolume", "NetVolume",
            "SurfaceGenusBeforeFeatures", "SurfaceGenusAfterFeatures"
        ],
        "Qto_ReinforcingElementBaseQuantities": [
            "Count", "Length", "Weight"
        ]
    },


    "IfcCurtainWall": {
        "Pset_Condition": [
            "AssessmentDate", "AssessmentCondition", "AssessmentDescription",
            "AssessmentType", "AssessmentMethod", "LastAssessmentReport",
            "NextAssessmentDate", "AssessmentFrequency"
        ],
        "Pset_ConstructionAdministration": [
            "ProcurementMethod", "SpecificationSectionNumber", "SubmittalIdentifer"
        ],
        "Pset_ConstructionOccurence": [
            "InstallationDate", "ModelNumber", "TagNumber", "AssetIdentifier"
        ],
        "Pset_CurtainWallCommon": [
            "Reference", "Status", "AcousticRating", "FireRating", "Combustible",
            "SurfaceSpreadOfFlame", "ThermalTransmittance", "IsExternal"
        ],
        "Pset_ElementKinematics": [
            "CyclicPath", "CyclicRange", "LinearPath", "LinearRange",
            "MaximumAngularVelocity", "MaximumConstantSpeed", "MinimumTime"
        ],
        "Pset_EnvironmentalCondition": [
            "ReferenceAirRelativeHumidity", "ReferenceEnvironmentTemperature",
            "MaximumAtmosphericPressure", "StorageTemperatureRange", "MaximumWindSpeed",
            "OperationalTemperatureRange", "MaximumRainIntensity", "SaltMistLevel",
            "SeismicResistance", "SmokeLevel", "MaximumSolarRadiation"
        ],
        "Pset_EnvironmentalImpactIndicators": [
            "Reference", "FunctionalUnitReference", "IndicatorsUnit", "LifeCyclePhase",
            "ExpectedServiceLife", "TotalPrimaryEnergyConsumptionPerUnit",
            "WaterConsumptionPerUnit", "HazardousWastePerUnit", "NonHazardousWastePerUnit",
            "ClimateChangePerUnit", "AtmosphericAcidificationPerUnit",
            "RenewableEnergyConsumptionPerUnit", "NonRenewableEnergyConsumptionPerUnit",
            "ResourceDepletionPerUnit", "InertWastePerUnit", "RadioactiveWastePerUnit",
            "StratosphericOzoneLayerDestructionPerUnit", "PhotochemicalOzoneFormationPerUnit",
            "EutrophicationPerUnit"
        ],
        "Pset_EnvironmentalImpactValues": [
            "TotalPrimaryEnergyConsumption", "WaterConsumption", "HazardousWaste",
            "NonHazardousWaste", "ClimateChange", "AtmosphericAcidification",
            "RenewableEnergyConsumption", "NonRenewableEnergyConsumption", "ResourceDepletion",
            "InertWaste", "RadioactiveWaste", "StratosphericOzoneLayerDestruction",
            "PhotochemicalOzoneFormation", "Eutrophication", "LeadInTime", "Duration", "LeadOutTime"
        ],
        "Pset_InstallationOccurrence": [
            "InstallationDate", "AcceptanceDate", "PutIntoOperationDate"
        ],
        "Pset_MaintenanceStrategy": [
            "AssetCriticality", "AssetFrailty", "AssetPriority", "MonitoringType", "AccidentResponse"
        ],
        "Pset_MaintenanceTriggerCondition": [
            "ConditionTargetPerformance", "ConditionMaintenanceLevel", "ConditionReplacementLevel",
            "ConditionDisposalLevel"
        ],
        "Pset_MaintenanceTriggerDuration": [
            "DurationTargetPerformance", "DurationMaintenanceLevel", "DurationReplacementLevel",
            "DurationDisposalLevel"
        ],
        "Pset_MaintenanceTriggerPerformance": [
            "TargetPerformance", "PerformanceMaintenanceLevel", "ReplacementLevel", "DisposalLevel"
        ],
        "Pset_ManufacturerOccurrence": [
            "AcquisitionDate", "BarCode", "SerialNumber", "BatchReference", "AssemblyPlace", "ManufacturingDate"
        ],
        "Pset_ManufacturerTypeInformation": [
            "GlobalTradeItemNumber", "ArticleNumber", "ModelReference", "ModelLabel", "Manufacturer",
            "ProductionYear", "AssemblyPlace", "OperationalDocument", "SafetyDocument", "PerformanceCertificate"
        ],
        "Pset_RepairOccurrence": [
            "RepairContent", "RepairDate", "MeanTimeToRepair"
        ],
        "Pset_Risk": [
            "RiskName", "RiskType", "NatureOfRisk", "RiskAssessmentMethodology",
            "UnmitigatedRiskLikelihood", "UnmitigatedRiskConsequence", "UnmitigatedRiskSignificance",
            "MitigationPlanned", "MitigatedRiskLikelihood", "MitigatedRiskConsequence",
            "MitigatedRiskSignificance", "MitigationProposed", "AssociatedProduct",
            "AssociatedActivity", "AssociatedLocation"
        ],
        "Pset_ServiceLife": [
            "ServiceLifeDuration", "MeanTimeBetweenFailure"
        ],
        "Pset_Tolerance": [
            "ToleranceDescription", "ToleranceBasis", "OverallTolerance", "HorizontalTolerance",
            "OrthogonalTolerance", "VerticalTolerance", "PlanarFlatness", "HorizontalFlatness",
            "ElevationalFlatness", "SideFlatness", "OverallOrthogonality", "HorizontalOrthogonality",
            "OrthogonalOrthogonality", "VerticalOrthogonality", "OverallStraightness",
            "HorizontalStraightness", "OrthogonalStraightness", "VerticalStraightness"
        ],
        "Pset_Uncertainty": [
            "UncertaintyBasis", "UncertaintyDescription", "HorizontalUncertainty",
            "LinearUncertainty", "OrthogonalUncertainty", "VerticalUncertainty"
        ],
        "Pset_Warranty": [
            "WarrantyIdentifier", "WarrantyStartDate", "IsExtendedWarranty",
            "WarrantyPeriod", "WarrantyContent", "PointOfContact", "Exclusions"
        ],
        "Qto_BodyGeometryValidation": [
            "GrossSurfaceArea", "NetSurfaceArea", "GrossVolume", "NetVolume",
            "SurfaceGenusBeforeFeatures", "SurfaceGenusAfterFeatures"
        ],
        "Qto_CurtainWallQuantities": [
            "Length", "Height", "Width"
        ]
    },    


    # Altri elementi di supporto o infrastrutturali
    "IfcFootingType": {
        "Pset_ConcreteElementGeneral": [
            "AssemblyPlace", "CastingMethod", "StructuralClass", "StrengthClass",
            "ExposureClass", "ReinforcementVolumeRatio", "ReinforcementAreaRatio",
            "DimensionalAccuracyClass", "ConstructionToleranceClass", "ConcreteCover",
            "ConcreteCoverAtMainBars", "ConcreteCoverAtLinks", "ReinforcementStrengthClass"
        ],
        "Pset_Condition": [
            "AssessmentDate", "AssessmentCondition", "AssessmentDescription",
            "AssessmentType", "AssessmentMethod", "LastAssessmentReport",
            "NextAssessmentDate", "AssessmentFrequency"
        ],
        "Pset_ConstructionAdministration": [
            "ProcurementMethod", "SpecificationSectionNumber", "SubmittalIdentifer"
        ],
        "Pset_ElementKinematics": [
            "CyclicPath", "CyclicRange", "LinearPath", "LinearRange",
            "MaximumAngularVelocity", "MaximumConstantSpeed", "MinimumTime"
        ],
        "Pset_EnvironmentalCondition": [
            "ReferenceAirRelativeHumidity", "ReferenceEnvironmentTemperature",
            "MaximumAtmosphericPressure", "StorageTemperatureRange", "MaximumWindSpeed",
            "OperationalTemperatureRange", "MaximumRainIntensity", "SaltMistLevel",
            "SeismicResistance", "SmokeLevel", "MaximumSolarRadiation"
        ],
        "Pset_EnvironmentalImpactIndicators": [
            "Reference", "FunctionalUnitReference", "IndicatorsUnit", "LifeCyclePhase",
            "ExpectedServiceLife", "TotalPrimaryEnergyConsumptionPerUnit",
            "WaterConsumptionPerUnit", "HazardousWastePerUnit", "NonHazardousWastePerUnit",
            "ClimateChangePerUnit", "AtmosphericAcidificationPerUnit",
            "RenewableEnergyConsumptionPerUnit", "NonRenewableEnergyConsumptionPerUnit",
            "ResourceDepletionPerUnit", "InertWastePerUnit", "RadioactiveWastePerUnit",
            "StratosphericOzoneLayerDestructionPerUnit", "PhotochemicalOzoneFormationPerUnit",
            "EutrophicationPerUnit"
        ],
        "Pset_EnvironmentalImpactValues": [
            "TotalPrimaryEnergyConsumption", "WaterConsumption", "HazardousWaste",
            "NonHazardousWaste", "ClimateChange", "AtmosphericAcidification",
            "RenewableEnergyConsumption", "NonRenewableEnergyConsumption", "ResourceDepletion",
            "InertWaste", "RadioactiveWaste", "StratosphericOzoneLayerDestruction",
            "PhotochemicalOzoneFormation", "Eutrophication", "LeadInTime", "Duration", "LeadOutTime"
        ],
        "Pset_FootingCommon": ["Reference", "Status", "LoadBearing"],
        "Pset_FootingTypePadFooting": ["LoadBearingCapacity", "IsReinforced"],
        "Pset_MaintenanceStrategy": ["AssetCriticality", "AssetFrailty", "AssetPriority", "MonitoringType", "AccidentResponse"],
        "Pset_MaintenanceTriggerCondition": ["ConditionTargetPerformance", "ConditionMaintenanceLevel", "ConditionReplacementLevel", "ConditionDisposalLevel"],
        "Pset_MaintenanceTriggerDuration": ["DurationTargetPerformance", "DurationMaintenanceLevel", "DurationReplacementLevel", "DurationDisposalLevel"],
        "Pset_MaintenanceTriggerPerformance": ["TargetPerformance", "PerformanceMaintenanceLevel", "ReplacementLevel", "DisposalLevel"],
        "Pset_ManufacturerTypeInformation": ["GlobalTradeItemNumber", "ArticleNumber", "ModelReference", "ModelLabel", "Manufacturer", "ProductionYear", "AssemblyPlace", "OperationalDocument", "SafetyDocument", "PerformanceCertificate"],
        "Pset_PrecastConcreteElementFabrication": ["TypeDesignation", "ProductionLotId", "SerialNumber", "PieceMark", "AsBuiltLocationNumber", "ActualProductionDate", "ActualErectionDate"],
        "Pset_PrecastConcreteElementGeneral": ["TypeDesignation", "CornerChamfer", "ManufacturingToleranceClass", "FormStrippingStrength", "LiftingStrength", "ReleaseStrength", "MinimumAllowableSupportLength", "InitialTension", "TendonRelaxation", "TransportationStrength", "SupportDuringTransportDescription", "SupportDuringTransportDocReference", "HollowCorePlugging", "CamberAtMidspan", "BatterAtStart", "BatterAtEnd", "Twisting", "Shortening", "PieceMark", "DesignLocationNumber"],
        "Pset_ReinforcementBarCountOfIndependentFooting": ["Description", "Reference", "XDirectionLowerBarCount", "YDirectionLowerBarCount", "XDirectionUpperBarCount", "YDirectionUpperBarCount"],
        "Pset_ReinforcementBarPitchOfContinuousFooting": ["Description", "Reference", "CrossingUpperBarPitch", "CrossingLowerBarPitch"],
        "Pset_Risk": ["RiskName", "RiskType", "NatureOfRisk", "RiskAssessmentMethodology", "UnmitigatedRiskLikelihood", "UnmitigatedRiskConsequence", "UnmitigatedRiskSignificance", "MitigationPlanned", "MitigatedRiskLikelihood", "MitigatedRiskConsequence", "MitigatedRiskSignificance", "MitigationProposed", "AssociatedProduct", "AssociatedActivity", "AssociatedLocation"],
        "Pset_ServiceLife": ["ServiceLifeDuration", "MeanTimeBetweenFailure"],
        "Pset_Tolerance": ["ToleranceDescription", "ToleranceBasis", "OverallTolerance", "HorizontalTolerance", "OrthogonalTolerance", "VerticalTolerance", "PlanarFlatness", "HorizontalFlatness", "ElevationalFlatness", "SideFlatness", "OverallOrthogonality", "HorizontalOrthogonality", "OrthogonalOrthogonality", "VerticalOrthogonality", "OverallStraightness", "HorizontalStraightness", "OrthogonalStraightness", "VerticalStraightness"],
        "Pset_Uncertainty": ["UncertaintyBasis", "UncertaintyDescription", "HorizontalUncertainty", "LinearUncertainty", "OrthogonalUncertainty", "VerticalUncertainty"],
        "Pset_Warranty": ["WarrantyIdentifier", "WarrantyStartDate", "IsExtendedWarranty", "WarrantyPeriod", "WarrantyContent", "PointOfContact", "Exclusions"],
        "Qto_FootingBaseQuantities": ["Length", "Width", "Height", "CrossSectionArea"]
    },


    "IfcPile": {
        "Pset_ConcreteElementGeneral": [
            "AssemblyPlace", "CastingMethod", "StructuralClass", "StrengthClass",
            "ExposureClass", "ReinforcementVolumeRatio", "ReinforcementAreaRatio",
            "DimensionalAccuracyClass", "ConstructionToleranceClass", "ConcreteCover",
            "ConcreteCoverAtMainBars", "ConcreteCoverAtLinks", "ReinforcementStrengthClass"
        ],
        "Pset_Condition": [
            "AssessmentDate", "AssessmentCondition", "AssessmentDescription",
            "AssessmentType", "AssessmentMethod", "LastAssessmentReport",
            "NextAssessmentDate", "AssessmentFrequency"
        ],
        "Pset_ConstructionAdministration": [
            "ProcurementMethod", "SpecificationSectionNumber", "SubmittalIdentifer"
        ],
        "Pset_ConstructionOccurence": ["InstallationDate", "ModelNumber", "TagNumber", "AssetIdentifier"],
        "Pset_ElementKinematics": [
            "CyclicPath", "CyclicRange", "LinearPath", "LinearRange",
            "MaximumAngularVelocity", "MaximumConstantSpeed", "MinimumTime"
        ],
        "Pset_EnvironmentalCondition": [
            "ReferenceAirRelativeHumidity", "ReferenceEnvironmentTemperature",
            "MaximumAtmosphericPressure", "StorageTemperatureRange", "MaximumWindSpeed",
            "OperationalTemperatureRange", "MaximumRainIntensity", "SaltMistLevel",
            "SeismicResistance", "SmokeLevel", "MaximumSolarRadiation"
        ],
        "Pset_EnvironmentalImpactIndicators": [
            "Reference", "FunctionalUnitReference", "IndicatorsUnit", "LifeCyclePhase",
            "ExpectedServiceLife", "TotalPrimaryEnergyConsumptionPerUnit",
            "WaterConsumptionPerUnit", "HazardousWastePerUnit", "NonHazardousWastePerUnit",
            "ClimateChangePerUnit", "AtmosphericAcidificationPerUnit",
            "RenewableEnergyConsumptionPerUnit", "NonRenewableEnergyConsumptionPerUnit",
            "ResourceDepletionPerUnit", "InertWastePerUnit", "RadioactiveWastePerUnit",
            "StratosphericOzoneLayerDestructionPerUnit", "PhotochemicalOzoneFormationPerUnit",
            "EutrophicationPerUnit"
        ],
        "Pset_EnvironmentalImpactValues": [
            "TotalPrimaryEnergyConsumption", "WaterConsumption", "HazardousWaste",
            "NonHazardousWaste", "ClimateChange", "AtmosphericAcidification",
            "RenewableEnergyConsumption", "NonRenewableEnergyConsumption", "ResourceDepletion",
            "InertWaste", "RadioactiveWaste", "StratosphericOzoneLayerDestruction",
            "PhotochemicalOzoneFormation", "Eutrophication", "LeadInTime", "Duration", "LeadOutTime"
        ],
        "Pset_InstallationOccurrence": ["InstallationDate", "AcceptanceDate", "PutIntoOperationDate"],
        "Pset_MaintenanceStrategy": ["AssetCriticality", "AssetFrailty", "AssetPriority", "MonitoringType", "AccidentResponse"],
        "Pset_MaintenanceTriggerCondition": ["ConditionTargetPerformance", "ConditionMaintenanceLevel", "ConditionReplacementLevel", "ConditionDisposalLevel"],
        "Pset_MaintenanceTriggerDuration": ["DurationTargetPerformance", "DurationMaintenanceLevel", "DurationReplacementLevel", "DurationDisposalLevel"],
        "Pset_MaintenanceTriggerPerformance": ["TargetPerformance", "PerformanceMaintenanceLevel", "ReplacementLevel", "DisposalLevel"],
        "Pset_ManufacturerOccurrence": ["AcquisitionDate", "BarCode", "SerialNumber", "BatchReference", "AssemblyPlace", "ManufacturingDate"],
        "Pset_ManufacturerTypeInformation": ["GlobalTradeItemNumber", "ArticleNumber", "ModelReference", "ModelLabel", "Manufacturer", "ProductionYear", "AssemblyPlace", "OperationalDocument", "SafetyDocument", "PerformanceCertificate"],
        "Pset_PileCommon": ["Reference", "Status", "LoadBearing"],
        "Pset_PrecastConcreteElementFabrication": ["TypeDesignation", "ProductionLotId", "SerialNumber", "PieceMark", "AsBuiltLocationNumber", "ActualProductionDate", "ActualErectionDate"],
        "Pset_PrecastConcreteElementGeneral": ["TypeDesignation", "CornerChamfer", "ManufacturingToleranceClass", "FormStrippingStrength", "LiftingStrength", "ReleaseStrength", "MinimumAllowableSupportLength", "InitialTension", "TendonRelaxation", "TransportationStrength", "SupportDuringTransportDescription", "SupportDuringTransportDocReference", "HollowCorePlugging", "CamberAtMidspan", "BatterAtStart", "BatterAtEnd", "Twisting", "Shortening", "PieceMark", "DesignLocationNumber"],
        "Pset_RepairOccurrence": ["RepairContent", "RepairDate", "MeanTimeToRepair"],
        "Pset_Risk": ["RiskName", "RiskType", "NatureOfRisk", "RiskAssessmentMethodology", "UnmitigatedRiskLikelihood", "UnmitigatedRiskConsequence", "UnmitigatedRiskSignificance", "MitigationPlanned", "MitigatedRiskLikelihood", "MitigatedRiskConsequence", "MitigatedRiskSignificance", "MitigationProposed", "AssociatedProduct", "AssociatedActivity", "AssociatedLocation"],
        "Pset_ServiceLife": ["ServiceLifeDuration", "MeanTimeBetweenFailure"],
        "Pset_Tolerance": ["ToleranceDescription", "ToleranceBasis", "OverallTolerance", "HorizontalTolerance", "OrthogonalTolerance", "VerticalTolerance", "PlanarFlatness", "HorizontalFlatness", "ElevationalFlatness", "SideFlatness", "OverallOrthogonality", "HorizontalOrthogonality", "OrthogonalOrthogonality", "VerticalOrthogonality", "OverallStraightness", "HorizontalStraightness", "OrthogonalStraightness", "VerticalStraightness"],
        "Pset_Uncertainty": ["UncertaintyBasis", "UncertaintyDescription", "HorizontalUncertainty", "LinearUncertainty", "OrthogonalUncertainty", "VerticalUncertainty"],
        "Pset_Warranty": ["WarrantyIdentifier", "WarrantyStartDate", "IsExtendedWarranty", "WarrantyPeriod", "WarrantyContent", "PointOfContact", "Exclusions"],
        "Qto_BodyGeometryValidation": ["GrossSurfaceArea", "NetSurfaceArea", "GrossVolume", "NetVolume", "SurfaceGenusBeforeFeatures", "SurfaceGenusAfterFeatures"],
        "Qto_PileBaseQuantities": ["Length", "CrossSectionArea", "OuterSurfaceArea", "GrossSurfaceArea"]
    },  


    "IfcBridge": {
        "Pset_AirSideSystemInformation": [
            "Description", "AirSideSystemType", "AirSideSystemDistributionType", "TotalAirFlow",
            "EnergyGainTotal", "AirFlowSensible", "EnergyGainSensible", "EnergyLoss",
            "InfiltrationDiversitySummer", "InfiltrationDiversityWinter", "ApplianceDiversity",
            "HeatingTemperatureDelta", "CoolingTemperatureDelta", "Ventilation", "FanPower"
        ],
        "Pset_BridgeCommon": ["StructureIndicator"],
        "Pset_PropertyAgreement": [
            "AgreementType", "TrackingIdentifier", "AgreementVersion", "AgreementDate",
            "PropertyName", "CommencementDate", "TerminationDate", "Duration", "Options",
            "ConditionCommencement", "Restrictions", "ConditionTermination"
        ],
        "Pset_Risk": [
            "RiskName", "RiskType", "NatureOfRisk", "RiskAssessmentMethodology",
            "UnmitigatedRiskLikelihood", "UnmitigatedRiskConsequence", "UnmitigatedRiskSignificance",
            "MitigationPlanned", "MitigatedRiskLikelihood", "MitigatedRiskConsequence",
            "MitigatedRiskSignificance", "MitigationProposed", "AssociatedProduct",
            "AssociatedActivity", "AssociatedLocation"
        ],
        "Pset_SpaceAirHandlingDimensioning": [
            "CoolingDesignAirFlow", "HeatingDesignAirFlow", "SensibleHeatGain",
            "TotalHeatGain", "TotalHeatLoss", "CoolingDryBulb", "CoolingRelativeHumidity",
            "HeatingDryBulb", "HeatingRelativeHumidity", "VentilationDesignAirFlow",
            "DesignAirFlow", "CeilingRAPlenum", "BoundaryAreaHeatLoss"
        ],
        "Pset_SpaceCommon": [
            "Reference", "IsExternal", "GrossPlannedArea", "NetPlannedArea",
            "PubliclyAccessible", "HandicapAccessible"
        ],
        "Pset_SpaceCoveringRequirements": [
            "FloorCovering", "FloorCoveringThickness", "WallCovering", "WallCoveringThickness",
            "CeilingCovering", "CeilingCoveringThickness", "SkirtingBoard", "SkirtingBoardHeight",
            "Molding", "MoldingHeight", "ConcealedFlooring", "ConcealedFlooringOffset",
            "ConcealedCeiling", "ConcealedCeilingOffset"
        ],
        "Pset_SpaceFireSafetyRequirements": [
            "FireRiskFactor", "FlammableStorage", "FireExit", "SprinklerProtection",
            "SprinklerProtectionAutomatic", "AirPressurization"
        ],
        "Pset_SpaceHVACDesign": [
            "TemperatureSetPoint", "TemperatureMax", "TemperatureMin", "TemperatureSummerMax",
            "TemperatureSummerMin", "TemperatureWinterMax", "TemperatureWinterMin",
            "HumiditySetPoint", "HumidityMax", "HumidityMin", "HumiditySummer", "HumidityWinter",
            "DiscontinuedHeating", "NaturalVentilation", "NaturalVentilationRate",
            "MechanicalVentilation", "MechanicalVentilationRate", "AirConditioning",
            "AirConditioningCentral", "AirHandlingName"
        ],
        "Pset_SpaceLightingDesign": ["ArtificialLighting", "Illuminance"],
        "Pset_SpaceOccupancyRequirements": [
            "OccupancyType", "OccupancyNumber", "OccupancyNumberPeak", "OccupancyTimePerDay",
            "AreaPerOccupant", "MinimumHeadroom", "IsOutlookDesirable"
        ],
        "Pset_SpaceThermalLoad": [
            "People", "Lighting", "EquipmentSensible", "VentilationIndoorAir",
            "VentilationOutdoorAir", "RecirculatedAir", "ExhaustAir", "AirExchangeRate",
            "DryBulbTemperature", "RelativeHumidity", "InfiltrationSensible",
            "TotalSensibleLoad", "TotalLatentLoad", "TotalRadiantLoad"
        ],
        "Pset_SpaceThermalLoadPHistory": [
            "PeopleHistory", "LightingHistory", "EquipmentSensibleHistory",
            "VentilationIndoorAirHistory", "VentilationOutdoorAirHistory",
            "RecirculatedAirHistory", "ExhaustAirHistory", "AirExchangeRateTimeHistory",
            "DryBulbTemperatureHistory", "RelativeHumidityHistory", "InfiltrationSensibleHistory",
            "TotalSensibleLoadHistory", "TotalLatentLoadHistory", "TotalRadiantLoadHistory"
        ],
        "Pset_SpaceThermalPHistory": [
            "CoolingAirFlowRate", "HeatingAirFlowRate", "VentilationAirFlowRateHistory",
            "ExhaustAirFlowRate", "SpaceTemperatureHistory", "SpaceRelativeHumidity"
        ],
        "Pset_ThermalLoad": [
            "OccupancyDiversity", "LightingDiversity", "ApplianceDiversity", "OutsideAirPerPerson",
            "ReceptacleLoadIntensity", "AppliancePercentLoadToRadiant", "LightingLoadIntensity",
            "LightingPercentLoadToReturnAir", "TotalCoolingLoad", "TotalHeatingLoad",
            "InfiltrationDiversitySummer", "InfiltrationDiversityWinter", "LoadSafetyFactor"
        ],
        "Pset_Tolerance": [
            "ToleranceDescription", "ToleranceBasis", "OverallTolerance", "HorizontalTolerance",
            "OrthogonalTolerance", "VerticalTolerance", "PlanarFlatness", "HorizontalFlatness",
            "ElevationalFlatness", "SideFlatness", "OverallOrthogonality", "HorizontalOrthogonality",
            "OrthogonalOrthogonality", "VerticalOrthogonality", "OverallStraightness",
            "HorizontalStraightness", "OrthogonalStraightness", "VerticalStraightness"
        ],
        "Pset_Uncertainty": ["UncertaintyBasis", "UncertaintyDescription", "HorizontalUncertainty", "LinearUncertainty", "OrthogonalUncertainty", "VerticalUncertainty"],
        "Qto_BodyGeometryValidation": ["GrossSurfaceArea", "NetSurfaceArea", "GrossVolume"]
    },


    "IfcRamp": {
        "Pset_ConcreteElementGeneral": [
            "AssemblyPlace", "CastingMethod", "StructuralClass", "StrengthClass",
            "ExposureClass", "ReinforcementVolumeRatio", "ReinforcementAreaRatio",
            "DimensionalAccuracyClass", "ConstructionToleranceClass", "ConcreteCover",
            "ConcreteCoverAtMainBars", "ConcreteCoverAtLinks", "ReinforcementStrengthClass"
        ],
        "Pset_Condition": [
            "AssessmentDate", "AssessmentCondition", "AssessmentDescription",
            "AssessmentType", "AssessmentMethod", "LastAssessmentReport",
            "NextAssessmentDate", "AssessmentFrequency"
        ],
        "Pset_ConstructionAdministration": [
            "ProcurementMethod", "SpecificationSectionNumber", "SubmittalIdentifer"
        ],
        "Pset_ConstructionOccurence": ["InstallationDate", "ModelNumber", "TagNumber", "AssetIdentifier"],
        "Pset_ElementKinematics": [
            "CyclicPath", "CyclicRange", "LinearPath", "LinearRange",
            "MaximumAngularVelocity", "MaximumConstantSpeed", "MinimumTime"
        ],
        "Pset_EnvironmentalCondition": [
            "ReferenceAirRelativeHumidity", "ReferenceEnvironmentTemperature", "MaximumAtmosphericPressure",
            "StorageTemperatureRange", "MaximumWindSpeed", "OperationalTemperatureRange",
            "MaximumRainIntensity", "SaltMistLevel", "SeismicResistance", "SmokeLevel",
            "MaximumSolarRadiation"
        ],
        "Pset_EnvironmentalImpactIndicators": [
            "Reference", "FunctionalUnitReference", "IndicatorsUnit", "LifeCyclePhase",
            "ExpectedServiceLife", "TotalPrimaryEnergyConsumptionPerUnit", "WaterConsumptionPerUnit",
            "HazardousWastePerUnit", "NonHazardousWastePerUnit", "ClimateChangePerUnit",
            "AtmosphericAcidificationPerUnit", "RenewableEnergyConsumptionPerUnit",
            "NonRenewableEnergyConsumptionPerUnit", "ResourceDepletionPerUnit", "InertWastePerUnit",
            "RadioactiveWastePerUnit", "StratosphericOzoneLayerDestructionPerUnit",
            "PhotochemicalOzoneFormationPerUnit", "EutrophicationPerUnit"
        ],
        "Pset_EnvironmentalImpactValues": [
            "TotalPrimaryEnergyConsumption", "WaterConsumption", "HazardousWaste", "NonHazardousWaste",
            "ClimateChange", "AtmosphericAcidification", "RenewableEnergyConsumption",
            "NonRenewableEnergyConsumption", "ResourceDepletion", "InertWaste", "RadioactiveWaste",
            "StratosphericOzoneLayerDestruction", "PhotochemicalOzoneFormation", "Eutrophication",
            "LeadInTime", "Duration", "LeadOutTime"
        ],
        "Pset_InstallationOccurrence": ["InstallationDate", "AcceptanceDate", "PutIntoOperationDate"],
        "Pset_MaintenanceStrategy": [
            "AssetCriticality", "AssetFrailty", "AssetPriority", "MonitoringType", "AccidentResponse"
        ],
        "Pset_MaintenanceTriggerCondition": [
            "ConditionTargetPerformance", "ConditionMaintenanceLevel",
            "ConditionReplacementLevel", "ConditionDisposalLevel"
        ],
        "Pset_MaintenanceTriggerDuration": [
            "DurationTargetPerformance", "DurationMaintenanceLevel",
            "DurationReplacementLevel", "DurationDisposalLevel"
        ],
        "Pset_MaintenanceTriggerPerformance": [
            "TargetPerformance", "PerformanceMaintenanceLevel", "ReplacementLevel", "DisposalLevel"
        ],
        "Pset_ManufacturerOccurrence": [
            "AcquisitionDate", "BarCode", "SerialNumber", "BatchReference", "AssemblyPlace", "ManufacturingDate"
        ],
        "Pset_ManufacturerTypeInformation": [
            "GlobalTradeItemNumber", "ArticleNumber", "ModelReference", "ModelLabel",
            "Manufacturer", "ProductionYear", "AssemblyPlace", "OperationalDocument",
            "SafetyDocument", "PerformanceCertificate"
        ],
        "Pset_PrecastConcreteElementFabrication": [
            "TypeDesignation", "ProductionLotId", "SerialNumber", "PieceMark",
            "AsBuiltLocationNumber", "ActualProductionDate", "ActualErectionDate"
        ],
        "Pset_PrecastConcreteElementGeneral": [
            "TypeDesignation", "CornerChamfer", "ManufacturingToleranceClass", "FormStrippingStrength",
            "LiftingStrength", "ReleaseStrength", "MinimumAllowableSupportLength", "InitialTension",
            "TendonRelaxation", "TransportationStrength", "SupportDuringTransportDescription",
            "SupportDuringTransportDocReference", "HollowCorePlugging", "CamberAtMidspan",
            "BatterAtStart", "BatterAtEnd", "Twisting", "Shortening", "PieceMark", "DesignLocationNumber"
        ],
        "Pset_RampCommon": [
            "Reference", "Status", "RequiredHeadroom", "RequiredSlope", "HandicapAccessible",
            "HasNonSkidSurface", "FireExit", "IsExternal", "ThermalTransmittance", "LoadBearing", "FireRating"
        ],
        "Pset_RepairOccurrence": ["RepairContent", "RepairDate", "MeanTimeToRepair"],
        "Pset_Risk": [
            "RiskName", "RiskType", "NatureOfRisk", "RiskAssessmentMethodology",
            "UnmitigatedRiskLikelihood", "UnmitigatedRiskConsequence", "UnmitigatedRiskSignificance",
            "MitigationPlanned", "MitigatedRiskLikelihood", "MitigatedRiskConsequence",
            "MitigatedRiskSignificance", "MitigationProposed", "AssociatedProduct",
            "AssociatedActivity", "AssociatedLocation"
        ],
        "Pset_ServiceLife": ["ServiceLifeDuration", "MeanTimeBetweenFailure"],
        "Pset_Tolerance": [
            "ToleranceDescription", "ToleranceBasis", "OverallTolerance", "HorizontalTolerance",
            "OrthogonalTolerance", "VerticalTolerance", "PlanarFlatness", "HorizontalFlatness",
            "ElevationalFlatness", "SideFlatness", "OverallOrthogonality", "HorizontalOrthogonality",
            "OrthogonalOrthogonality", "VerticalOrthogonality", "OverallStraightness",
            "HorizontalStraightness", "OrthogonalStraightness", "VerticalStraightness"
        ],
        "Pset_Uncertainty": [
            "UncertaintyBasis", "UncertaintyDescription", "HorizontalUncertainty",
            "LinearUncertainty", "OrthogonalUncertainty", "VerticalUncertainty"
        ],
        "Pset_Warranty": [
            "WarrantyIdentifier", "WarrantyStartDate", "IsExtendedWarranty", "WarrantyPeriod",
            "WarrantyContent", "PointOfContact", "Exclusions"
        ],
        "Qto_BodyGeometryValidation": [
            "GrossSurfaceArea", "NetSurfaceArea", "GrossVolume", "NetVolume",
            "SurfaceGenusBeforeFeatures", "SurfaceGenusAfterFeatures"
        ]
    },


    "IfcStair":  {
        "Pset_ConcreteElementGeneral": [
            "AssemblyPlace", "CastingMethod", "StructuralClass", "StrengthClass",
            "ExposureClass", "ReinforcementVolumeRatio", "ReinforcementAreaRatio",
            "DimensionalAccuracyClass", "ConstructionToleranceClass", "ConcreteCover",
            "ConcreteCoverAtMainBars", "ConcreteCoverAtLinks", "ReinforcementStrengthClass"
        ],
        "Pset_Condition": [
            "AssessmentDate", "AssessmentCondition", "AssessmentDescription",
            "AssessmentType", "AssessmentMethod", "LastAssessmentReport",
            "NextAssessmentDate", "AssessmentFrequency"
        ],
        "Pset_ConstructionAdministration": [
            "ProcurementMethod", "SpecificationSectionNumber", "SubmittalIdentifer"
        ],
        "Pset_ConstructionOccurence": ["InstallationDate", "ModelNumber", "TagNumber", "AssetIdentifier"],
        "Pset_ElementKinematics": [
            "CyclicPath", "CyclicRange", "LinearPath", "LinearRange",
            "MaximumAngularVelocity", "MaximumConstantSpeed", "MinimumTime"
        ],
        "Pset_EnvironmentalCondition": [
            "ReferenceAirRelativeHumidity", "ReferenceEnvironmentTemperature", "MaximumAtmosphericPressure",
            "StorageTemperatureRange", "MaximumWindSpeed", "OperationalTemperatureRange",
            "MaximumRainIntensity", "SaltMistLevel", "SeismicResistance", "SmokeLevel",
            "MaximumSolarRadiation"
        ],
        "Pset_EnvironmentalImpactIndicators": [
            "Reference", "FunctionalUnitReference", "IndicatorsUnit", "LifeCyclePhase",
            "ExpectedServiceLife", "TotalPrimaryEnergyConsumptionPerUnit", "WaterConsumptionPerUnit",
            "HazardousWastePerUnit", "NonHazardousWastePerUnit", "ClimateChangePerUnit",
            "AtmosphericAcidificationPerUnit", "RenewableEnergyConsumptionPerUnit",
            "NonRenewableEnergyConsumptionPerUnit", "ResourceDepletionPerUnit", "InertWastePerUnit",
            "RadioactiveWastePerUnit", "StratosphericOzoneLayerDestructionPerUnit",
            "PhotochemicalOzoneFormationPerUnit", "EutrophicationPerUnit"
        ],
        "Pset_EnvironmentalImpactValues": [
            "TotalPrimaryEnergyConsumption", "WaterConsumption", "HazardousWaste", "NonHazardousWaste",
            "ClimateChange", "AtmosphericAcidification", "RenewableEnergyConsumption",
            "NonRenewableEnergyConsumption", "ResourceDepletion", "InertWaste", "RadioactiveWaste",
            "StratosphericOzoneLayerDestruction", "PhotochemicalOzoneFormation", "Eutrophication",
            "LeadInTime", "Duration", "LeadOutTime"
        ],
        "Pset_InstallationOccurrence": ["InstallationDate", "AcceptanceDate", "PutIntoOperationDate"],
        "Pset_MaintenanceStrategy": [
            "AssetCriticality", "AssetFrailty", "AssetPriority", "MonitoringType", "AccidentResponse"
        ],
        "Pset_MaintenanceTriggerCondition": [
            "ConditionTargetPerformance", "ConditionMaintenanceLevel",
            "ConditionReplacementLevel", "ConditionDisposalLevel"
        ],
        "Pset_MaintenanceTriggerDuration": [
            "DurationTargetPerformance", "DurationMaintenanceLevel",
            "DurationReplacementLevel", "DurationDisposalLevel"
        ],
        "Pset_MaintenanceTriggerPerformance": [
            "TargetPerformance", "PerformanceMaintenanceLevel", "ReplacementLevel", "DisposalLevel"
        ],
        "Pset_ManufacturerOccurrence": [
            "AcquisitionDate", "BarCode", "SerialNumber", "BatchReference", "AssemblyPlace", "ManufacturingDate"
        ],
        "Pset_ManufacturerTypeInformation": [
            "GlobalTradeItemNumber", "ArticleNumber", "ModelReference", "ModelLabel",
            "Manufacturer", "ProductionYear", "AssemblyPlace", "OperationalDocument",
            "SafetyDocument", "PerformanceCertificate"
        ],
        "Pset_PrecastConcreteElementFabrication": [
            "TypeDesignation", "ProductionLotId", "SerialNumber", "PieceMark",
            "AsBuiltLocationNumber", "ActualProductionDate", "ActualErectionDate"
        ],
        "Pset_PrecastConcreteElementGeneral": [
            "TypeDesignation", "CornerChamfer", "ManufacturingToleranceClass", "FormStrippingStrength",
            "LiftingStrength", "ReleaseStrength", "MinimumAllowableSupportLength", "InitialTension",
            "TendonRelaxation", "TransportationStrength", "SupportDuringTransportDescription",
            "SupportDuringTransportDocReference", "HollowCorePlugging", "CamberAtMidspan",
            "BatterAtStart", "BatterAtEnd", "Twisting", "Shortening", "PieceMark", "DesignLocationNumber"
        ],
        "Pset_RepairOccurrence": ["RepairContent", "RepairDate", "MeanTimeToRepair"],
        "Pset_Risk": [
            "RiskName", "RiskType", "NatureOfRisk", "RiskAssessmentMethodology",
            "UnmitigatedRiskLikelihood", "UnmitigatedRiskConsequence", "UnmitigatedRiskSignificance",
            "MitigationPlanned", "MitigatedRiskLikelihood", "MitigatedRiskConsequence",
            "MitigatedRiskSignificance", "MitigationProposed", "AssociatedProduct",
            "AssociatedActivity", "AssociatedLocation"
        ],
        "Pset_ServiceLife": ["ServiceLifeDuration", "MeanTimeBetweenFailure"],
        "Pset_StairCommon": [
            "Reference", "Status", "NumberOfRiser", "NumberOfTreads", "RiserHeight", "TreadLength",
            "NosingLength", "WalkingLineOffset", "TreadLengthAtOffset", "TreadLengthAtInnerSide",
            "WaistThickness", "RequiredHeadroom", "HandicapAccessible", "HasNonSkidSurface",
            "IsExternal", "ThermalTransmittance", "LoadBearing", "FireRating", "FireExit"
        ],
        "Pset_Tolerance": [
            "ToleranceDescription", "ToleranceBasis", "OverallTolerance", "HorizontalTolerance",
            "OrthogonalTolerance", "VerticalTolerance", "PlanarFlatness", "HorizontalFlatness",
            "ElevationalFlatness", "SideFlatness", "OverallOrthogonality", "HorizontalOrthogonality",
            "OrthogonalOrthogonality", "VerticalOrthogonality", "OverallStraightness",
            "HorizontalStraightness", "OrthogonalStraightness", "VerticalStraightness"
        ],
        "Pset_Uncertainty": [
            "UncertaintyBasis", "UncertaintyDescription", "HorizontalUncertainty",
            "LinearUncertainty", "OrthogonalUncertainty", "VerticalUncertainty"
        ],
        "Pset_Warranty": [
            "WarrantyIdentifier", "WarrantyStartDate", "IsExtendedWarranty", "WarrantyPeriod",
            "WarrantyContent", "PointOfContact", "Exclusions"
        ],
        "Qto_BodyGeometryValidation": [
            "GrossSurfaceArea", "NetSurfaceArea", "GrossVolume", "NetVolume",
            "SurfaceGenusBeforeFeatures", "SurfaceGenusAfterFeatures"
        ]
    }
}