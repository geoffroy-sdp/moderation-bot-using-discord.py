from flask import Blueprint, jsonify, render_template, request
from pymongo import MongoClient
import os
import json

CONFIG_FILE = 'config.json'

if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, 'r') as f:
        data = json.load(f)
        MONGO_URI = data.get("MONGO_URI", [])
        DB_NAME = data.get("DB_NAME", [])
        DB_COLLECTION = data.get("DB_COLLECTION_ROLES", [])
else :
    MONGO_URI = []
    DB_NAME = []
    DB_COLLECTION = []

roles_bp = Blueprint('roles', __name__, template_folder='templates')

def connect_db():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    return db[DB_COLLECTION]

@roles_bp.route('/')
def roles():
    return render_template('roles.html')

@roles_bp.route('/api/roles', methods=['GET'])
def get_roles():
    roles_collection = connect_db()
    roles_data = list(roles_collection.find({}, {'_id': 0}))  # Exclure le champ _id
    return jsonify(roles_data)