from pymongo import MongoClient
from modules.Shared.Logger import logger
from config import MONGO_CONNECTION, MONGO_USER, MONGO_PASS, MONGO_CONNECT_TIMEOUT


def mongoClient():
    try:
        return MongoClient(MONGO_CONNECTION.format(MONGO_USER, MONGO_PASS), connect=False, connectTimeoutMS=MONGO_CONNECT_TIMEOUT)

    except Exception as e:
        logger.exception(e)
        return None
