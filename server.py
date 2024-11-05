import asyncio
import websockets

async def echo(websocket, path):
    async for message in websocket:
        print(f"Received message: {message}")
        await websocket.send(f"Echo: {message}")

# WebSocketサーバーを起動
async def main():
    async with websockets.serve(echo, "localhost", 8765):
        print("WebSocket server started at ws://localhost:8765")
        await asyncio.Future()  # 永久に実行するため

asyncio.run(main())
