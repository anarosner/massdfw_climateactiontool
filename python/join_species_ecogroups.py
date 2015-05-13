import arcpy
from arcpy import env
import os


### join study areas to habitats
##
#

geodb1 = "C:/ALR/Projects/MassDFW/Data/dfw_study_areas.gdb"
geodb2 = "C:/ALR/Projects/MassDFW/Data/dfw_habitats.gdb"
geodb3 = "C:/ALR/Projects/MassDFW/Data/dfw_geoprocessing.gdb"

i = "town"
i = "watershed"
j = "formation"
j = "macrogroup_forest"
j = "forest_type"
#"formation","macrogroup_forest","forest_type"

for i in ["town","watershed"]:
	print i
	for j in ["forest_type"]:
		print j
		arcpy.gp.Combine_sa( geodb1 + "/" + i + "_raster;" + geodb2 + "/" + j,
		geodb3 + "/" + i + "_" + j )

		arcpy.TableToTable_conversion( in_rows=geodb3 + "/" + i + "_" + j,
		out_path="C:/ALR/Projects/MassDFW/Data/tables/joins/",
		out_name= i + "_" + j + ".dbf" )





### join study areas to species
##
#
geodb1 = "C:/ALR/Projects/MassDFW/Data/dfw_study_areas.gdb"
geodb2 = "C:/ALR/Projects/MassDFW/Data/dfw_species.gdb"
geodb3 = "C:/ALR/Projects/MassDFW/Data/dfw_geo_species.gdb"

env.workspace = geodb2
species = arcpy.ListRasters()

for i in ["town","watershed"]:
	print i
	for j in species:
		print j
		arcpy.gp.Combine_sa( geodb1 + "/" + i + "_raster;" + geodb2 + "/" + j,
		geodb3 + "/" + i + "_" + j )

		arcpy.TableToTable_conversion( in_rows=geodb3 + "/" + i + "_" + j,
		out_path="C:/ALR/Projects/MassDFW/Data/tables/species_joins/",
		out_name= i + "_" + j + ".dbf" )



# i = "town"
# param = geodb1 + "/" + i + "_raster" 
# for j in species:
	# param = param + "; " + geodb2 + "/" + j	
	
# for j in species:
	# arcpy.gp.Combine_sa( geodb1 + "/" + i + "_raster;" + geodb2 + "/" + j,
	# geodb3 + "/" + i + "_" + j )


# arcpy.gp.Combine_sa( geodb1 + "/" + i + "_raster;" + geodb2 + "/" + j,
# geodb3 + "/" + i + "_species" )

	
# arcpy.TableToTable_conversion( in_rows=geodb3 + "/" + i + "_" + j,
# out_path="C:/ALR/Projects/MassDFW/Data/tables/species/",
# out_name= i + "_" + j + ".dbf" )



# arcpy.TableToTable_conversion(in_rows="C:/ALR/Projects/MassDFW/Data/dfw_geoprocessing.gdb/towns_formations",out_path="C:/ALR/Projects/MassDFW/Data/tables",out_name="towns_formations.dbf",where_clause="#",field_mapping="""towns_rast "towns_rast" true true false 4 Long 0 0 ,First,#,C:/ALR/Projects/MassDFW/Data/dfw_geoprocessing.gdb/towns_formations/Band_1,towns_raster,-1,-1;formations "formations" true true false 4 Long 0 0 ,First,#,C:/ALR/Projects/MassDFW/Data/dfw_geoprocessing.gdb/towns_formations/Band_1,formations,-1,-1""",config_keyword="#")


# arcpy.gp.Combine_sa("TOWNSSURVEY_Raster2;'ecosystems habitats/mass_formation'","C:/Users/arosner/Documents/ArcGIS/Default.gdb/town_formation_comb")

# arcpy.gp.Combine_sa("
# C:/ALR/Projects/MassDFW/Data/dfw_study_areas.gdb/towns_raster;C:/ALR/Projects/MassDFW/Data/dfw_habitats.gdb/mass_formation",
# 'C:/ALR/Projects/MassDFW/Data/dfw_study_areas.gdb/towns_raster;C:/ALR/Projects/MassDFW/Data/dfw_study_areas.gdb/formations'
# "C:/Users/arosner/Documents/ArcGIS/Default.gdb/town_formation_comb2")