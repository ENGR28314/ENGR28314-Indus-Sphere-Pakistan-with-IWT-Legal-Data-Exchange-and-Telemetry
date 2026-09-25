"""Structured socio-economic and agro-economic reference inputs."""

CROP_SEASONS = {
    "Kharif": {"period":"Typically April–October (timing varies by crop and locality).","crops":["Rice","Cotton","Maize","Sugarcane","Sorghum","Millet","Mung bean","Mash bean"],"water_focus":"Higher summer irrigation demand; monsoon and canal availability can strongly affect scheduling."},
    "Rabi": {"period":"Typically October–April (timing varies by crop and locality).","crops":["Wheat","Gram/Chickpea","Barley","Mustard/Rapeseed","Canola","Lentil","Fodder"],"water_focus":"Winter irrigation demand is important for wheat and other cool-season crops."},
}

CROP_MATRIX = [
    {"season":"Rabi","crop":"Wheat","typical_window":"Oct–Apr","engineering_water_note":"Cool-season crop; irrigation scheduling is sensitive to winter rainfall, canal rotations and soil moisture."},
    {"season":"Rabi","crop":"Gram / Chickpea","typical_window":"Oct–Mar/Apr","engineering_water_note":"Generally lower water demand than wheat; supplemental irrigation can be important in dry periods."},
    {"season":"Rabi","crop":"Barley","typical_window":"Oct–Mar/Apr","engineering_water_note":"Cool-season cereal; water demand varies with climate, soil and planting date."},
    {"season":"Rabi","crop":"Mustard / Rapeseed","typical_window":"Oct–Feb/Mar","engineering_water_note":"Oilseed; avoid excessive irrigation near maturity while maintaining establishment moisture."},
    {"season":"Kharif","crop":"Rice","typical_window":"Apr/May–Sep/Oct","engineering_water_note":"High seasonal water demand; land levelling, irrigation efficiency and drainage strongly affect performance."},
    {"season":"Kharif","crop":"Cotton","typical_window":"Apr/May–Oct/Nov","engineering_water_note":"Sensitive to water stress during flowering and boll development; drainage and irrigation timing matter."},
    {"season":"Kharif","crop":"Maize","typical_window":"Spring/Summer","engineering_water_note":"Water requirement depends on hybrid, planting date and heat; critical stages include flowering and grain filling."},
    {"season":"Kharif","crop":"Sugarcane","typical_window":"Annual / seasonal establishment","engineering_water_note":"Long-duration crop with substantial irrigation requirement; conveyance and field efficiency are important."},
]

APICULTURE_INDICATORS = [
    {"indicator":"Colonies / hives","unit":"count","description":"Number of managed bee colonies used for honey and pollination services."},
    {"indicator":"Honey production","unit":"tonnes","description":"Harvested honey output; can be linked to forage, climate and management conditions."},
    {"indicator":"Apiary sites","unit":"count","description":"Number of apiary locations or managed production sites."},
    {"indicator":"Forage area","unit":"ha","description":"Estimated area supporting flowering plants and seasonal forage availability."},
]

AQUACULTURE_INDICATORS = [
    {"indicator":"Aquaculture production","unit":"tonnes","description":"Harvested production from managed ponds, tanks or other culture systems."},
    {"indicator":"Pond area","unit":"ha","description":"Water surface area used for managed aquaculture."},
    {"indicator":"Stocking density","unit":"fish/m²","description":"Number or biomass of stocked organisms per unit water area."},
    {"indicator":"Dissolved oxygen","unit":"mg/L","description":"Key water-quality variable affecting fish survival, growth and feeding performance."},
]

# Backward-compatible aliases used by earlier versions.
APICULTURE = {x["indicator"]: x["description"] for x in APICULTURE_INDICATORS}
AQUACULTURE = {x["indicator"]: x["description"] for x in AQUACULTURE_INDICATORS}

SOCIO_ECONOMIC_INPUTS = ["Population / households","Employment / labor force","Poverty / income","Urban growth","Food security","Education","Health access","Tourism","Domestic water utility","Industrial water utility","Energy access / generation","Climate vulnerability"]
AGRO_ECONOMIC_INPUTS = ["Cultivated area","Irrigated area","Crop yield","Crop production","Farm-gate value","Input costs","Rural employment","Livestock","Fisheries","Apiculture","Aquaculture","Water productivity"]

SOCIO_AGRO_COLUMNS = ["Province / Region","Cultivated area (ha)","Crop production (tonnes)","Employment (persons)","Honey production (tonnes)","Aquaculture production (tonnes)"]
DEFAULT_SOCIO_AGRO = [
    ["Punjab",1000000,5000000,2500000,1200,18000],
    ["Sindh",700000,3200000,1400000,700,24000],
    ["Khyber Pakhtunkhwa",450000,1800000,900000,500,6000],
    ["Balochistan",250000,600000,450000,300,2500],
    ["Gilgit-Baltistan",90000,250000,160000,250,900],
    ["Azad Jammu & Kashmir",120000,400000,220000,350,1200],
    ["Islamabad Capital Territory",12000,35000,25000,20,100],
]
