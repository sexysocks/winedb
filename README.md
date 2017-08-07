# WineDB

## Application on Flask / MongoDB for managing a wine collection over 1 or more wine fridges.

# How to run WineDB

## Install and start Mongodb:

(On Mac OSX)

```
$ brew install mongodb
$ mongod
```

(or with custom config)

```
$ mongod -f conf/mongod.conf
```

## Get pymongo client

```
$ python -m pip install pymongo
```

## Set paths

```
$ export PRODROOT=(path to winedb code)
$ export PYTHONPATH=(path to winedb code):(path to winedb code)/app
$ export FLASK_APP=winedb.py
```

## Start the server

```
$ python -m flask run
```

## Example requests

```
$ curl -i http://127.0.0.1:5000/wines/right/1 --data-binary @test/wine.json -H "Content-type: application/json"
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 181
Server: Werkzeug/0.12.2 Python/3.6.1
Date: Mon, 07 Aug 2017 14:14:47 GMT

{
  "_id": "598875d7574590b379917363",
  "location": {
    "fridge": "right",
    "shelf": "1"
  },
  "producer": "homewood",
  "varietal": "sangiovese",
  "vintage": "2013"
}

$ curl -i http://127.0.0.1:5000/wines
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 205
Server: Werkzeug/0.12.2 Python/3.6.1
Date: Mon, 07 Aug 2017 14:14:59 GMT

[
  {
    "_id": "598875d7574590b379917363",
    "location": {
      "fridge": "right",
      "shelf": "1"
    },
    "producer": "homewood",
    "varietal": "sangiovese",
    "vintage": "2013"
  }
]

$ curl -i http://127.0.0.1:5000/wines/right/1
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 205
Server: Werkzeug/0.12.2 Python/3.6.1
Date: Mon, 07 Aug 2017 14:15:03 GMT

[
  {
    "_id": "598875d7574590b379917363",
    "location": {
      "fridge": "right",
      "shelf": "1"
    },
    "producer": "homewood",
    "varietal": "sangiovese",
    "vintage": "2013"
  }
]

$ curl -i http://127.0.0.1:5000/wines/right/1/598875d7574590b379917363 -X DELETE
HTTP/1.0 204 NO CONTENT
Content-Type: text/html; charset=utf-8
Content-Length: 0
Server: Werkzeug/0.12.2 Python/3.6.1
Date: Mon, 07 Aug 2017 14:15:16 GMT


$ curl -i http://127.0.0.1:5000/wines
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 3
Server: Werkzeug/0.12.2 Python/3.6.1
Date: Mon, 07 Aug 2017 14:15:21 GMT

[]
```

# Planned items:

## Basics:
1. More templates than just the basic
2. Verify query logic
3. Custom way to add fridges too?

## API:
1. REST API to add, remove, update, query wine
2. When loading new wine, query that lists open locations in the wine fridge to load new bottles
3. Query to suggest wine to drink based on age
4. Query to suggest wine to drink based on food pairing
5. Query to suggest wine based on activity (i.e. watching GoT, having happy hour, etc)

## DATA:
1. Add all the existing wine
2. Pre-populate suggested drink dates based on type/region 
3. Identify other source of "intelligence" for the wine, like wine websites with food pairing, etc

## DEPLOYMENT:

## EXTRAS:
1. Alexa skill to add, query, remove wine
