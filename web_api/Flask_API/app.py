from flask import Flask
import pymongo
import json
from flask import Response

client = pymongo.MongoClient("mongodb://shivvu_123:gagan123@cluster0-shard-00-00.gcxus.mongodb.net:27017,cluster0-shard-00-01.gcxus.mongodb.net:27017,cluster0-shard-00-02.gcxus.mongodb.net:27017/test?ssl=true&replicaSet=atlas-83ocs2-shard-0&authSource=admin&retryWrites=true&w=majority")

db = client["company"]
collection = db["profiles"]

app = Flask(__name__)

def remove_id(all_profiles):
    for profile_id in all_profiles:
        del profile_id['_id']
    return all_profiles

@app.route("/company", methods=["GET"])
def get_profiles():
    all_profiles = list(collection.find({}))
    profiles_data = remove_id(all_profiles)
    company_profiles = {"status_code": "200", "message": "successful", "data": profiles_data}
    return Response(json.dumps(company_profiles, indent=4, default=str), mimetype='application/json')



