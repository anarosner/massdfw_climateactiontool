import arcpy
from arcpy import env
import os


geodb = "C:/ALR/Projects/MassDFW/Data/dfw_study_areas.gdb"


### create buffer of state outline
##
#
state_outline = "C:/ALR/Projects/MassDFW/Data/dfw_study_areas.gdb/mass_outline"

arcpy.Buffer_analysis(in_features=state_outline,
out_feature_class=geodb + "/mass_buffer_outline",
buffer_distance_or_field="100 Kilometers",
line_side="FULL",line_end_type="ROUND",dissolve_option="ALL",dissolve_field="#")


### prep towns
##
#

# towns to raster
arcpy.PolygonToRaster_conversion(in_features="C:/ALR/Data/GeneralSpatialData/towns/ma/TOWNSSURVEY_POLY.shp", 
value_field="TOWN_ID",
out_rasterdataset=geodb + "/town_raster",
cell_assignment="CELL_CENTER",priority_field="NONE",
cellsize="C:/ALR/Data/EcoData/NatureServe/habmap141611/syst_ne141611")

# save table w/ town ids
arcpy.TableToTable_conversion(in_rows="C:/ALR/Data/GeneralSpatialData/towns/ma/TOWNSSURVEY_POLY.shp",
out_path="C:/ALR/Projects/MassDFW/Data/tables/study_areas",
out_name="town.dbf")




### prep watersheds 
##
#

# create integer id field
arcpy.AddField_management(in_table="C:/ALR/Projects/MassDFW/Data/watershed.shp",
field_name="watershed",
field_type="SHORT",
field_precision="#",field_scale="#",field_length="#",field_alias="#",
field_is_nullable="NULLABLE",field_is_required="NON_REQUIRED",field_domain="#")

arcpy.CalculateField_management(in_table="C:/ALR/Projects/MassDFW/Data/watershed.shp",
field="watershed",
expression="!FID!",
expression_type="PYTHON",code_block="#")

# watersheds to raster
arcpy.PolygonToRaster_conversion(in_features="watershed", 
value_field="watershed",
out_rasterdataset=geodb + "/watershed_raster",
cell_assignment="CELL_CENTER",priority_field="NONE",
cellsize="C:/ALR/Data/EcoData/NatureServe/habmap141611/syst_ne141611")

# save table w/ watershed ids
arcpy.TableToTable_conversion(in_rows="C:/ALR/Projects/MassDFW/Data/watershed.shp",
out_path="C:/ALR/Projects/MassDFW/Data/tables/study_areas",
out_name="watershed.dbf")








# arcpy.PolygonToRaster_conversion(in_features="watershed",
# value_field="HUC8",
# out_rasterdataset="C:/Users/arosner/Documents/ArcGIS/Default.gdb/watershed_PolygonToRaster",
# cell_assignment="CELL_CENTER",priority_field="NONE",
# cellsize="C:/ALR/Data/EcoData/NatureServe/habmap141611/syst_ne141611")

# C:\ALR\Projects\MassDFW\Data\watershed.shp


# arcpy.FeatureToRaster_conversion(
# in_features=geodb + "/" + "huc8",
# field="HUC8",
# out_raster=geodb + "/huc8_raster",
# cell_size="C:/ALR/Data/EcoData/NatureServe/habmap141611/syst_ne141611")


# arcpy.FeatureToRaster_conversion(
# in_features=geodb + "/" + "huc8", 
# field="HUC8",
# out_raster=geodb + "/watershed_raster",
# cell_size="C:/ALR/Data/EcoData/NatureServe/habmap141611/syst_ne141611")





# arcpy.FeatureToRaster_conversion(
# in_features="C:/ALR/Projects/MassDFW/Data/dfw_study_areas.gdb/huc8",
# field="HUC8",
# out_raster="C:/Users/arosner/Documents/ArcGIS/Default.gdb/Feature_huc81",
# cell_size="C:/ALR/Data/EcoData/NatureServe/habmap141611/syst_ne141611")



# # data_dir = "C:/ALR/Data/StreamData/WBD/WBDHU8_June2013.gdb/WBDHU8"
# # arcpy.SelectLayerByLocation_management(
# # in_layer="WBDHU8",
# # overlap_type="INTERSECT",
# # select_features="C:/ALR/Projects/MassDFW/Data/dfw_study_areas.gdb/mass_outline",
# # search_distance="#",
# # selection_type="NEW_SELECTION")




# C:\ALR\Data\StreamData\WBD\WBDHU8_June2013.gdb

