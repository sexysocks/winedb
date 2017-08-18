from flask import Flask
from pymongo import MongoClient

application = Flask(__name__)
application.config.from_object('config')
dbclient = MongoClient('0.0.0.0', 27017)