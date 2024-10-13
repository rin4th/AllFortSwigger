import requests
import json

def check_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response
    except Exception as e:
        return None
        
def retrieve_json_data():
    path = '/mnt/project/ctf/portSwigger/AllFortSwigger/config/labs.json'
    with open(path, 'r') as file:
        return json.load(file)