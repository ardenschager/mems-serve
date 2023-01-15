
import os
import asyncio
import json
import websockets
import random
import text2emotion as te

initial_data = [
    "Don sucks",
    "What am I supposed to say here, and who is going to hear?",
    "The wintertime is killing my garden and it's bumming me out",
    "Woah hey, I can't believe she did that to me",
    "My sister hates lobster rolls",
    "Nothing lifts my spirits like a bath bomb",
]

responses = []

for datum in initial_data:
    response = {
        "message": datum,
        "scores": te.get_emotion(datum)
    }
    responses.append(response)


async def handle_websocket(websocket, path):
    try:
        # sync server game state to newly connected game client
        print('connected to: ' + str(websocket.id))
        random.shuffle(responses)
        await websocket.send(json.dumps({'isInit': True, 'memories': responses}))
        # route and handle messages for duration of websocket connection
        async for message in websocket:
            if len(message) != 0:
                response = {
                    "message": message,
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
    try: 
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
    finally: 
        print("server error?")

asyncio.run(main())