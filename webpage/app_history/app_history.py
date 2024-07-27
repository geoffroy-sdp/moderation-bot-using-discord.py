from flask import Flask, Blueprint, jsonify, render_template
from pymongo import MongoClient
from database.database import reset_sanction_points
import os
import json

history_bp = Blueprint('history', __name__, template_folder='templates')

CONFIG_FILE = 'config.json'

if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, 'r') as f:
        data = json.load(f)
        MONGO_URI = data.get("MONGO_URI", [])
        DB_NAME = data.get("DB_NAME", [])
        DB_COLLECTION = data.get("DB_COLLECTION_USER_SANCTIONS", [])
else :
    MONGO_URI = []
    DB_NAME = []
    DB_COLLECTION = []
        

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[DB_COLLECTION]
        
@history_bp.route('/')
def history_index():
    return render_template('history.html')

@history_bp.route('/api/sanctions', methods=['GET'])
def get_sanctions():
    try:
        
        sanctions_data = collection.find()
        sanctions_list = []
        
        for sanction in sanctions_data:
            sanctions_list.append({
                'user_id': str(sanction.get('user_id', '')),
                'username': sanction.get('username', ''),
                'sanction_points': sanction.get('sanction_points', 0),
                'last_updated': sanction.get('last_updated', ''),
                'status': sanction.get('status', '')
            })
        
        return jsonify(sanctions_list)
    except Exception as e:
        print(f"An error occurred: {e}")  # Log the error
        return jsonify({"error": str(e)}), 500

@history_bp.route('/api/reset_sanctions', methods=['POST'])
def reset_sanctions():
    try:
        
        reset_sanction_points()
        print('all sanctions points have been deleted')
        
        return jsonify({"message": "All sanctions have been reset."}), 200
    except Exception as e:
        print(f"An error occurred while resetting sanctions: {e}")  # Log the error
        return jsonify({"error": str(e)}), 500
