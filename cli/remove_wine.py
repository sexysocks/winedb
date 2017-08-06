import db.mongo
from pymongo import MongoClient

if __name__ == '__main__':
	args = {
		'producer': input("Producer: ").lower(),
		'varietal': input("Varietal: ").lower(),
		'vintage': input("Vintage: ").lower(),
		'fridge': input("Fridge Name: ").lower(),
		'shelf': input("Shelf Number: ").lower()
	}

	print(db.mongo.remove_wine(**args))
