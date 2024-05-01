import requests
import os

def get_definition(word):

    api_url = 'https://api.api-ninjas.com/v1/dictionary?word={}'.format(word)
    response = requests.get(api_url, headers={'X-Api-Key': os.environ.get("API_KEY")})
    if response.status_code == requests.codes.ok:
        print(response.json())
        return response.json()
    else:
        print("Error:", response.status_code, response.json())