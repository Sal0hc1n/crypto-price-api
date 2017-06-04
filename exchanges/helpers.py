from datetime import datetime

import requests

def get_datetime():
    return datetime.now().strftime('%Y-%m-%d')

def get_response(url):
    response = requests.get(url)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
        return None
    return response.json()
