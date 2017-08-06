from flask import Flask
from flask import Response, jsonify, json, request
app = Flask(__name__)

import db.mongo

@app.route('/')
def hello_winedb():
    return 'This is WineDB!'

# To query all wines
@app.route('/wines')
def get_all_wines():
	wines = db.mongo.find_wine()
	return jsonify(wines)

@app.route('/wines/<fridgename>/<shelfnumber>',  methods=['GET'])
def get_wines_in_fridge(fridgename, shelfnumber):
	wines = db.mongo.find_wine(fridge=fridgename, shelf=shelfnumber)
	return jsonify(wines)

@app.route('/wines/<fridgename>/<shelfnumber>', methods=['POST'])
def add_wine(fridgename, shelfnumber):
	wine = json.loads(request.data)
	wine['fridge'] = fridgename
	wine['shelf'] = shelfnumber
	return jsonify(db.mongo.add_wine(**wine))

