from deps.detection import hotspots
from deps.util import write_geojson_file

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

	hotspot_coords = hotspots(l1b_filepath, geo_filepath)

	output_path = "%i.geojson"%i
	write_geojson_file(output_path, hotspot_coords)

	print(output_path, "written")
	i += 1