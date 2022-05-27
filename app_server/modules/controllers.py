from flask import escape
from datetime import datetime
from modules.Logger import logger
from modules.MongoClient import mongoClient
from config import MONGO_DB, MONGO_SUBSCRIBER_COLLECTION, MONGO_SERVERS_COLLECTION


def valid_subscriber(username='', password=''):
    try:
        username = escape(username)
        password = escape(password)

        mongo_client = mongoClient()
        col_subscribers = mongo_client[MONGO_DB][MONGO_SUBSCRIBER_COLLECTION]

        subsriber_server = col_subscribers.find_one({
            'username': username,
            'password': password,
            'locked': 'false',
            'expires_at': {
                '$gte': datetime.now()
            }
        }, {
            '_id': 0, 'server': 1
        })

        if not subsriber_server:
            logger.info('INVALID/EXPIRED USER {}:{}'.format(username, password))
            mongo_client.close()
            return None, None, None

        col_servers = mongo_client[MONGO_DB][MONGO_SERVERS_COLLECTION]

        server_data = col_servers.find_one({'server': subsriber_server['server']}, {'_id': 0, 'username': 1, 'password': 1})
        mongo_client.close()

        if not server_data:
            return None, None, None

        return subsriber_server['server'], server_data['username'], server_data['password']

    except Exception as e:
        logger.exception(e)
        return None, None, None
