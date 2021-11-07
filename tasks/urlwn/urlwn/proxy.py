import asyncio
import sys
from asyncio import subprocess
from collections import OrderedDict
from typing import Optional

cmd = [
    'bwrap',
    '--ro-bind', './srv', '/bin/srv',
    '--ro-bind', './index.resp', '/index',
    '--ro-bind', './passwd.resp', '/etc/passwd',
    '--ro-bind', './flag.resp', '/home/kettle/flag',
    '/bin/srv'
]


class LRUDict(OrderedDict):
    def __init__(self, size: int):
        self.size = size

    def get(self, key: str) -> Optional[tuple[subprocess.Process, int]]:
        if not key in self:
            return None
        self.move_to_end(key)
        return self[key]

    def put(self, key: str, value: tuple[subprocess.Process, int]):
        if key in self:
            self[key][0].kill()
            free_ports.put_nowait(self[key][1])
            self.move_to_end(key)
        self[key] = value
        if len(self) > self.size:
            _, deleted = self.popitem(last=False)
            deleted[0].kill()
            free_ports.put_nowait(deleted[1])


free_ports = asyncio.Queue(1100)
for port in range(60000, 61000):
    free_ports.put_nowait(port)
processes = LRUDict(1000)


def extract_path(line: bytes) -> tuple[str, bytes]:
    req = line.decode().strip().split()
    if len(req) != 3:
        raise ValueError
    path = req[1].split('/')
    if len(path) < 2 or path[0] != '':
        raise ValueError
    req[1] = '/' + '/'.join(path[2:])
    return path[1], ' '.join(req).encode() + b'\r\n'


async def send_bad_request(writer: asyncio.StreamWriter):
    resp = 'HTTP/1.1 400 Bad Request\r\n'
    writer.write(resp.encode())
    await writer.drain()
    writer.close()
    await writer.wait_closed()


async def start_new_process(key: str) -> tuple[subprocess.Process, int]:
    loop = asyncio.get_event_loop()
    port = await free_ports.get()
    process = await subprocess.create_subprocess_exec(*cmd, str(port))
    processes.put(key, (process, port))

    async def clean():
        await process.wait()
        await free_ports.put(port)
        del processes[key]

    loop.create_task(clean())
    await asyncio.sleep(0.1)
    return (process, port)


async def communicate(port: int, req: bytes) -> bytes:
    try:
        reader, writer = await asyncio.open_connection('127.0.0.1', port)
        writer.write(req)
        await writer.drain()
        resp = await reader.read()
        writer.close()
        await writer.wait_closed()
        return resp
    except (ConnectionRefusedError, ConnectionAbortedError,
            ConnectionResetError):
        return b'HTTP/1.1 521 Web Server Is Down\r\n'


async def read_all(reader: asyncio.StreamReader) -> bytes:
    res = b''
    line = await reader.readline()
    while len(line.strip()):
        res += line
        line = await reader.readline()
    res += line
    return res


async def handle(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    req = await reader.readline()
    try:
        path, req = extract_path(req)
    except ValueError:
        await send_bad_request(writer)
        return
    val = processes.get(path)
    if val is None:
        _, port = await start_new_process(path)
    else:
        _, port = val
    req += await read_all(reader)
    resp = await communicate(port, req)
    writer.write(resp)
    await writer.drain()
    writer.close()
    await writer.wait_closed()


async def main(sock: Optional[str] = None):
    if sock:
        srv = await asyncio.start_unix_server(handle, sock)
    else:
        srv = await asyncio.start_server(handle, '0.0.0.0', 3333)
    async with srv:
        await srv.serve_forever()


if __name__ == '__main__':
    asyncio.run(main(sys.argv[1] if len(sys.argv) > 1 else None))
