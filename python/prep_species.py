import arcpy
from arcpy import env
import os
import numpy


state_outline = "C:/ALR/Projects/MassDFW/Data/dfw_study_areas.gdb/mass_buffer_outline"


### prep GAP species layers
##
#

# clip GAP species rasters to state outline

geodb = "C:/ALR/Projects/MassDFW/Data/dfw_species.gdb"
basedir = "C:/ALR/Data/EcoData/USGS_GAP/to_process"
dirs = os.listdir(basedir)
csv_file = "C:/ALR/Data/EcoData/USGS_GAP/GAP_species_table.csv"	
tbl = numpy.recfromcsv(csv_file, delimiter=',', filling_values=numpy.nan, case_sensitive=True, deletechars='', replace_space=' ')


for i in dirs:
	env.workspace = basedir
	env.workspace = env.workspace + "/" + i
	layer = arcpy.ListRasters()[0]
	id = tbl[tbl['GAP_layer_name']==layer]['GAP_id'][0]

	arcpy.gp.ExtractByMask_sa(
	env.workspace + "/" + layer,
	state_outline,
	geodb + "/" + layer + "1")

	arcpy.AddField_management( in_table = geodb + "/" + layer + "1",
	field_name="GAP_id",
	field_type="LONG",
	field_is_nullable="NULLABLE",field_is_required="NON_REQUIRED",field_domain="#" )

	arcpy.CalculateField_management( in_table = geodb + "/" + layer + "1",
	field="GAP_id",
	expression=id,
	expression_type="PYTHON",code_block="#")
	
	arcpy.gp.Lookup_sa(geodb + "/" + layer + "1",
	"GAP_id",
	geodb + "/" + layer )
	
	arcpy.Delete_management(
	in_data=geodb + "/" + layer + "1",
	data_type="RasterDataset")

### prep GAP species layers
##
#

# clip GAP species rasters to state outline

geodb = "C:/ALR/Projects/MassDFW/Data/dfw_species_dsl.gdb"
basedir = "C:/ALR/Data/EcoData/DSL_species"
dirs = os.listdir(basedir)
csv_file = "C:/ALR/Data/EcoData/USGS_GAP/GAP_species_table.csv"	
tbl = numpy.recfromcsv(csv_file, delimiter=',', filling_values=numpy.nan, case_sensitive=True, deletechars='', replace_space=' ')


for i in dirs:
	env.workspace = basedir
	env.workspace = env.workspace + "/" + i
	layer = arcpy.ListRasters()[0].split(".")[0]
	id = tbl[tbl['GAP_layer_name']==layer]['GAP_id'][0]

	arcpy.gp.ExtractByMask_sa(
	env.workspace + "/" + arcpy.ListRasters()[0],
	state_outline,
	geodb + "/" + layer + "1")

	arcpy.AddField_management( in_table = geodb + "/" + layer + "1",
	field_name="GAP_id",
	field_type="LONG",
	field_is_nullable="NULLABLE",field_is_required="NON_REQUIRED",field_domain="#" )

	arcpy.CalculateField_management( in_table = geodb + "/" + layer + "1",
	field="GAP_id",
	expression=id,
	expression_type="PYTHON",code_block="#")
	
	arcpy.gp.Lookup_sa(geodb + "/" + layer + "1",
	"GAP_id",
	geodb + "/" + layer )
	
	arcpy.Delete_management(
	in_data=geodb + "/" + layer + "1",
	data_type="RasterDataset")
