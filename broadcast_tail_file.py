import asyncio, sys
import logging
from websockets import WebSocketServerProtocol, connect, serve

logging.basicConfig(level=logging.INFO)

local_host="0.0.0.0"

class Server:
    clients = set()

    async def register(self, ws: WebSocketServerProtocol):
        self.clients.add(ws)
        logging.info(f'{ws.remote_address} connects.')

    async def unregister(self, ws: WebSocketServerProtocol):
        self.clients.remove(ws)
        logging.info(f'{ws.remote_address} disconnects.')

    async def send_to_clients(self, message: str) -> None:
        if self.clients:
            await asyncio.wait([asyncio.create_task(client.send(message)) for client in self.clients])

    async def ws_handler(self, ws: WebSocketServerProtocol, uri: str):
        await self.register(ws)
        try:
            await self.distribute(ws)
        finally:
            await self.unregister(ws)

    async def distribute(self, ws: WebSocketServerProtocol):
        async for message in ws:
              await self.send_to_clients(message)

async def feed(p_file: str,  p_port: int):
    await asyncio.sleep(1)
    async with connect(f"ws://{local_host}:{p_port}", ping_interval=None) as ws:
    # for ssl connection
    #async with connect(f"wss://{local_host}:{p_port}", ping_interval=None) as ws:
        with open(p_file, 'r') as f:
          while True:
            #line=f.readline().rstrip('\n')
            line=f.readline()
            if not line:
                await asyncio.sleep(0.2)
            else:
                await ws.send(line)

async def main(p_file: str, p_port: int):
    server = Server()
    res = await asyncio.gather(serve(server.ws_handler, local_host, p_port, ping_interval=None), feed(p_file,  p_port))
    return res

if __name__=="__main__":
    if len(sys.argv) < 3:
        print('Usage: python broadcast_tail_file.py <file_name> <port>')
    else:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main(sys.argv[1], int(sys.argv[2])))
        loop.run_forever()
