import config
from modules.Shared.Logger import logger
from modules.Shared.MongoClient import mongo_client


def valid_user(username='', password=''):
    try:
        col_users = mongo_client[config.MONGO_DB][config.MONGO_USERS_COLLECTION]
        if col_users.find_one({"user_info.username": username, "user_info.password": password}):

            return True

        logger.info('INVALID/EXPIRED USER {}:{}'.format(username, password))
        return False

    except Exception:

        logger.info('INVALID/EXPIRED USER {}:{}'.format(username, password))
        return False
