import asyncio

async def count():
    print("One")
    await asyncio.sleep(1)
    print("Two")
    await asyncio.sleep(1)
    print("eeee")

async def count2():
    print("Three")
    await asyncio.sleep(1)
    print("Four")

async def count3():
    print("Five")
    await asyncio.sleep(1)
    print("Six")
    await asyncio.sleep(1)
    print("eeeeu6ryfhm")

async def main():
    await asyncio.gather(count(), count2(), count3())

if __name__ == "__main__":
    import time
    s = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")