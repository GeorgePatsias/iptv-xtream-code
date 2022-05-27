from flask import escape
from modules.Shared.Logger import logger
from werkzeug.security import check_password_hash
from modules.Shared.MongoClient import mongoClient
from config import MONGO_DB, MONGO_ADMINS_COLLECTION


def valid_user(username, password):
    try:
        if not username or not password:
            return False

        mongo_client = mongoClient()
        col_admins = mongo_client[MONGO_DB][MONGO_ADMINS_COLLECTION]

        admin_data = col_admins.find_one({'username': escape(username)}, {'_id': 0, 'password': 1})
        mongo_client.close()
        if not admin_data:
            return False

        if check_password_hash(admin_data.get('password'), escape(password)):
            return True

        return False

    except Exception as e:
        logger.exception(e)
        return False
