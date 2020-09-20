""" Initialization of Server
"""
import asyncio
import signal
from server_class import Server

signal.signal(signal.SIGINT, signal.SIG_DFL)
CLIENT_DICTIONARY = {}

async def handle_echo(reader, writer):
    """ Server-client connections are handled in this function"""
    addr = writer.get_extra_info('peername')
    message = f"{addr} is connected !!!!"
    CLIENT_DICTIONARY[addr[1]] = Server()
    print(message)
    while True:
        data = await reader.read(10000)
        message = data.decode().strip()
        if message == 'quit':
            CLIENT_DICTIONARY[addr[1]].removelog()
            break
        print(f"Received {message} from {addr}")
        reply = CLIENT_DICTIONARY[addr[1]].split(message)
        print(f"Send: {reply}")
        #hello = 'successful'
        if reply != '' or reply != 'None':
            writer.write(reply.encode())
        else:
            reply = '.'
            writer.write(reply.encode())
        await writer.drain()
    print("Close the connection")
    writer.close()

async def main():
    """
    In this function the main program will starts execution
    """
    server_ip = '127.0.0.1'
    port = 8080
    logfile = open('loginlog.txt', 'w')
    logfile.close()
    server = await asyncio.start_server(
        handle_echo, server_ip, port)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()

asyncio.run(main())
