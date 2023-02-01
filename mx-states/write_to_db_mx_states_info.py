import pymongo
import json
from pymongo import InsertOne

client = pymongo\
    .MongoClient("mongodb+srv://mexdata:mexdata@mexdatacluster.v6rgzzo.mongodb.net/?retryWrites=true&w=majority")

db = client.mexdata_sandbox
collection = db.mex_geojson_single

bulk_write_list = []

feature_collection = {
    "type": "FeatureCollection",
    "features": []
}


with open('mx_states.json') as f:
    data = json.load(f)
    for feature in data['features']:
        feature_collection['features'].append(feature)

with open('mx_states_2.json') as f:
    data = json.load(f)
    for feature in data['features']:
        feature_collection['features'].append(feature)

with open('mx_states_3.json') as f:
    data = json.load(f)
    for feature in data['features']:
        feature_collection['features'].append(feature)


bulk_write_list.append(InsertOne(feature_collection))

result = collection.bulk_write(bulk_write_list)
client.close()

# for jsonObj in data['data']:
    # myDict = json.load(jsonObj)
    #print(jsonObj)
    # bulk_write_list.append(InsertOne(jsonObj))
