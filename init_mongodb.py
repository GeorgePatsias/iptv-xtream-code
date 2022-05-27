from pymongo import MongoClient
from datetime import datetime
from werkzeug.security import generate_password_hash
from config import MONGO_CONNECTION, MONGO_USER, MONGO_PASS, MONGO_DB, MONGO_ADMINS_COLLECTION

mongo_client = MongoClient(MONGO_CONNECTION.format(MONGO_USER, MONGO_PASS), connect=False, connectTimeoutMS=5000)

col_admins = mongo_client[MONGO_DB][MONGO_ADMINS_COLLECTION]


username = 'administrator'
password = 'Password1!'
col_admins.insert_one({'username': 'administrator', 'password': generate_password_hash(password), 'created_at': datetime.now(), 'last_activity': '', 'locked': 'false'})