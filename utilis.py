
import requests

def get_people_in_space():
    response = requests.get('http://api.open-notify.org/astros.json')
    data = response.json()
    return data.get("people", [])