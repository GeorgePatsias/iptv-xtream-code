import config
from modules.Shared.Logger import logger


def valid_api(api_key):
    try:
        if api_key == config.FLASK_API_KEY:
            return True

        logger.info('INVALID APIKEY {}'.format(api_key))
        return False
    except Exception:
        logger.info('INVALID APIKEY {}'.format(api_key))
        return False
