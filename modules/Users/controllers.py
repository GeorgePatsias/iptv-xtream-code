import config
from flask_login import UserMixin
from modules.Shared.Logger import logger


class User(UserMixin):
    pass


def valid_api(api_key):
    try:
        if api_key == config.FLASK_API_KEY:
            return True

        logger.info('INVALID APIKEY {}'.format(api_key))
        return False
    except Exception:
        logger.info('INVALID APIKEY {}'.format(api_key))
        return False
