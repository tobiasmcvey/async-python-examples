# tasks-intro.py

import trio

async def child1():
    print(f"  child1: started! sleeping now...")
    await trio.sleep(1)
    print(f"  child1: exiting!")

async def child2():
    print(f"  child2: started! sleeping now...")
    await trio.sleep(1)
    print(f"  child2: exiting!")

async def parent():
    print(f"parent: started!")
    async with trio.open_nursery() as nursery:
        print(f"parent: spawning child1...")
        nursery.start_soon(child1)

        print(f"parent: spawning child2...")
        nursery.start_soon(child2)

        print(f"parent: waiting for children to finish...")
        # -- we exit the nursery block here --
    print(f"parent: all done!")

trio.run(parent)
