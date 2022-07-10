from datetime import datetime
from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from app.config import MONGO_CONNECTION, MONGO_USER, MONGO_PASS, MONGO_DB, MONGO_ADMINS_COLLECTION, MONGO_CSRF_COLLECTION, MONGO_SUBSCRIBER_COLLECTION, MONGO_SERVERS_COLLECTION, MONGO_CONNECT_TIMEOUT

mongo_client = MongoClient(MONGO_CONNECTION.format(MONGO_USER, MONGO_PASS), connect=False, connectTimeoutMS=MONGO_CONNECT_TIMEOUT)

col_admins = mongo_client[MONGO_DB][MONGO_ADMINS_COLLECTION]
col_csrf = mongo_client[MONGO_DB][MONGO_CSRF_COLLECTION]
col_subscribers = mongo_client[MONGO_DB][MONGO_SUBSCRIBER_COLLECTION]
col_servers = mongo_client[MONGO_DB][MONGO_SERVERS_COLLECTION]

username = 'administrator'
password = 'temp_password'

col_admins.insert_one({'username': username, 'password': generate_password_hash(password), 'created_at': datetime.now(), 'last_activity': '', 'locked': 'false'})

col_admins.create_index({'username': 1})


col_csrf.create_index({'created_at': 1})
col_csrf.create_index({'csrf_token': 1})


col_subscribers.create_index({'username': 1})
col_subscribers.create_index({'expires_at': 1})


col_servers.create_index({'server': 1})
col_servers.create_index({'server': 1, 'username': 1})

mongo_client.close()
