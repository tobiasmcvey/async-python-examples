# tasks-intro.py

import trio

class Tracer(trio.abc.Instrument):
    def before_run(self):
        print("!!! run started")

    def _print_with_task(self, msg, task):
        # repr(task) is perhaps more useful than task.name in general,
        # but in context of a tutorial the extra noise is unhelpful.
        print(f"{msg}: {task.name}")

    def task_spawned(self, task):
        self._print_with_task("### new task spawned", task)

    def task_scheduled(self, task):
        self._print_with_task("### task scheduled", task)

    def before_task_step(self, task):
        self._print_with_task(">>> about to run one step of task", task)

    def after_task_step(self, task):
        self._print_with_task("<<< task step finished", task)

    def task_exited(self, task):
        self._print_with_task("### task exited", task)

    def before_io_wait(self, timeout):
        if timeout:
            print(f"### waiting for I/O for up to {timeout} seconds")
        else:
            print("### doing a quick check for I/O")
        self._sleep_time = trio.current_time()

    def after_io_wait(self, timeout):
        duration = trio.current_time() - self._sleep_time
        print(f"### finished I/O check (took {duration} seconds)")

    def after_run(self):
        print("!!! run finished")


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

trio.run(parent, instruments=[Tracer()])
