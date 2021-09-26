import geojson

def point_features(points, features=[]):
	"""creates a geojson features from the point list"""
	"""appends if features list is already specified"""
	for p in points:
		point = geojson.Point(p)
		features.append(geojson.Feature(geometry=point))
	return features

def polygon_features(polygons, features=[]):
	"""creates a geojson features from the polygon list"""
	"""appends if features list is already specified"""
	for p in polygons:
		polygon = geojson.Polygon([p])
		features.append(geojson.Feature(geometry=polygon))
	return features

def write_geojson_file(outputpath, features):
	"""writes features to a geojson file"""
	feature_collection = geojson.FeatureCollection(features)
	with open(outputpath, 'w') as f:
		geojson.dump(feature_collection, f)