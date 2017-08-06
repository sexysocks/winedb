import os
import logging
from pymongo import MongoClient

def add_wine(producer='', varietal='', vintage='', fridge='', shelf=''):
	wine_template = open(os.environ['PRODROOT'] + '/db/wine-template.json').read()

	entry = eval(wine_template % {'varietal': varietal.lower(),
								 'producer': producer.lower(),
								 'vintage': vintage,
								 'fridge': fridge.lower(),
								 'shelf': shelf})

	client = MongoClient('0.0.0.0', 27017)

	# Database name -- to remove it do "use winedb" and "db.dropDatabase()"
	db = client.winedb

	# Collection name
	wine = db.wine

	# Insert document for wine
	entry_wine_id = wine.insert_one(entry).inserted_id
	entry_wine = db.wine.find({'_id': entry_wine_id}).next()
	entry_wine['_id'] = str(entry_wine['_id'])
	return entry_wine

def find_wine(producer='', varietal='', vintage='', fridge='', shelf=''):
	wine_template = open(os.environ['PRODROOT'] + '/db/wine-template.json').read()

	entry = {}
	if producer:
		entry['producer'] = producer.lower()
	if varietal:
		entry['varietal'] = varietal.lower()
	if vintage:
		entry['vintage'] = vintage

	# TODO: figure out the right way to query this
	if fridge:
		entry['location'] = {}
		entry['location']['fridge'] = fridge.lower()
	if shelf:
		if 'location' not in entry.keys():
			entry['location'] = {}
		entry['location']['shelf'] = shelf

	client = MongoClient('0.0.0.0', 27017)

	# Database name -- to remove it do "use winedb" and "db.dropDatabase()"
	db = client.winedb

	# Collection name
	wine = db.wine
	query = db.wine.find(entry)

	result = []
	for w in query:
		logging.error(str(w))
		w['_id'] = str(w['_id'])
		result += [w]
	return result

def remove_wine(producer='', varietal='', vintage='', fridge='', shelf=''):
	wine_template = open(os.environ['PRODROOT'] + '/db/wine-template.json').read()

	entry = {}
	if producer:
		entry['producer'] = producer
	if varietal:
		entry['varietal'] = varietal
	if vintage:
		entry['vintage'] = vintage

	# TODO: figure out the right way to query this
	if fridge:
		entry['location'] = {}
		entry['location']['fridge'] = fridge
	if shelf:
		if 'location' not in entry.keys():
			entry['location'] = {}
		entry['location']['shelf'] = shelf

	client = MongoClient('0.0.0.0', 27017)

	# Database name -- to remove it do "use winedb" and "db.dropDatabase()"
	db = client.winedb

	# Collection name
	wine = db.wine
	query = db.wine.delete_many(entry)

	print("Deleted " + str(query.deleted_count) + " items from WineDB")
	return {}

