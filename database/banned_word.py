from pymongo import MongoClient
import json
import os

CONFIG_FILE = 'config.json'

if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, 'r') as f:
        data = json.load(f)
        MONGO_URI = data.get("MONGO_URI", [])
        DB_NAME = data.get("DB_NAME", [])
        COLLECTION_NAME = data.get("DB_COLLECTION_BANNEDS_WORDS", [])
        
else:
    MONGO_URI = []
    DB_NAME = []
    COLLECTION_NAME = []

client = MongoClient(MONGO_URI) 
db = client[DB_NAME]  
banned_words_collection = db[COLLECTION_NAME]  

def add_banned_word(word):
    banned_words_collection.insert_one({'word': word})

def remove_banned_word(word):
    banned_words_collection.delete_one({'word': word})

def get_banned_words():
    return [doc['word'] for doc in banned_words_collection.find()]

def list_banned_words():
    words = collection.find()
    return [word['word'] for word in words]
