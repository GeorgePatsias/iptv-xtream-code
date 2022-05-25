import config
from uuid import uuid4
from modules.Shared.Logger import logger
from datetime import datetime, timedelta
from modules.Shared.MongoClient import mongo_client


class CSRFClass():
    def generate_CSRF(self):
        try:
            csrf_token = str(uuid4())

            col_csrf = mongo_client[config.MONGO_DB][config.MONGO_CSRF_COLLECTION]

            col_csrf.insert_one({'csrf_token': csrf_token, 'created_at': datetime.now()})

            return csrf_token
        except Exception as e:
            logger.exception(e)
            return ''

    def is_valid_csrf(self, csrf):
        try:
            if not csrf:
                return False

            col_csrf = mongo_client[config.MONGO_DB][config.MONGO_CSRF_COLLECTION]

            time_difference = datetime.now() - timedelta(minutes=config.CSRF_TIME_TO_LIVE)

            col_csrf.delete_many({'created_at': {'$lte': time_difference}})

            csrf_exits = col_csrf.find_one({'csrf_token': csrf}, {'_id': 0})

            if csrf_exits:
                col_csrf.delete_one({'csrf_token': csrf})
                return True

            return False
        except Exception as e:
            logger.exception(e)
            return False
