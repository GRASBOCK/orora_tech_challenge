import matplotlib.pyplot as plt # for debugging
import netCDF4
import cv2
import numpy

def hotspots(l1b_filepath: str, geo_filepath: str):
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
	latitude = geolocation_data['latitude'][:]
	longitude = geolocation_data['longitude'][:]

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
	_, thresh = cv2.threshold(m13_data, threshold_value, 65535, cv2.THRESH_BINARY)

	# DEBUG plot
	#plt.imshow(m13_data, cmap='hot', interpolation='nearest')
	#plt.show()
	#plt.imshow(thresh, cmap='hot', interpolation='nearest')
	#plt.show()

	hotspot_image = thresh
	print("post processing completed")

	# extract indices of hotspots
	# origin: https://stackoverflow.com/a/27175491/5044463
	indices = numpy.asarray(numpy.where(hotspot_image == 65535)).T

	# create list of coords
	hotspot_coords = []
	for point in indices:
		# ordering of indices can be verified by looking at geojson.io
		lat = float(latitude[point[0]][point[1]])
		lon = float(longitude[point[0]][point[1]])
		coords = (lon, lat)
		hotspot_coords.append(coords)

	print("coordinates collected")

	return hotspot_coords