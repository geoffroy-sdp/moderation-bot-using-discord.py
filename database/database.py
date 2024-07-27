from pymongo import MongoClient
from datetime import datetime
import json
import os

CONFIG_FILE = 'config.json'

if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, 'r') as f:
        data = json.load(f)
        MONGO_URI = data.get("MONGO_URI", [])
        DB_NAME = data.get("DB_NAME", [])
        COLLECTION_NAME = data.get("DB_COLLECTION_USER_SANCTIONS", [])
        
else:
    MONGO_URI = []
    DB_NAME = []
    COLLECTION_NAME = []

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
user_sanctions_collection = db[COLLECTION_NAME]


def connect_db():
    """ Connect to the MongoDB database. """
    return db['history']


def update_sanction_points(user_id, username, points, is_admin=False, is_warning_only=False):
    if username is None or username.strip() == "":
        username = "Unknown"  # Default value if username is empty

    # Create the base update document
    update_doc = {
        '$set': {
            'username': username,
            'last_updated': datetime.now()
        }
    }

    if is_admin:
        update_doc['$set']['status'] = 'admin'
    elif is_warning_only:
        update_doc['$inc'] = {'sanctions_points' : points}
        update_doc['$set']['status'] = 'distro/helper'
    else:
        update_doc['$inc'] = {'sanctions_points': points}
        update_doc['$unset'] = {'status': ""} 

    user_sanctions_collection.update_one(
        {'user_id': user_id},
        update_doc,
        upsert=True  # Create a new document if none exists
    )


def get_sanction_points(user_id):
    user_data = user_sanctions_collection.find_one({'user_id': user_id})
    
    if user_data:
        return user_data.get('sanctions_points', 0)
    return 0


def reset_sanction_points():
    user_sanctions_collection.update_many({}, {'$set': {'sanctions_points': 0, 'last_updated': datetime.now()}})
    print("All sanction points have been reset.")


def reset_sanction_data():
    user_sanctions_collection.delete_many({})
    print("All data in the user_sanctions collection has been deleted.")


def reset_sanction_points_member(user_id):
    user_sanctions_collection.update_one(
        {'user_id': user_id},
        {'$set': {'sanction_points': 0, 'last_updated': datetime.now()}}
    )
    print(f"Sanction points for user_id {user_id} have been reset.")
