from settings import DATABASE_URL
import pymongo
import json
from pymongo import InsertOne

client = pymongo\
    .MongoClient(DATABASE_URL)

db = client.mexdata_sandbox
collection = db.lmb_pitching_team

bulk_write_list = []

with open('../stats_files/team_pitching_LMB_stats.json') as f:
    data = json.load(f)
    for jsonObj in data['data']:
        bulk_write_list.append(InsertOne(jsonObj))

result = collection.bulk_write(bulk_write_list)
client.close()

# for jsonObj in data['data']:
    # myDict = json.load(jsonObj)
    #print(jsonObj)
    # bulk_write_list.append(InsertOne(jsonObj))
