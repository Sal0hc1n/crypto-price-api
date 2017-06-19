from datetime import datetime

import requests

def get_datetime():
    return datetime.now().strftime('%Y-%m-%d')

def get_response(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
        return None
    except requests.exceptions.SSLError as err:
        print(err)
        print("Consider upgrading OpenSSL")
        return None
    except requests.exceptions.ReadTimeout as err:
        print(err)
        return None
    except requests.exceptions.ConnectionError as err:
        print(err)
        return None
    return response.json()
