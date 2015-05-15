import arcpy
from arcpy import env
import os
import numpy


geodb = "C:/ALR/Projects/MassDFW/Data/dfw_candidate_sites.gdb"
basedir = "C:/ALR/Data/ConnectivityData/CriticalLinkages"

mxd = arcpy.mapping.MapDocument("C:\ALR\Models\massdfw_climateactiontool\maps\mass dfw geoprocessing2.mxd")
df = arcpy.mapping.ListDataFrames(mxd)

### load/set-up terrestrial crossings
##
#

arcpy.CopyFeatures_management(in_features= basedir + "/link_roads_all.shp",
out_feature_class=geodb + "/terr_cross_point")

arcpy.AddField_management(in_table=geodb + "/terr_cross_point",
field_name="category",
field_type="LONG")

arcpy.MakeFeatureLayer_management(in_features=geodb + "/terr_cross_point",
out_layer="temp_terr_cross_point")


### assign categories
##
#

# brackets = ["00000","00500","01000","02500","05000","10000","100000"]
# for i in [0,1,2,3,4,5]:

	# arcpy.SelectLayerByAttribute_management(in_layer_or_view="temp_terr_cross_point",
	# selection_type="NEW_SELECTION",
	# where_clause="IEIdelta >= " + brackets[i] + " AND IEIdelta < " + brackets[i+1])

	# arcpy.CalculateField_management(in_table="temp_terr_cross_point",
	# field="category",
	# expression=int(brackets[i]),
	# expression_type="PYTHON")
	
brackets = [0,500,1000,2500,5000,100000]
for i in [0,1,2,3,4]:

	arcpy.SelectLayerByAttribute_management(in_layer_or_view="temp_terr_cross_point",
	selection_type="NEW_SELECTION",
	where_clause="IEIdelta >= " + str( brackets[i]+100 ) + " AND IEIdelta < " + str( brackets[i+1]-100) )

	arcpy.CalculateField_management(in_table="temp_terr_cross_point",
	field="category",
	expression=int(brackets[i]),
	expression_type="PYTHON")

# arcpy.CopyFeatures_management( in_features="C:/ALR/Data/ConnectivityData/CriticalLinkages/link_roads_all.shp",
# out_feature_class=geodb + "/terr_cross_point_" +str(brackets[i]) )
	

	
# # clear selection	
# arcpy.SelectLayerByAttribute_management(in_layer_or_view="temp_terr_cross_point",
# selection_type="CLEAR_SELECTION")



# arcpy.MakeFeatureLayer_management(in_features="temp_terr_cross_point",
# out_layer="temp_terr_cross_point_select")

# arcpy.DeleteFeatures_management("temp_terr_cross_point")

# buffer
# multi-part to single-point
# select by attributes for each category
# intersect w/ each consecutive pair
# erase lower from higher
# multi-part to single-point
# eliminate small polygons

### create buffers
##
#

# select points for buffer
arcpy.SelectLayerByAttribute_management(in_layer_or_view="temp_terr_cross_point",
selection_type="NEW_SELECTION",
where_clause="category IS NOT NULL" )

# create buffer 
arcpy.Buffer_analysis(in_features="temp_terr_cross_point",
out_feature_class= geodb + "/terr_cross_buffer",
buffer_distance_or_field="125 Meters",
dissolve_option="LIST",dissolve_field="category")

# multi-point to single-point
arcpy.MultipartToSinglepart_management(in_features=geodb + "/terr_cross_buffer",
out_feature_class=geodb + "/terr_cross_buffer_single")






### intersect, subtract, multi- to single-
##
#

arcpy.Intersect_analysis(in_features=geodb + "/terr_cross_buffer",
out_feature_class=geodb + "/terr_cross_intersect")

arcpy.MakeFeatureLayer_management(in_features=geodb + "/terr_cross_intersect",
out_layer="temp_terr_cross_intersect")


# intersect consecutive pairs
for i in [0,1,2,3,4,5]:

	arcpy.SelectLayerByAttribute_management(in_layer_or_view="temp_terr_cross_intersect",
	selection_type="NEW_SELECTION",
	where_clause="category = " + brackets[i])
	

	










	
	
arcpy.MakeFeatureLayer_management(in_features="temp_terr_cross_point",
out_layer="temp_terr_cross_point_" + brackets[i])



# <500
arcpy.SelectLayerByAttribute_management(in_layer_or_view="temp_terr_cross_point",
selection_type="NEW_SELECTION",
where_clause="IEIdelta < 500")

arcpy.CalculateField_management(in_table="temp_terr_cross_point",
field="category",
expression=0,
expression_type="PYTHON")

arcpy.MakeFeatureLayer_management(in_features="temp_terr_cross_point",
out_layer="temp_terr_cross_point_00000")

# 500-1000
arcpy.SelectLayerByAttribute_management(in_layer_or_view="temp_terr_cross_point",
selection_type="NEW_SELECTION",
where_clause="IEIdelta >= 500 AND IEIdelta < 1000")

arcpy.CalculateField_management(in_table="temp_terr_cross_point",
field="category",
expression=500,
expression_type="PYTHON")

arcpy.MakeFeatureLayer_management(in_features="temp_terr_cross_point",
out_layer="temp_terr_cross_point_500")

arcpy.Buffer_analysis(in_features="temp_terr_cross_point_500",
out_feature_class= geodb + "/terr_buffer_500",
buffer_distance_or_field="125 Meters",
dissolve_option="LIST",dissolve_field="category")








# 1000-2500
arcpy.SelectLayerByAttribute_management(in_layer_or_view="temp_terr_cross_point",
selection_type="NEW_SELECTION",
where_clause="IEIdelta >= 1000 AND IEIdelta < 2500")

arcpy.CalculateField_management(in_table="temp_terr_cross_point",
field="category",
expression=1000,
expression_type="PYTHON")

# 2500-5000
arcpy.SelectLayerByAttribute_management(in_layer_or_view="temp_terr_cross_point",
selection_type="NEW_SELECTION",
where_clause="IEIdelta >= 2500 AND IEIdelta < 5000")

arcpy.CalculateField_management(in_table="temp_terr_cross_point",
field="category",
expression=2500,
expression_type="PYTHON")

# 5000-10,000
arcpy.SelectLayerByAttribute_management(in_layer_or_view="temp_terr_cross_point",
selection_type="NEW_SELECTION",
where_clause="IEIdelta >= 5000 AND IEIdelta < 10000")

arcpy.CalculateField_management(in_table="temp_terr_cross_point",
field="category",
expression=5000,
expression_type="PYTHON")

# >10,000
arcpy.SelectLayerByAttribute_management(in_layer_or_view="temp_terr_cross_point",
selection_type="NEW_SELECTION",
where_clause="IEIdelta >= 10000")

arcpy.CalculateField_management(in_table="temp_terr_cross_point",
field="category",
expression=10000,
expression_type="PYTHON")


### create polygons
##
#

# buffer
arcpy.Buffer_analysis(in_features=geodb + "/terr_cross_point",
out_feature_class=geodb + "/terr_cross_buffer",
buffer_distance_or_field="125 Meters",
line_side="FULL",line_end_type="ROUND",
dissolve_option="LIST",dissolve_field="category")

# multi-part to single-part
arcpy.MultipartToSinglepart_management(in_features=geodb + "/terr_cross_buffer",
out_feature_class=geodb + "/terr_cross_polygon")

### remove lower score polygons where they overlap w/ higher
##
#






############
arcpy.CopyFeatures_management(in_features=temp_link_roads1,
out_feature_class=geodb + "/link_roads")

arcpy.MakeFeatureLayer_management(in_features=geodb + "/link_roads",
out_layer="/temp_link_roads")

arcpy.CalculateField_management(in_table="temp_road_crossings",field="category",expression="math.floor( !IEIdelta!/1000 )*1000",expression_type="PYTHON_9.3",code_block="#")

arcpy.Buffer_analysis(in_features="temp_road_crossings",out_feature_class="C:/Users/arosner/Documents/ArcGIS/Default.gdb/temp_road_crossings_dissolve3",buffer_distance_or_field="125 Meters",line_side="FULL",line_end_type="ROUND",dissolve_option="LIST",dissolve_field="category")

arcpy.MultipartToSinglepart_management(in_features="temp_road_crossings_dissolve3",out_feature_class="C:/Users/arosner/Documents/ArcGIS/Default.gdb/temp_road_crossings_dissolve4")

<500
>=500 AND <1000
>=1000 AND <2500
>=2000 AND <5000
>=5000 AND < 10000
>=10000

