import arcpy
from arcpy import env
import os
import numpy


state_outline = "C:/ALR/Projects/MassDFW/Data/dfw_study_areas.gdb/mass_buffer_outline"



	
### prep naturserve terr habitat to state raster
##
#

geodb = "C:/ALR/Projects/MassDFW/Data/dfw_habitats.gdb"

# clip ne terr map to state outline
arcpy.gp.ExtractByMask_sa(
"C:/ALR/Data/EcoData/NatureServe/habmap141611/syst_ne141611",
state_outline,
geodb + "/habitat")



# reclassify habitats to formations
arcpy.gp.Lookup_sa(geodb + "/habitat",
"FORMATION",
geodb + "/formation")

# save table w/ formations ids
arcpy.TableToTable_conversion(in_rows=geodb + "/formation",
out_path="C:/ALR/Projects/MassDFW/Data/tables/habitats",
out_name="formation.dbf")

# reclassify habitats to macrogroups
arcpy.gp.Lookup_sa(geodb + "/habitat",
"MACROGROUP",
geodb + "/macrogroup")



### prep macrogroup -level forest layer 
##
#

geodb = "C:/ALR/Projects/MassDFW/Data/dfw_habitats.gdb"

# pull select macrogroup types for forest layer
arcpy.gp.ExtractByAttributes_sa( geodb + "/macrogroup",
"MACROGROUP = 'Boreal Upland Forest' OR MACROGROUP = 'Central Hardwood Swamp' OR MACROGROUP = 'Central Oak-Pine' OR MACROGROUP = 'Northern Hardwood & Conifer' OR MACROGROUP = 'Northern Swamp'",
geodb + "/macrogroup_forest")

# save table w/ forest ids
arcpy.TableToTable_conversion(in_rows=geodb + "/macrogroup_forest",
out_path="C:/ALR/Projects/MassDFW/Data/tables/habitats",
out_name="macrogroup_forest.dbf")


### prep custom forest layer (regrouped habitat-level definitions) 
##
#

# pull select habitats types for additional forest layer
arcpy.gp.ExtractByAttributes_sa( geodb + "/habitat",
"MACROGROUP = 'Boreal Upland Forest' OR MACROGROUP = 'Central Hardwood Swamp' OR MACROGROUP = 'Central Oak-Pine'  OR MACROGROUP = 'Coastal Plain Peat Swamp' OR MACROGROUP = 'Coastal Plain Peatland' OR MACROGROUP = 'Coastal Plain Swamp' OR MACROGROUP = 'Glade, Barren and Savanna' OR MACROGROUP = 'Large River Floodplain' OR MACROGROUP = 'Northern Hardwood & Conifer' OR MACROGROUP = 'Northern Peatland' OR MACROGROUP = 'Northern Swamp' OR MACROGROUP = 'Wet Meadow / Shrub Marsh'",
geodb + "/habitat_forest")

#add field for custom forest type
arcpy.AddField_management( in_table = geodb + "/habitat_forest" ,
field_name="forest_type",
field_type="text",
field_length=255,
field_is_nullable="NULLABLE",field_is_required="NON_REQUIRED",field_domain="#" )

#pull raster into local memory
arcpy.MakeRasterLayer_management( in_raster=geodb + "/habitat_forest",
out_rasterlayer="temp_hab_forest")

#set all rows to non-forest initially
arcpy.CalculateField_management(in_table="temp_hab_forest",
field="forest_type",
expression="'Non-forest'",expression_type="PYTHON")



#
# loop through custom forest types to save
# select by sql query, and set forest_type name
#

#Northern hardwood
arcpy.SelectLayerByAttribute_management(in_layer_or_view="temp_hab_forest",
selection_type="NEW_SELECTION",
where_clause="HABITAT = 'Laurentian-Acadian Northern Hardwood Forest' OR HABITAT = 'Laurentian-Acadian Red Oak-Northern Hardwood Forest'")

arcpy.CalculateField_management(in_table="temp_hab_forest",
field="forest_type",
expression="'Northern hardwood'",expression_type="PYTHON")

#Transition hardwood
arcpy.SelectLayerByAttribute_management(in_layer_or_view="temp_hab_forest",
selection_type="NEW_SELECTION",
where_clause="HABITAT = 'North Atlantic Coastal Plain Hardwood Forest' OR HABITAT = 'North Atlantic Coastal Plain Basin Swamp and Wet Hardwood Forest' OR HABITAT = 'Northern Appalachian-Acadian Conifer-Hardwood Acidic Swamp' OR HABITAT = 'Laurentian-Acadian Alkaline Conifer-Hardwood Swamp' OR HABITAT = 'Appalachian (Hemlock)-Northern Hardwood Forest'")

arcpy.CalculateField_management(in_table="temp_hab_forest",
field="forest_type",
expression="'Transition hardwood'",expression_type="PYTHON")

#Central hardwoods-pine
arcpy.SelectLayerByAttribute_management(in_layer_or_view="temp_hab_forest",
selection_type="NEW_SELECTION",
where_clause="HABITAT = 'Laurentian-Acadian Pine-Hemlock-Hardwood Forest' OR HABITAT = 'Northeastern Interior Dry-Mesic Oak Forest'")

arcpy.CalculateField_management(in_table="temp_hab_forest",
field="forest_type",
expression="'Central hardwoods-pine'",expression_type="PYTHON")

#Pitch pine-scrub oak
arcpy.SelectLayerByAttribute_management(in_layer_or_view="temp_hab_forest",
selection_type="NEW_SELECTION",
where_clause="HABITAT = 'North Atlantic Coastal Plain Pitch Pine Barrens' OR HABITAT = 'Northeastern Interior Pine Barrens' OR HABITAT = 'Central Appalachian Dry Oak-Pine Forest' OR HABITAT = 'Central Appalachian Pine-Oak Rocky Woodland' OR HABITAT = 'Laurentian-Acadian Northern Pine-(Oak) Forest' OR HABITAT = 'Northeastern Coastal and Interior Pine-Oak Forest'")

arcpy.CalculateField_management(in_table="temp_hab_forest",
field="forest_type",
expression="'Pitch pine-scrub oak'",expression_type="PYTHON")

#Spruce-Fir
arcpy.SelectLayerByAttribute_management(in_layer_or_view="temp_hab_forest",
selection_type="NEW_SELECTION",
where_clause="HABITAT = 'Acadian Sub-boreal Spruce Flat' OR HABITAT = 'Acadian Low Elevation Spruce-Fir-Hardwood Forest' OR HABITAT = 'Acadian-Appalachian Montane Spruce-Fir-Hardwood Forest'")

arcpy.CalculateField_management(in_table="temp_hab_forest",
field="forest_type",
expression="'Spruce-fir'",expression_type="PYTHON")

#Other forest
arcpy.SelectLayerByAttribute_management(in_layer_or_view="temp_hab_forest",
selection_type="NEW_SELECTION",
where_clause="HABITAT = 'North Atlantic Coastal Plain Maritime Forest' OR HABITAT = 'North-Central Interior Wet Flatwoods' OR HABITAT = 'Central Appalachian Alkaline Glade and Woodland' OR HABITAT = 'Glacial Marine & Lake Wet Clayplain Forest'  OR HABITAT = 'Glacial Marine & Lake Mesic Clayplain Forest'")

arcpy.CalculateField_management(in_table="temp_hab_forest",
field="forest_type",
expression="'Other forest'",expression_type="PYTHON")

#
# create new raster and table of custom forest types
#

#resave raster without the "non forest" rows  
arcpy.gp.ExtractByAttributes_sa( geodb + "/habitat_forest",
"forest_type <> 'Non-forest' ",
geodb + "/forest_type1")

# reclassify values by forest group
arcpy.gp.Lookup_sa(geodb + "/forest_type1",
"forest_type",
geodb + "/forest_type")

# save table w/ forest group ids
arcpy.TableToTable_conversion(in_rows=geodb + "/forest_type",
out_path="C:/ALR/Projects/MassDFW/Data/tables/habitats",
out_name="forest_type.dbf")


### notes on definition for forest types
##
#

x	
#

	# Northern hardwood (NH)
	Laurentian-Acadian Northern Hardwood Forest
	Laurentian-Acadian Red Oak-Northern Hardwood Forest

	
	# Transition hardwood (TH)
	North Atlantic Coastal Plain Hardwood Forest
	North Atlantic Coastal Plain Basin Swamp and Wet Hardwood Forest
	Northern Appalachian-Acadian Conifer-Hardwood Acidic Swamp
	Laurentian-Acadian Alkaline Conifer-Hardwood Swamp
	Appalachian (Hemlock)-Northern Hardwood Forest

	# Central hardwoods-pine (CHP)
	Laurentian-Acadian Pine-Hemlock-Hardwood Forest
	Northeastern Interior Dry-Mesic Oak Forest

	# Pitch pine-scrub oak, (PPSO)
	North Atlantic Coastal Plain Pitch Pine Barrens
	Northeastern Interior Pine Barrens
	Central Appalachian Dry Oak-Pine Forest
	Central Appalachian Pine-Oak Rocky Woodland
	Laurentian-Acadian Northern Pine-(Oak) Forest
	Northeastern Coastal and Interior Pine-Oak Forest

	# Spruce fir (SF)
	Acadian Sub-boreal Spruce Flat
	Acadian Low Elevation Spruce-Fir-Hardwood Forest
	Acadian-Appalachian Montane Spruce-Fir-Hardwood Forest
	
	# Other forest	
	North Atlantic Coastal Plain Maritime Forest
	North-Central Interior Wet Flatwoods
	Central Appalachian Alkaline Glade and Woodland
	Glacial Marine & Lake Wet Clayplain Forest
	Glacial Marine & Lake Mesic Clayplain Forest
	


	


