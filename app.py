from deps.detection import hotspots
from deps.geojson_util import point_features, polygon_features, write_geojson_file

# load dataset
dir = "C:/Users/grasb/Downloads/Suomi-NPP_sample_data"
files = [
	("VNP02MOD_NRT.A2020233.1000.001.nc","VNP03MOD_NRT.A2020233.1000.001.nc"),
	("VNP02MOD_NRT.A2020233.2118.001.nc","VNP03MOD_NRT.A2020233.2118.001.nc"),
	("VNP02MOD_NRT.A2020234.0942.001.nc","VNP03MOD_NRT.A2020234.0942.001.nc"),
	("VNP02MOD_NRT.A2020234.2100.001.nc","VNP03MOD_NRT.A2020234.2100.001.nc"),
	]

i = 0
for (file_l1b, file_geo) in files:
	l1b_filepath = dir + "/" + file_l1b
	geo_filepath = dir + "/" + file_geo
	# detection
	points, polygons = hotspots(l1b_filepath, geo_filepath)
	# geojson
	features = point_features(points)
	features = polygon_features(polygons, features)
	output_path = "%i.geojson"%i
	write_geojson_file(output_path, features)

	print(output_path, "written")
	i += 1