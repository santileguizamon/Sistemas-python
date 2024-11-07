import requests

HEADERS = {

'x-Master-Key' : '$2a$10$TBHIT0URiuQTffLWJQLlvunqZLmjpYsrRxAKGoL7t/imbvztClSO.'
}


JSONBIN_URL = 'https://api.jsonbin.io/v3/b/671a4696ad19ca34f8bdd532'


"""
Estructura básica de jsonbin
{
  "record": [
    {
      "username": "usuario1",
      "password": "contraseña1"
    },
    {
      "username": "usuario2",
      "password": "contraseña2"
    },
    {
      "username": "usuario3",
      "password": "contraseña3"
    },
    {
      "username": "Gamaliel",
      "password": "1234"
    }
  ]
}
"""


params = {
  'access_key': 'ab4cb3a8be3f01ec3ad753e67407d71f'
}

api_result = requests.get('https://api.aviationstack.com/v1/flights', params)

api_response = api_result.json()




url = 'https://randomuser.me/api/'
headers = {
}

response = requests.get(url, headers=headers)

api_respuesta = response.json()



