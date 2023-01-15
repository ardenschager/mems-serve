
import os
import asyncio
import json
import websockets

import text2emotion as te

responses = []

async def handle_websocket(websocket, path):
    try:
        # sync server game state to newly connected game client
        print('connected to: ' + str(websocket.id))
        await websocket.send(json.dumps(responses))
        # route and handle messages for duration of websocket connection
        async for message in websocket:
            if len(message) != 0:
                response = {
                    "input": message,
                    "scores": te.get_emotion(message)
                }
                responses.append(response)
                response = json.dumps(response)
                print("response: " + str(response))
                websocket.send(await websocket.send(response))
    finally:
        # upon websocket disconnect remove client's player
        print("disconnected")

async def main():
    port = 8080
    print("listening on: " + str(port))
    async with websockets.serve(
		handle_websocket,
		host="", 
		port=port,
        # host="0.0.0.0",
        # port=8000
	):
        await asyncio.Future()

asyncio.run(main())