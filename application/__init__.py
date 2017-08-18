from flask import Flask
from pymongo import MongoClient

application = Flask(__name__)
application.config.from_object('config')
dbclient = MongoClient('34.207.89.142', 27017)

