from uuid import uuid4
from modules.Shared.Logger import logger
from datetime import datetime, timedelta
from modules.Shared.MongoClient import mongoClient
from config import MONGO_DB, MONGO_CSRF_COLLECTION, CSRF_TIME_TO_LIVE


class CSRFClass():
    def generate_CSRF(self):
        try:
            csrf_token = str(uuid4())

            mongo_client = mongoClient()
            col_csrf = mongo_client[MONGO_DB][MONGO_CSRF_COLLECTION]

            col_csrf.insert_one({'csrf_token': csrf_token, 'created_at': datetime.now()})
            mongo_client.close()

            return csrf_token
        except Exception as e:
            logger.exception(e)
            return ''

    def is_valid_csrf(self, csrf):
        try:
            if not csrf:
                return False

            mongo_client = mongoClient()
            col_csrf = mongo_client[MONGO_DB][MONGO_CSRF_COLLECTION]

            time_difference = datetime.now() - timedelta(minutes=CSRF_TIME_TO_LIVE)

            col_csrf.delete_many({'created_at': {'$lte': time_difference}})

            csrf_exists = col_csrf.find_one({'csrf_token': csrf}, {'_id': 0})

            if csrf_exists:
                col_csrf.delete_one({'csrf_token': csrf})
                mongo_client.close()
                return True

            mongo_client.close()

            return False
        except Exception as e:
            logger.exception(e)
            return False
