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
        COLLECTION_NAME = data.get("DB_COLLECTION_COMMANDS_HISTORY", [])
        
else:
    MONGO_URI = []
    DB_NAME = []
    COLLECTION_NAME = []

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
commands_collection = db[COLLECTION_NAME]

def log_command_history(user_id, username, command_name):
    log_entry = {
        'user_id': user_id,
        'username': username,
        'command': command_name,
        'date': datetime.now().isoformat()  
    }
    commands_collection.insert_one(log_entry)
