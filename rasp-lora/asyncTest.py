import asyncio

import time

async def say_after(delay, what):

    await asyncio.sleep(delay)

    print(what)


async def main():

    task1 = asyncio.create_task(

        say_after(1, 'hello'))



    task2 = asyncio.create_task(

        say_after(20, 'world'))



    task3 = asyncio.create_task(

        say_after(4, 'more'))

    task4 = asyncio.create_task(

        say_after(6, 'words'))



    print(f"started at {time.strftime('%X')}")

    await task1

    await task2

    await task3

    await task4

    print(f"finished at {time.strftime('%X')}")

asyncio.run(main())