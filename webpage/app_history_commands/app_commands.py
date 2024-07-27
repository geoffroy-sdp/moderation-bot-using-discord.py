from flask import Flask, jsonify, render_template, Blueprint
from pymongo import MongoClient
import os
import json

app = Flask(__name__)

CONFIG_FILE = 'config.json'

if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, 'r') as f:
        data = json.load(f)
        MONGO_URI = data.get("MONGO_URI", [])
        DB_NAME = data.get("DB_NAME", [])
        DB_COLLECTION = data.get("DB_COLLECTION_COMMANDS_HISTORY", [])
else :
    MONGO_URI = []
    DB_NAME = []
    DB_COLLECTION = []

# Connexion à MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
commands_collection = db[DB_COLLECTION]

commands_bp = Blueprint('commands', __name__, template_folder='templates')

@commands_bp.route('/')
def history_commands():
    return render_template('history_commands.html')

@commands_bp.route('/api/command_history', methods=['GET'])
def command_history():
    try:
        commands_data = list(commands_collection.find({}, {'_id': 0}))
        if not commands_data:
            return jsonify([])  
        return jsonify(commands_data)
    except Exception as e:
        print(f"Error fetching command history: {e}")
        return jsonify({"error": "Internal Server Error"}), 500



@commands_bp.route('/api/reset_command_history', methods=['POST'])
def reset_command_history():
    commands_collection.delete_many({}) 
    return '', 200

app.register_blueprint(commands_bp, url_prefix='/commands')

if __name__ == '__main__':
    create_tables() 
    app.run(debug=True, port=5500)
