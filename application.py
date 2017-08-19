import logging
from random import randint
from flask import Flask, Response, request, jsonify, json, render_template
from flask_ask import Ask, statement, question, session
from application.mongo import db_add_wine, db_get_wine, db_update_wine, db_delete_wine, db_get_wine_by_fields

# Elastic Beanstalk initalization
application = Flask(__name__)
ask = Ask(application, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

@application.route('/', methods=['GET'])
def hello_winedb():
	return "Hello WineDB User!"

#
# Basic API to add/get/update/delete wine
#

@application.route('/wines/<fridgename>/<shelfnumber>', methods=['POST'])
def add_wine_to_fridge(fridgename, shelfnumber):
	wine = json.loads(request.data)
	wine['fridge'] = fridgename
	wine['shelf'] = shelfnumber
	return jsonify(db_add_wine(**wine))

@application.route('/wines', methods=['POST'])
def add_wine():
	wine = json.loads(request.data)

	# Allow wine to be supplied in "location" subdict or directly in fridge/shelf keys
	if 'location' in wine.keys():
		wine['fridge'] = wine['location']['fridge']
		wine['shelf'] = wine['location']['shelf']

	if 'fridge' not in wine.keys() or 'shelf' not in wine.keys():
		return ('Must specify wine location (fridge/shelf) in path or POST body', 400)

	return jsonify(db_add_wine(**wine))

@application.route('/wines/<wineid>',  methods=['GET'])
def get_wine(wineid):
	wines = db_get_wine(wineid)
	return jsonify(wines)

@application.route('/wines/<wineid>',  methods=['PUT'])
def update_wine(wineid):
	wine = json.loads(request.data)

	if 'location' in wine.keys():
		wine['fridge'] = wine['location']['fridge']
		wine['shelf'] = wine['location']['shelf']
		del wine['location']

	return jsonify(db_update_wine(wineid, **wine))

@application.route('/wines/<wineid>', methods=['DELETE'])
def delete_wine(wineid):
	db_delete_wine(wineid)
	return ('', 204)

# 
# APIs to query database of wines based on wine attributes, locations.
# 

@application.route('/wines')
def get_all_wines():
	print(dict(request.args))
	wines = db_get_wine_by_fields(**dict(request.args))
	return jsonify(wines)

@application.route('/wines/<fridgename>/<shelfnumber>',  methods=['GET'])
def get_wine_on_shelf(fridgename, shelfnumber):
	wines = db_get_wine_by_fields(fridge=fridgename, shelf=shelfnumber, **dict(request.args))
	return jsonify(wines)

@application.route('/wines/<fridgename>',  methods=['GET'])
def get_wine_in_fridge(fridgename):
	wines = db_get_wine_by_fields(fridge=fridgename, **dict(request.args))
	return jsonify(wines)

@ask.launch
def launch_alexa():
    welcome_msg = render_template('welcome')
    return statement(welcome_msg)

# @ask.intent("YesIntent")
# def next_round():
#     numbers = [randint(0, 9) for _ in range(3)]
#     round_msg = render_template('round', numbers=numbers)
#     session.attributes['numbers'] = numbers[::-1]  # reverse
#     return question(round_msg)

# @ask.intent("AnswerIntent", convert={'first': int, 'second': int, 'third': int})
# def answer(first, second, third):
#     winning_numbers = session.attributes['numbers']
#     if [first, second, third] == winning_numbers:
#         msg = render_template('win')
#     else:
#         msg = render_template('lose')
#     return statement(msg)


if __name__ == '__main__':
    application.run(host='0.0.0.0')