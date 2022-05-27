from pymongo import MongoClient
from modules.Shared.Logger import logger
from config import MONGO_CONNECTION, MONGO_USER, MONGO_PASS


def mongoClient():
    try:
        return MongoClient(MONGO_CONNECTION.format(MONGO_USER, MONGO_PASS), connect=False, connectTimeoutMS=5000)

    except Exception as e:
        logger.exception(e)
        return None
