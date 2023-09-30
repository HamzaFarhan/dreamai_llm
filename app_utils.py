from imports import *

async def long_running_task(input: str):
    print(f"\nGot input: {input}\n")
    await asyncio.sleep(10)
    return "Task Done"
