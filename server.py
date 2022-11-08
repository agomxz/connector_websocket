import websockets
import asyncio
import time
from websocket import create_connection
import json
import requests

PORT = 8000

print("Server listening on Port " + str(PORT))

async def echo(websocket, path):
    print("A client just connected")
    try:
        async for message in websocket:




            #Config
            url = "http://204.236.161.174/api/session"
            payload='email=admin&password=admin'
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            response = requests.request("POST", url, headers=headers, data=payload)
            jsession = ""

            if response.status_code == 200:
                print("Connected!")
                data = json.loads(response.text)
                print(response.headers.get('Set-Cookie'))
                cookie = response.headers.get('Set-Cookie')
                jsession = cookie.split(';')[0]
            else:
                print("Error while trying to connect")

            ws = create_connection("ws://204.236.161.174/api/socket", cookie=jsession)

            while True:
                result =  ws.recv()
                await websocket.send(result)
                time.sleep(1)
                await websocket.send("******")


            print("Received message from client: " + message)
            await websocket.send("Pong: " + message)


    except websockets.exceptions.ConnectionClosed as e:
        print("A client just disconnected")

start_server = websockets.serve(echo, "localhost", PORT)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()