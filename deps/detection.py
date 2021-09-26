import matplotlib.pyplot as plt # for debugging
import netCDF4
import cv2
import numpy

def coords_from_point(point, latitude_map, longitude_map):
	"""looks up point in latitude and longitude map and returns the geographical coordinate associated with that point"""
	# ordering of indices can be verified by looking at geojson.io
	lat = float(latitude_map[point[0]][point[1]])
	lon = float(longitude_map[point[0]][point[1]])
	coords = (lon, lat)
	return coords

def hotspots(l1b_filepath: str, geo_filepath: str):
	"""detects hotspots in the l1b dataset and uses the geographical dataset to convert the hotspots int geo locations"""
	"""returns single points and polygons"""
	nc_l1b = netCDF4.Dataset(l1b_filepath)
	nc_geo = netCDF4.Dataset(geo_filepath)

	# extract data
	observation_data = nc_l1b['observation_data']
	btl_data = observation_data['M13_brightness_temperature_lut'][:]
	m13 = observation_data['M13']
	scale_factor = m13.scale_factor
	add_offset = m13.add_offset
	m13_data = m13[:]
	geolocation_data = nc_geo['geolocation_data']
	latitude_data = geolocation_data['latitude'][:]
	longitude_data = geolocation_data['longitude'][:]
	get_coords = lambda point: coords_from_point(point, latitude_data, longitude_data)
	print("data extracted")

	# convert temperature values to brightness
	# 56.7°C because that is the highest recorded air temperature: https://en.wikipedia.org/wiki/Highest_temperature_recorded_on_Earth
	threshold_temperature = 56.7 + 273.15 # in kelvin
	u16_threshold_value = 0 # the value of the sensor ADC at which the temperature must be high enough
	i = 0
	for value in btl_data:
		if value > threshold_temperature :
			u16_threshold_value = i
			break
		i += 1
	
	# scale to brightness
	threshold_value = u16_threshold_value * scale_factor + add_offset
	print("Temperature: %.2fK is %i sensor adc => threshold brightness is %f"%(threshold_temperature, u16_threshold_value,threshold_value) )

	# filtering
	# ...

	# thresholding
	m13_data[m13_data==numpy.ma.masked]=numpy.nan # set masked values -- to NaN
	_, thresh = cv2.threshold(m13_data, threshold_value, 255, cv2.THRESH_BINARY)
	thresh = cv2.convertScaleAbs(thresh) # convert to 8 bit
	hotspot_image = thresh

	print("post processing completed")
	
	# Find hotspots
	contours, _ = cv2.findContours(hotspot_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	for i in range(len(contours)):
		contours[i] = numpy.squeeze(contours[i]) # opencv creates unneccary dimension, this removes it

	# extract coordinates for hotspots
	single_points = []
	polygons = []
	for c in contours:
		if c.ndim == 1: # 1 single point
			single_points.append(get_coords(c))
			continue
	
		# it has more than one point -> add a polygon
		polygon = []
		for point in c:
			polygon.append(get_coords((point[1], point[0])))
		polygon.append(get_coords((c[0][1], c[0][0]))) # append first to close loop
		polygons.append(polygon)

	print("coordinates collected")

	# DEBUGGING
	#plt.imshow(m13_data, cmap='hot', interpolation='nearest')
	#plt.show()
	#plt.imshow(hotspot_image, cmap='hot', interpolation='nearest')
	#plt.show()

	return single_points, polygons