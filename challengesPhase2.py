import asyncio
import time


# async def download_file(name, delay):
#     try:
#         print(f"⬇️  Downloading {name}...")
#         await asyncio.sleep(delay)
#         print(f"✅ Download successful: {name}")
#         return name
#     except asyncio.CancelledError:
#         print(f"❌ Download cancelled: {name}")
#         raise

# async def main():
#     # Create tasks explicitly so we can cancel them
#     task1 = asyncio.create_task(download_file("name.pdf", 2))
#     task2 = asyncio.create_task(download_file("OpenCv.pdf", 4))
#     task3 = asyncio.create_task(download_file("docker.pdf", 3))
#     task4 = asyncio.create_task(download_file("Resume.pdf", 5))

#     await asyncio.sleep(1) #Let them start
#     print(f"⚠️ Cancelling docker.pdf...")
#     task3.cancel()  # Cancel one download

#     # Gather results, handling cancellation
#     try:
#         results = await asyncio.gather(
#             task1,
#             task2,
#             task3,
#             task4,
#             return_exceptions=True
#         )
#         print("All tasks finished.")
#         print(f"Results:{results}")
#     except Exception as e:
#         print("Error:", e)

# if __name__ == "__main__":
#     asyncio.run(main())

#@ 🔑 Key Points Learned
# asyncio.create_task → lets you control each task individually.
# task.cancel() → sends a cancellation request.
# CancelledError must be caught inside the coroutine if you want to handle cleanup.
# asyncio.gather(..., return_exceptions=True) → prevents other tasks from being killed by one cancelled/failed task.

# ##* Challenge two
# async def main_wait():
#     tasks = [asyncio.create_task(download_file("name.pdf", 2)),
#              asyncio.create_task(download_file("OpenCv.pdf", 4)),
#              asyncio.create_task(download_file("docker.pdf", 3)),
#              asyncio.create_task(download_file("Resume.pdf", 5))
#     ]

#     done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
#     print(f"First task finished: {done}")

# if __name__ == "__main__":
#     asyncio.run(main_wait())



# #* Challenge three
# print("==========Challenge three============")
# async def do_task(delay, task):
#     try:
#         await asyncio.sleep(delay)
#         print(f"task {task} done")
#         return delay, task
#     except asyncio.CancelledError:
#         print(f"task {task} was cancelled!")
#         raise

# async def main():
#     async with asyncio.TaskGroup() as tg:
#         t1=tg.create_task(do_task(2, "Task1"))
#         t2=tg.create_task(do_task(3, "Task2"))
#         t3=tg.create_task(do_task(5, "Task3"))


#         # Cancel Task2 after 1 second, but keep others running
#         await asyncio.sleep(1)
#         t2.cancel()

#     print("All tasks completed!")


# if __name__ == "__main__":
#     asyncio.run(main())

# ==============================================
#* challenge three
async def do_task(delay, task, should_fail=False):
    print(f"Task {task}: Starting...")
    await asyncio.sleep(delay)

    if should_fail:
        print(f"Task {task}: Intentionally failing!")
        raise ValueError(f"Error in {task}")
    print(f"Task {task}: completed successfully.")

async def main():
    try:
        async with asyncio.TaskGroup() as tg:
            # Create a task that will fail
            tg.create_task(do_task("Alpha", 2, should_fail=True))
            # Create tasks that would otherwise succeed
            tg.create_task(do_task("Beta", 2))
            tg.create_task(do_task("Gamma", 3))
    except ExceptionGroup as eg:
        print(f"\nCaught an ExceptionGroup: {eg.exceptions}")
        for exc in eg.exceptions:
            print(f" - {type(exc).__name__}: {exc}")
    except Exception as e:
        print(f"\nCaught a general exception: {e}")

if __name__=="__main__":
    asyncio.run(main())