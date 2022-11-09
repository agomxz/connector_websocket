from websocket import create_connection
import json
import requests


#Config
url = "http://204.236.161.174/api/session"
payload='email=admin&password=admin'
headers = {'Content-Type': 'application/x-www-form-urlencoded'}
response = requests.request("POST", url, headers=headers, data=payload)
jsession = ""

if response.status_code == 200:
    print("Connected!")
    print(response.headers)
    cookie = response.headers.get('Set-Cookie')
    jsession = cookie.split(';')[0]
else:
    print("Error while trying to connect")


ws = create_connection("ws://204.236.161.174/api/socket", cookie=jsession)

while True:
    result =  ws.recv()
    print("Received '%s'" % result)

ws.close()

