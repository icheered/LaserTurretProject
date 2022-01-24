import asyncio


async def funcA():
    i = 0
    a = 0
    for i in range(1000):
        a += i ** 3
        print("a")
        await asyncio.sleep(0.1)


async def funcB():
    for i in range(1000):
        print("11111")
        await asyncio.sleep(0.1)


asyncio.run(funcA())
asyncio.run(funcB())

print("Done")
