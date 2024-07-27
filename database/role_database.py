from pymongo import MongoClient
import json
import os

CONFIG_FILE = 'config.json'

if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, 'r') as f:
        data = json.load(f)
        MONGO_URI = data.get("MONGO_URI", [])
        DB_NAME = data.get("DB_NAME", [])
        COLLECTION_NAME = data.get("DB_COLLECTION_ROLES", [])
        
else:
    MONGO_URI = []
    DB_NAME = []
    COLLECTION_NAME = []

def connect_db():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    return db[COLLECTION_NAME]

def fetch_roles():
    roles_collection = connect_db()
    roles_data = roles_collection.find()

    admin_roles = []
    warning_only_roles = []
    muted_role = None

    for role in roles_data:
        role_name = role.get('role_type') 
        role_id = role.get('role_id')

        if role_name == "admin":
            admin_roles.append(role_id)
        elif role_name == "warning only":
            warning_only_roles.append(role_id)
        elif role_name == "mute":
            muted_role = role_id

    return admin_roles, warning_only_roles, muted_role



def add_role(role_name, role_id, role_real_name):
    roles_collection = connect_db()
    role_data = {
        'role_type': role_name,
        'role_id': str(role_id),
        'role_name': role_real_name
    }
    roles_collection.insert_one(role_data)

def remove_role(role_id):
    roles_collection = connect_db()
    result = roles_collection.delete_one({'role_id': str(role_id)})
    if result.deleted_count > 0:
        print(f"Role with ID {role_id} removed from the database.")
        return True
    else:
        print(f"No role with ID {role_id} found in the database.")
        return False
    
def list_roles():
    roles_collection = connect_db()
    roles = roles_collection.find()
    role_list = []
    for role in roles:
        role_name = role.get('role_name', 'Unknown') 
        role_id = role.get('role_id', 'Unknown')
        role_type = role.get('role_type', 'Unknown')
        role_list.append(f"Name: {role_name}, ID: {role_id}, Type: {role_type}")
    return role_list
