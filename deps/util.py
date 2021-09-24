import geojson

def write_geojson_file(outputpath, coords):
	features = []
	for c in coords:
		point = geojson.Point(c)
		features.append(geojson.Feature(geometry=point))
	feature_collection = geojson.FeatureCollection(features)

	with open(outputpath, 'w') as f:
		geojson.dump(feature_collection, f)