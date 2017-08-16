from flask import Flask, Response, request, jsonify, json
app = Flask(__name__)

import db.mongo

#
# Basic API to add/get/update/delete wine
#

@app.route('/wines/<fridgename>/<shelfnumber>', methods=['POST'])
def add_wine_to_fridge(fridgename, shelfnumber):
	wine = json.loads(request.data)
	wine['fridge'] = fridgename
	wine['shelf'] = shelfnumber
	return jsonify(db.mongo.add_wine(**wine))

@app.route('/wines', methods=['POST'])
def add_wine():
	wine = json.loads(request.data)

	# Allow wine to be supplied in "location" subdict or directly in fridge/shelf keys
	if 'location' in wine.keys():
		wine['fridge'] = wine['location']['fridge']
		wine['shelf'] = wine['location']['shelf']

	if 'fridge' not in wine.keys() or 'shelf' not in wine.keys():
		return ('Must specify wine location (fridge/shelf) in path or POST body', 400)

	return jsonify(db.mongo.add_wine(**wine))

@app.route('/wines/<wineid>',  methods=['GET'])
def get_wine(wineid):
	wines = db.mongo.get_wine(wineid)
	return jsonify(wines)

@app.route('/wines/<wineid>',  methods=['PUT'])
def update_wine(wineid):
	wine = json.loads(request.data)

	if 'location' in wine.keys():
		wine['fridge'] = wine['location']['fridge']
		wine['shelf'] = wine['location']['shelf']
		del wine['location']

	return jsonify(db.mongo.update_wine(wineid, **wine))

@app.route('/wines/<wineid>', methods=['DELETE'])
def delete_wine(wineid):
	db.mongo.delete_wine(wineid)
	return ('', 204)

# 
# APIs to query database of wines based on wine attributes, locations.
# 


@app.route('/wines')
def get_all_wines():
	print(dict(request.args))
	wines = db.mongo.get_wine_by_fields(**dict(request.args))
	return jsonify(wines)

@app.route('/wines/<fridgename>/<shelfnumber>',  methods=['GET'])
def get_wine_on_shelf(fridgename, shelfnumber):
	wines = db.mongo.get_wine_by_fields(fridge=fridgename, shelf=shelfnumber, **dict(request.args))
	return jsonify(wines)

@app.route('/wines/<fridgename>',  methods=['GET'])
def get_wine_in_fridge(fridgename):
	wines = db.mongo.get_wine_by_fields(fridge=fridgename, **dict(request.args))
	return jsonify(wines)


