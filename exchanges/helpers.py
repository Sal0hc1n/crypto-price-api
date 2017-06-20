from datetime import datetime

import requests
import logging

def get_datetime():
    return datetime.now().strftime('%Y-%m-%d')

def get_response(url, logger = None):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        if logger is not logging.getLoggerClass():
            print(err)
        else:
            logger.error(err)
        return None
    except requests.exceptions.SSLError as err:
        if logger is not logging.getLoggerClass():
            print(err)
            print("Consider upgrading OpenSSL")
        else:
            logger.error(err)
            logger.error("Consider upgrading OpenSSL")
        return None
    except requests.exceptions.ReadTimeout as err:
        if logger is not logging.getLoggerClass():
            print(err)
        else:
            logger.error(err)
        return None
    except requests.exceptions.ConnectionError as err:
        if logger is not logging.getLoggerClass():
            print(err)
        else:
            logger.error(err)
        return None
    return response.json()
