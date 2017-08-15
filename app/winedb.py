from flask import Flask, Response, request, jsonify, json
app = Flask(__name__)

import db.mongo

@app.route('/')
def hello_winedb():
    return 'This is WineDB!'

# To query all wines
@app.route('/wines')
def get_all_wines():
	print(dict(request.args))
	wines = db.mongo.find_wine_by_fields(**dict(request.args))
	return jsonify(wines)

@app.route('/wines/<fridgename>/<shelfnumber>',  methods=['GET'])
def get_wine_on_shelf(fridgename, shelfnumber):
	wines = db.mongo.find_wine_by_fields(fridge=fridgename, shelf=shelfnumber, **dict(request.args))
	return jsonify(wines)

@app.route('/wines/<fridgename>',  methods=['GET'])
def get_wine_in_fridge(fridgename):
	wines = db.mongo.find_wine_by_fields(fridge=fridgename, **dict(request.args))
	return jsonify(wines)

@app.route('/wines/<fridgename>/<shelfnumber>/<wineid>',  methods=['GET'])
def get_wine_by_id(fridgename, shelfnumber, wineid):
	wines = db.mongo.find_wine_by_id(wineid)
	return jsonify(wines)

@app.route('/wines/<wineid>',  methods=['GET'])
def get_wine_by_only_id(wineid):
	wines = db.mongo.find_wine_by_id(wineid)
	return jsonify(wines)

@app.route('/wines/<fridgename>/<shelfnumber>', methods=['POST'])
def add_wine(fridgename, shelfnumber):
	wine = json.loads(request.data)
	wine['fridge'] = fridgename
	wine['shelf'] = shelfnumber
	return jsonify(db.mongo.add_wine(**wine))

@app.route('/wines/<wineid>', methods=['DELETE'])
def delete_wine_by_only_id(wineid):
	db.mongo.remove_wine_by_id(wineid)
	return ('', 204)
