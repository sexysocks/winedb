import os
import logging
from bson import ObjectId
from pymongo import MongoClient

def add_wine(category='', subcategory='', country='', region='', producer='',
		varietal='', vintage='', name='', fridge='', shelf=''):
	wine_template = open(os.environ['PRODROOT'] + '/db/wine-template.json').read()

	entry = eval(wine_template % {'category': category.lower(),
								  'subcategory': subcategory.lower(),
								  'country': country.lower(),
								  'region': region.lower(),
								  'name': name.lower(),
								  'varietal': varietal.lower(),
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
	entry_wine = next(db.wine.find({'_id': entry_wine_id}), None)
	if entry_wine:
		entry_wine['_id'] = str(entry_wine['_id'])
		return entry_wine
	return {}

def get_wine(wineid):
	entry = {'_id': ObjectId(wineid)}
	client = MongoClient('0.0.0.0', 27017)

	# Database name -- to remove it do "use winedb" and "db.dropDatabase()"
	db = client.winedb

	# Collection name
	wine = db.wine
	query = db.wine.find(entry)

	result = next(query, None)
	if result:
		result['_id'] = str(result['_id'])
		return result
	return {}

def delete_wine(wineid):
	entry = {'_id': ObjectId(wineid)}

	client = MongoClient('0.0.0.0', 27017)

	# Database name -- to remove it do "use winedb" and "db.dropDatabase()"
	db = client.winedb

	# Collection name
	wine = db.wine
	query = db.wine.delete_one(entry)

	print("Deleted " + str(query.deleted_count) + " items from WineDB")
	return {}

def update_wine(wineid, category='', subcategory='', country='', region='', producer='',
		varietal='', vintage='', name='', fridge='', shelf=''):
	entry = {}
	if producer:
		entry['producer'] = producer.lower()
	if varietal:
		entry['varietal'] = varietal.lower()
	if vintage:
		entry['vintage'] = vintage
	if category:
		entry['category'] = category.lower()
	if subcategory:
		entry['subcategory'] = subcategory.lower()
	if country:
		entry['country'] = country.lower()
	if region:
		entry['region'] = region.lower()
	if name:
		entry['name'] = name.lower()

	if fridge:
		entry['location.fridge'] = fridge.lower()
	if shelf:
		entry['location.shelf'] = shelf.lower()

	client = MongoClient('0.0.0.0', 27017)

	# Database name -- to remove it do "use winedb" and "db.dropDatabase()"
	db = client.winedb

	# Collection name
	wine = db.wine
	query = db.wine.update_one({'_id': ObjectId(wineid)}, {"$set": entry}, upsert=False)

	print("Updated " + str(query.modified_count) + " item in WineDB")
	return get_wine(wineid)

def get_wine_by_fields(category=[], subcategory=[], country=[], region=[], producer=[],
		varietal=[], vintage=[], name=[], fridge='', shelf=''):
	wine_template = open(os.environ['PRODROOT'] + '/db/wine-template.json').read()

	entry = {}
	for x in producer:
		entry['producer'] = x.lower()
	for x in varietal:
		entry['varietal'] = x.lower()
	for x in vintage:
		entry['vintage'] = x
	for x in category:
		entry['category'] = x.lower()
	for x in subcategory:
		entry['subcategory'] = x.lower()
	for x in country:
		entry['country'] = x.lower()
	for x in region:
		entry['region'] = x.lower()
	for x in name:
		entry['name'] = x.lower()

	if fridge:
		entry['location.fridge'] = fridge.lower()
	if shelf:
		entry['location.shelf'] = shelf.lower()

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
