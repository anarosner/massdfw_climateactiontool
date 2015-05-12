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



### prep forest layer 
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



# pull select habitats types for additional forest layer
arcpy.gp.ExtractByAttributes_sa( geodb + "/habitat",
"MACROGROUP = 'Boreal Upland Forest' OR MACROGROUP = 'Central Hardwood Swamp' OR MACROGROUP = 'Central Oak-Pine'  OR MACROGROUP = 'Coastal Plain Peat Swamp' OR MACROGROUP = 'Coastal Plain Peatland' OR MACROGROUP = 'Coastal Plain Swamp' OR MACROGROUP = 'Glade, Barren and Savanna' OR MACROGROUP = 'Large River Floodplain' OR MACROGROUP = 'Northern Hardwood & Conifer' OR MACROGROUP = 'Northern Peatland' OR MACROGROUP = 'Northern Swamp' OR MACROGROUP = 'Wet Meadow / Shrub Marsh'",
geodb + "/habitat_forest")

arcpy.AddField_management( in_table = geodb + "/habitat_forest" ,
field_name="forest_type",
field_type="text",
field_length=255,
field_is_nullable="NULLABLE",field_is_required="NON_REQUIRED",field_domain="#" )




##############
# to do

# open space
	# filter by prim_purp cons, cons and rec, habitat
	# lowercase site name
	# find rows w blank site name, paste site owner
	# dissolve by site name
	# create unique id of first polygon id with park_ prefix


	

##############
# done

# towns poly
	# create unique idea w/ town_ prefix
	# poly to raster
# NE Terrestrial Hab
	# extract by mask (clip) to MA
	# Table to table habitat
	# Lookup formations
	# Table to table formations
	# Lookup macrogroup
	# Table to table macrogroup
# combine
	# Combine towns formations
	# Table to table towns formations combine
# species
	# extract by mask to MA
	


