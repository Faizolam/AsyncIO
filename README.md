# complete guide to AsyncIO in Python
A **complete guide to AsyncIO in Python**, let’s first structure the full set of topics you should learn. I’ll list them from **fundamentals → intermediate → advanced → real-world usage → testing & best practices**.

Here’s the **AsyncIO Roadmap (all topics):**

---

## 1. **Introduction & Basics**

* What is AsyncIO? (event loop, cooperative multitasking)
* Synchronous vs Multithreading vs Multiprocessing vs AsyncIO
* The Event Loop explained
* Coroutines (`async def`, `await`)
* Running coroutines (`asyncio.run`, `await`, `loop.run_until_complete`)
* Hello World example in AsyncIO

---

## 2. **Tasks & Futures**

* What is a Task? (`asyncio.create_task`)
* What is a Future?
* Converting coroutines into tasks
* Cancelling tasks (`task.cancel`)
* Gathering tasks (`asyncio.gather`, `asyncio.wait`)
* Shielding tasks (`asyncio.shield`)
* Task groups (`asyncio.TaskGroup` in Python 3.11+)

---

## 3. **Asynchronous I/O**

* Async I/O operations with files, sockets, and subprocesses
* `asyncio.sleep` (non-blocking wait)
* Networking basics with `asyncio`
* Subprocesses (`asyncio.create_subprocess_exec`)
* Async file handling (`aiofiles` library)

---

## 4. **Synchronization Primitives**

* `asyncio.Lock`
* `asyncio.Semaphore`
* `asyncio.Event`
* `asyncio.Condition`
* Producer-consumer problem in AsyncIO

---

## 5. **Queues**

* `asyncio.Queue` basics
* Producer-Consumer pattern with queues
* Priority queues (`asyncio.PriorityQueue`)
* Lifo queues (`asyncio.LifoQueue`)

---

## 6. **Timeouts & Cancellations**

* Cancelling tasks (`task.cancel`)
* Handling cancellations safely (`asyncio.CancelledError`)
* Timeouts with `asyncio.wait_for`
* Timeout handling patterns

---

## 7. **AsyncIO Streams**

* TCP server and client (`asyncio.start_server`, `asyncio.open_connection`)
* UDP communication (`asyncio.DatagramProtocol`)
* Reading/writing with streams (`StreamReader`, `StreamWriter`)
* Building chat server/client with streams

---

## 8. **AsyncIO + Context Managers & Iterators**

* Asynchronous context managers (`async with`)
* Asynchronous iterators (`async for`)
* Custom async iterators and context managers
* Using `asyncio.StreamReader` with `async for`

---

## 9. **Advanced Event Loop Features**

* Low-level APIs (`loop.call_soon`, `loop.call_later`)
* Running blocking code in executor (`loop.run_in_executor`, `concurrent.futures`)
* Thread-safe calls (`loop.call_soon_threadsafe`)
* Signals and event loop integration
* Policies and custom event loops

---

## 10. **Error Handling & Debugging**

* Exception handling in coroutines
* Handling task errors
* Debugging event loop (`asyncio.get_running_loop().set_debug(True)`)
* Common pitfalls (blocking calls, forgetting `await`, etc.)

---

## 11. **AsyncIO with External Libraries**

* `aiohttp` (async HTTP client & server)
* `aiomysql`, `asyncpg` (async databases)
* `aioredis` (Redis with asyncio)
* Async ORM frameworks (Tortoise ORM, SQLAlchemy async support)
* Async testing with `pytest-asyncio`

---

## 12. **Testing Async Code**

* Unit testing async functions
* Using `pytest-asyncio`
* Mocking async functions
* Integration testing async applications

---

## 13. **Performance & Optimization**

* Avoiding blocking calls
* Using `asyncio.to_thread` for sync code
* Concurrency vs Parallelism in AsyncIO
* Performance comparison (threads vs async)
* Scaling AsyncIO applications

---

## 14. **Real-World Use Cases**

* Async web scraping with `aiohttp`
* Async chat server
* Async background workers
* Async API service
* Combining AsyncIO with FastAPI, Django, etc.

---

## 15. **Best Practices**

* Structuring async code
* Graceful shutdown of async apps
* Proper resource cleanup
* Avoiding deadlocks & race conditions
* When NOT to use AsyncIO
* AsyncIO vs Trio vs Curio vs AnyIO (comparison)

---

✅ This covers **everything from basics → advanced → real-world usage**.
If you master all of these, you’ll be in the **top 5% of Python developers with AsyncIO expertise**.

---


Perfect 👍 Let’s start **Phase 1: Core Basics of AsyncIO**.
I’ll go **slowly, in detail, with real-world analogies, explanations, code examples, and challenges**.
We won’t skip anything in this phase.

---

# 📌 Phase 1: Core Basics of AsyncIO

### Topics in this phase:

1. What is AsyncIO? (concept & analogy)
2. Synchronous vs Multithreading vs Multiprocessing vs AsyncIO
3. The Event Loop explained
4. Coroutines (`async def`, `await`)
5. Running coroutines (`asyncio.run`, `await`, `loop.run_until_complete`)
6. Hello World example in AsyncIO

---

## 1. **What is AsyncIO?**

* **Definition:**
  AsyncIO is a Python library that lets you write **asynchronous programs**. Instead of waiting for one task to finish before starting another, it lets tasks **cooperate** and run "seemingly at the same time" using a single thread.

* **Analogy (Real World):**
  Imagine you’re a **chef in a kitchen**.

  * In synchronous code, you cook one dish fully → then start the next → then the next.
  * If a dish needs to **boil for 10 minutes**, you just **stand and wait**. Waste of time.
  * In asynchronous code, while one dish is boiling, you can chop vegetables, knead dough, or check the oven. You **don’t block yourself**—you multitask efficiently.

So AsyncIO = being a smart chef who keeps busy during waiting times.

---

## 2. **Synchronous vs Multithreading vs Multiprocessing vs AsyncIO**

Let’s break it down:

### 🔹 Synchronous (Normal Python)

* Code runs **line by line**.
* If one function is waiting (e.g., for a file read or network call), everything else is stuck.
* Like a single cashier in a store handling one customer at a time.

### 🔹 Multithreading

* Multiple **threads** share the same memory and run in parallel.
* Useful when tasks spend time waiting (like network requests).
* But threads can cause issues (race conditions, deadlocks).
* Like multiple cashiers in the same store, but they can bump into each other when handling the same cash drawer.

### 🔹 Multiprocessing

* Runs on multiple CPUs → true parallelism.
* Best for **CPU-heavy tasks** (like image processing, ML training).
* But expensive (more memory, process communication overhead).
* Like having multiple stores, each with its own cashier and cash drawer.

### 🔹 AsyncIO

* Single-threaded, single-process.
* Uses an **event loop** to switch between tasks when they’re waiting.
* Best for **I/O-heavy tasks** (API calls, database queries, file operations).
* Like a single super-efficient cashier who asks a customer to “step aside while waiting for change” and serves the next customer.

---

## 3. **The Event Loop Explained**

* The **event loop** is the heart of AsyncIO.
* Think of it as a **manager** that decides:

  > "Which coroutine should I run now? Who is waiting? Who is ready?"

**How it works:**

1. You give tasks to the event loop.
2. The loop starts running.
3. Whenever a task **hits `await`** (waiting on I/O), the loop says:

   > "Cool, while you’re waiting, let me switch to another task."
4. When the task is ready again, the loop returns to it.

**Analogy:**
The event loop is like an **air traffic controller** at an airport. Planes (tasks) don’t fly all at once—they wait for permission. The controller ensures everyone gets a turn and no one collides.

---

## 4. **Coroutines (`async def`, `await`)**

* A **coroutine** is a special function defined with `async def`.
* Instead of running immediately, it produces a coroutine object (something the event loop can run).
* Inside coroutines, you use `await` to pause execution until another coroutine finishes.

**Example (simple):**

```python
import asyncio

async def greet():
    print("Hello")
    await asyncio.sleep(1)   # non-blocking wait
    print("World")

asyncio.run(greet())
```

**Output:**

```
Hello
(1 second pause)
World
```

**Key points:**

* `async def` defines a coroutine.
* `await` is like saying: “Pause me here, and let the event loop handle others.”
* Without `await`, it’s just a normal function call.

---

## 5. **Running Coroutines**

There are multiple ways:

### 🔹 `asyncio.run()`

* Simplest way (Python 3.7+).
* Runs the event loop, executes the coroutine, and closes the loop.

```python
import asyncio

async def main():
    print("Start")
    await asyncio.sleep(1)
    print("End")

asyncio.run(main())
```

---

### 🔹 `await` (inside another coroutine)

* If you’re already inside an async function, you just `await` another coroutine.

```python
async def say_hello():
    await asyncio.sleep(1)
    print("Hello")

async def main():
    await say_hello()
    print("Done")

asyncio.run(main())
```

---

### 🔹 `loop.run_until_complete()` (old style)

* Older API, less used now but still important to know.

```python
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
```

---

## 6. **Hello World Example in AsyncIO**

Let’s compare synchronous vs asynchronous:

### 🔹 Synchronous

```python
import time

def greet(name):
    time.sleep(1)
    print(f"Hello, {name}")

def main():
    greet("Alice")
    greet("Bob")

main()
```

⏱ Takes \~2 seconds.

---

### 🔹 Asynchronous

```python
import asyncio

async def greet(name):
    await asyncio.sleep(1)
    print(f"Hello, {name}")

async def main():
    await asyncio.gather(
        greet("Alice"),
        greet("Bob")
    )

asyncio.run(main())
```

⏱ Takes \~1 second (both run concurrently).

---
## Example: Make a function `async def chef(dish, time)` that simulates cooking different dishes (use `asyncio.sleep`). Run multiple dishes at once using `asyncio.gather`.

let’s solve the **chef problem** step by step, with analogy and code.

---

## 🟢 Problem Statement

We need a function:

```python
async def chef(dish, time)
```

It should simulate **cooking a dish** using `asyncio.sleep` for the given time.
Then we’ll run **multiple dishes at once** using `asyncio.gather`.

---

## 🔹 Step 1: Writing the `chef` coroutine

```python
import asyncio

async def chef(dish, time):
    print(f"👨‍🍳 Starting {dish}...")
    await asyncio.sleep(time)  # Simulating cooking time
    print(f"✅ {dish} is ready after {time} seconds!")
    return f"{dish} done"
```

* `async def` → makes it a coroutine.
* `await asyncio.sleep(time)` → simulates the cooking time in a **non-blocking** way.
* It returns a string when done.

---

## 🔹 Step 2: Running multiple dishes concurrently

```python
async def main():
    results = await asyncio.gather(
        chef("🍝 Pasta", 3),
        chef("🥗 Salad", 2),
        chef("🍕 Pizza", 5),
    )
    print("All dishes ready:", results)

asyncio.run(main())
```

---

## 🔹 Expected Output

```
👨‍🍳 Starting 🍝 Pasta...
👨‍🍳 Starting 🥗 Salad...
👨‍🍳 Starting 🍕 Pizza...
✅ 🥗 Salad is ready after 2 seconds!
✅ 🍝 Pasta is ready after 3 seconds!
✅ 🍕 Pizza is ready after 5 seconds!
All dishes ready: ['🍝 Pasta done', '🥗 Salad done', '🍕 Pizza done']
```

---

## 🔹 Real-world analogy

Think of the chef as an **async worker**:

* If he cooked synchronously, he would make pasta → wait 3 sec → then start salad → wait 2 sec → then pizza → wait 5 sec.
  ⏱ Total = 10 seconds.

* With AsyncIO, while pasta is boiling, he chops salad; while pizza is baking, he finishes salad, etc.
  ⏱ Total = max(3, 2, 5) = 5 seconds only.

---

✅ Done! We used `asyncio.gather` to run **all dishes concurrently**, just like a real chef multitasking in the kitchen.

---


# ✅ Challenge for You (Phase 1)

1. Write a synchronous function that fetches 3 URLs using `time.sleep` (simulate network delay).
   Then rewrite it using `asyncio` so all 3 run concurrently.


---
Perfect 👍 We’re now moving into **Phase 2: Tasks & Futures**.
This is one of the **most important phases** of AsyncIO because this is where concurrency really comes alive.

---

# 📌 Phase 2: Tasks & Futures

### Topics:

1. What is a Task? (`asyncio.create_task`)
2. What is a Future?
3. Converting coroutines into tasks
4. Cancelling tasks (`task.cancel`)
5. Gathering tasks (`asyncio.gather`, `asyncio.wait`)
6. Shielding tasks (`asyncio.shield`)
7. Task groups (`asyncio.TaskGroup`, Python 3.11+)

---

## 1. **What is a Task? (`asyncio.create_task`)**

* A **Task** is a wrapper around a coroutine that tells the **event loop**:

  > "Please run this coroutine in the background while I keep working."

* If you just call a coroutine with `await`, you’re saying:

  > "Run this now, and I’ll wait until you’re done."

* If you wrap it with `asyncio.create_task`, you’re saying:

  > "Start running this coroutine, but don’t block me — I’ll come back for the result later."

---

**Analogy:**
Imagine you’re a **project manager**.

* If you personally write the report (`await`), you can’t do anything else until it’s finished.
* If you assign the report to an **employee** (`create_task`), you can continue managing other projects while they work. Later, you collect the finished report (task result).

---

**Example:**

```python
import asyncio

async def worker(name, delay):
    print(f"{name} started")
    await asyncio.sleep(delay)
    print(f"{name} finished")
    return f"{name} result"

async def main():
    # Create tasks
    task1 = asyncio.create_task(worker("Task1", 2))
    task2 = asyncio.create_task(worker("Task2", 3))

    print("Both tasks are running in the background...")
    
    result1 = await task1
    result2 = await task2

    print("Results:", result1, result2)

asyncio.run(main())
```

### Output:

```
Task1 started
Task2 started
Both tasks are running in the background...
Task1 finished
Task2 finished
Results: Task1 result Task2 result
```

➡️ Notice: `Task1` and `Task2` run concurrently.

---

## 2. **What is a Future?**

* A **Future** is a low-level object representing a **result that isn’t ready yet**.
* Think of it as a **placeholder** for a value that will arrive later.

---

**Analogy:**
Imagine ordering food in a restaurant.

* The waiter gives you a **token number** (Future).
* The actual food (result) isn’t ready yet, but you’ll get it when it’s done.
* Meanwhile, you can do other things (talk, scroll phone).

That’s a Future: a promise that a value will be available later.

---

**In AsyncIO:**

* `Task` is a subclass of `Future`.
* You usually don’t create `Future` objects directly. Instead, you deal with `Tasks` (high-level, easier to use).

---

**Example (manual future):**

```python
import asyncio

async def set_future(fut):
    await asyncio.sleep(2)
    fut.set_result("Future is done!")

async def main():
    #asyncio.get_running_loop() is a function in Python's asyncio library used to retrieve the currently running event loop in the current operating system thread.
    loop = asyncio.get_running_loop()
    fut = loop.create_future()
    
    asyncio.create_task(set_future(fut))
    print("Waiting for future...")
    
    result = await fut
    print("Got result:", result)

asyncio.run(main())
```

➡️ Here, the future acts like an **empty box** that will eventually get a value.

The provided Python code snippet demonstrates how to obtain the currently running asyncio event loop and then create a new `asyncio.Future` object associated with that loop.

Here's a breakdown: 

#### `loop = asyncio.get_running_loop()`: 
- This line retrieves the active event loop for the current operating system thread. 
- `asyncio.get_running_loop()` is the preferred way to get the event loop within coroutines and callbacks, as it ensures you're interacting with the loop that's currently executing. 

#### `loop.create_future()`: 
- This method is called on the obtained event loop object. 
- It creates a new `asyncio.Future` instance. 
- An `asyncio.Future` is a low-level awaitable object that represents the eventual result of an asynchronous operation. It can be used to manage the state (pending, done, cancelled) and result (value or exception) of a computation that may not be immediately available. 
- While you can create `asyncio.Future` objects directly, `loop.create_future()` is the recommended factory method to ensure proper association with the event loop and to potentially leverage optimizations or custom implementations provided by the loop. 

In essence, this code prepares a "placeholder" for a future result within the context of the running asynchronous event loop. This Future object can then be used to signal completion, set a result, or propagate exceptions from other parts of your asynchronous program. 

----

In `asyncio`, a `Future` object represents the eventual result of an asynchronous operation. It is a low-level, awaitable object that acts as a placeholder for a value that will become available at some point in the future. (https://www.integralist.co.uk/posts/python-asyncio/)  
#### Key aspects of `asyncio.Future`: 

- Representing a Result: 
- A `Future` signifies an ongoing operation whose result is not yet available but will be provided later. This is analogous to a promise in other asynchronous programming paradigms. 
- States: 
- A `Future` can be in one of three states: 
	- Pending: The operation is still in progress, and the result is not yet available. 
	- Done: The operation has completed, and the result (or an exception) has been set. 
	- Cancelled: The operation was explicitly cancelled before completion. 

- Result and Exception Handling: 
	- The `set_result()` method is used to set the successful result of the operation. 
	- The `set_exception()` method is used to set an exception if the operation failed. 
	- The `result()` method retrieves the result (or raises the exception) once the `Future` is done. 
	- The `exception()` method retrieves the exception if one was set. 

- Awaitability: 
- `Future` objects are awaitable, meaning you can use the `await` keyword to pause the execution of a coroutine until the `Future` is done. 
- Callbacks: 
- You can attach callbacks to a Future using `add_done_callback()`. These callbacks are scheduled to run when the Future completes, regardless of whether it succeeded, failed, or was cancelled. 
- Relationship with `asyncio.Task`: 
- While `asyncio.Future` is a fundamental concept, in most high-level `asyncio` programming, you will primarily interact with `asyncio.Task` objects. An `asyncio.Task` is a subclass of `asyncio.Future` that specifically wraps and executes a coroutine within the asyncio event loop. When you use `asyncio.create_task()` or `asyncio.ensure_future()`, you are typically creating and managing Task objects, which inherit the capabilities of `Future` for result management and awaitability. 
- Bridging Callback-based Code: 
- `asyncio.Future` is particularly useful for integrating older, callback-based asynchronous code with the modern `async`/`await` syntax in `asyncio`. Functions like `loop.run_in_executor()` return `Future` objects, allowing you to `await` the completion of operations running in a separate thread or process.


---

## 3. **Converting Coroutines into Tasks**

* If you have a coroutine function (`async def`), calling it gives you a **coroutine object**.
* To actually run it **in the background**, you must wrap it with `asyncio.create_task`.

---

**Example:**

```python
import asyncio

async def greet():
    await asyncio.sleep(1)
    return "Hello!"

async def main():
    coro = greet()                   # coroutine object
    task = asyncio.create_task(coro) # wrapped as Task

    print("Task started...")
    result = await task
    print("Result:", result)

asyncio.run(main())
```

➡️ Coroutines are like **blueprints**, and tasks are like **workers** built from those blueprints.

---

## 4. **Cancelling Tasks (`task.cancel`)**

Sometimes, you don’t want a task to finish — you want to cancel it.

* You call `task.cancel()` to request cancellation.
* Inside the coroutine, it raises `asyncio.CancelledError`.
* You can catch it to clean up resources.

---

**Example:**

```python
import asyncio

async def worker():
    try:
        print("Worker started")
        await asyncio.sleep(5)
        print("Worker finished")
    except asyncio.CancelledError:
        print("Worker was cancelled!")
        raise

async def main():
    task = asyncio.create_task(worker())
    await asyncio.sleep(2)
    task.cancel()

    try:
        await task
    except asyncio.CancelledError:
        print("Caught task cancellation")

asyncio.run(main())
```

### Output:

```
Worker started
Worker was cancelled!
Caught task cancellation
```

---

## 5. **Gathering Tasks (`asyncio.gather`, `asyncio.wait`)**

### 🔹 `asyncio.gather`

* Runs multiple tasks concurrently and **collects results** in order.
* If one task fails, the others are also cancelled.

```python
async def main():
    results = await asyncio.gather(
        worker("A", 2),
        worker("B", 3),
        worker("C", 1)
    )
    print("Results:", results)
```

➡️ All tasks run in parallel, and you get a list of results.

---

### 🔹 `asyncio.wait`

* More flexible than `gather`.
* You can choose to wait for **all tasks** or just the **first one**.

```python
async def main():
    tasks = [asyncio.create_task(worker("X", 2)),
             asyncio.create_task(worker("Y", 3))]
    
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    print("First task finished:", done)
```

---

**Analogy:**

* `gather` = order **all dishes** and wait until everyone’s done.
* `wait` = wait for **first dish**, then maybe cancel or keep waiting.

## More Detailed
## Introduction to asyncio

The `asyncio` library is a powerful framework in Python for writing concurrent code using the `async/await` syntax. This paradigm is known as **cooperative multitasking**, where tasks voluntarily yield control, allowing other tasks to run. This differs from pre-emptive multitasking, where the operating system can interrupt and switch tasks at any time.

## What is a Task?

In `asyncio`, a **Task** is a wrapper around a coroutine. A coroutine is a special type of function that can be paused and resumed. The `asyncio` event loop schedules and runs tasks, managing their execution and switching between them. Tasks are the fundamental unit for concurrent execution in `asyncio`.

## Gathering Tasks

Gathering tasks is the process of running multiple coroutines concurrently and waiting for all of them to complete. The primary way to achieve this is by using the `asyncio.gather()` function.

### `asyncio.gather()`

`asyncio.gather(*aws, return_exceptions=False)` is the go-to function for gathering tasks. It takes one or more awaitable objects (coroutines or tasks) and runs them concurrently.

  * `*aws`: This can be any number of awaitables. `gather()` will automatically wrap coroutines in `Task` objects.
  * `return_exceptions`: If set to `True`, `gather()` will not raise an exception immediately if a coroutine fails. Instead, it will wait for all other coroutines to finish and return the exception objects as part of the result list. If `False` (the default), the first exception encountered is immediately propagated.

**Syntax**

```python
import asyncio

async def my_coroutine(name):
    print(f"Starting {name}")
    await asyncio.sleep(1)
    print(f"Finishing {name}")
    return f"Result from {name}"

async def main():
    results = await asyncio.gather(
        my_coroutine("Task 1"),
        my_coroutine("Task 2"),
        my_coroutine("Task 3")
    )
    print("All tasks are done.")
    print(f"Results: {results}")

if __name__ == "__main__":
    asyncio.run(main())
```

**Output:**

```
Starting Task 1
Starting Task 2
Starting Task 3
Finishing Task 1
Finishing Task 2
Finishing Task 3
All tasks are done.
Results: ['Result from Task 1', 'Result from Task 2', 'Result from Task 3']
```

### Key Concepts

  * **Order of Results**: The results returned by `asyncio.gather()` are in the **same order** as the awaitables provided in the function call.
  * **Cancellation**: You can cancel a `gather` future by calling its `cancel()` method. This will then propagate the cancellation to the underlying tasks. If a task is cancelled, a `CancelledError` is raised in the task.
  * **Error Handling**: Without `return_exceptions=True`, if one task raises an exception, the `gather` call will immediately raise that exception, and the other tasks will continue to run in the background unless they are explicitly cancelled.

### Common Alternatives and Comparisons

While `asyncio.gather()` is the most common method, other functions also exist for managing multiple tasks.

  * **`asyncio.wait()`**: This function is more primitive and flexible than `gather`. It returns two sets of tasks: `(done, pending)`. You can specify a timeout and how to wait (e.g., `asyncio.FIRST_COMPLETED`, `asyncio.FIRST_EXCEPTION`, or `asyncio.ALL_COMPLETED`). Unlike `gather`, `wait` does not automatically cancel pending tasks, and it does not return the results of the completed tasks directly; you must retrieve them from the `done` set.

  * **`asyncio.as_completed()`**: This is an iterator that yields tasks as they are completed. This is useful when you want to process results as they become available rather than waiting for all tasks to finish. It returns a future object for each completed task, which you then need to await to get the result.

| Feature | `asyncio.gather()` | `asyncio.wait()` | `asyncio.as_completed()` |
| :--- | :--- | :--- | :--- |
| **Return Value** | List of results/exceptions. | Tuple of `(done, pending)` sets. | Async iterator over futures. |
| **Result Order** | Preserved (same as input). | Not preserved (depends on completion time). | Not preserved (depends on completion time). |
| **Error Handling** | Raises first exception by default. Can collect exceptions with `return_exceptions=True`. | Can wait for `FIRST_EXCEPTION`. | Raises exceptions as they occur. |
| **Primary Use Case** | Run tasks concurrently and collect all results in a single batch. | Wait for a specific condition (e.g., first task to finish) or with a timeout. | Process results as they become available, without waiting for all tasks to complete. |

-----


## 6. **Shielding Tasks (`asyncio.shield`)**

* Sometimes, you want to cancel the parent coroutine but keep a child task running.
* `asyncio.shield` protects a task from being cancelled.

---

**Example:**

```python
async def protected_task():
    await asyncio.sleep(3)
    return "Protected done!"

async def main():
    task = asyncio.create_task(protected_task())
    try:
        await asyncio.wait_for(asyncio.shield(task), timeout=1)
    except asyncio.TimeoutError:
        print("Timeout, but task is still running...")
    
    result = await task
    print("Result:", result)

asyncio.run(main())
```

➡️ Even though we timed out, the shielded task kept running.

---

## 7. **Task Groups (`asyncio.TaskGroup`, Python 3.11+)**

* New in Python 3.11.
* Provides a structured way to manage multiple tasks.
* If one task fails, all others are automatically cancelled.
* Think of it as a **team project manager**.

---

**Example:**

```python
async def do_work(i):
    await asyncio.sleep(i)
    print(f"Work {i} done")
    return i

async def main():
    async with asyncio.TaskGroup() as tg:
        tg.create_task(do_work(1))
        tg.create_task(do_work(2))
        tg.create_task(do_work(3))
    print("All tasks completed!")

asyncio.run(main())
```

### Output:

```
Work 1 done
Work 2 done
Work 3 done
All tasks completed!
```
---
When using **asyncio.TaskGroup** in Python, if any task in the group fails with an unhandled exception, all other tasks in that group are automatically cancelled, ensuring robust error handling and structured concurrency in asynchronous applications. see example below.

## Example

```python
import asyncio

async def task1():
    await asyncio.sleep(1)
    return "Task 1 done"

async def task2():
    await asyncio.sleep(2)
    return "Task 2 done"

async def task_with_error():
    await asyncio.sleep(1)
    raise ValueError("An error occurred")

async def main():
    try:
        async with asyncio.TaskGroup() as tg:
            t1 = tg.create_task(task1())
            t2 = tg.create_task(task2())
            t3 = tg.create_task(task_with_error())
    except Exception as e:
        print(f"Error: {e}")

asyncio.run(main())
```

- In this example, as soon as `task_with_error()` raises an exception, both `task1` and `task2` are cancelled and the exception is propagated.

## Real-Life Use Cases

- **API Aggregation**: Fetching data from several APIs at once, but aborting all requests if any fails to avoid inconsistent data or wasted effort.
- **Microservice Coordination**: Coordinating calls to multiple microservices, ensuring that if one fails, no partial action is taken—ideal for transactional or batch operations in distributed systems.
- **Batch Processing**: Running multiple background jobs concurrently (e.g., data uploads), and cancelling all jobs if one job encounters a fatal error.
- **Database or File Operations**: Writing to multiple databases or files in parallel, ensuring consistency by cancelling all writes if any single write fails.

## Summary Table

| Feature                  | Description                                      |
|--------------------------|--------------------------------------------------|
| **Failure Handling**     | Cancels all tasks if any fails     |
| **Common Use Case**      | API/data aggregation, batch job orchestration  |
| **How to Use**           | Use `asyncio.TaskGroup()` context manager        |
| **Introduced In**        | Python 3.11                                      |

This pattern is extremely useful for managing critical sections in async code where partial success is not acceptable and robust error handling is necessary.

---

**Another Example**

The `asyncio.TaskGroup` in Python 3.11+ provides a convenient way to manage a group of asynchronous tasks, including automatic cancellation of other tasks within the group if one task fails.
Example of `asyncio.TaskGroup` with failure propagation: 

```python
import asyncio

    async def worker_task(name, should_fail=False):
        """A worker coroutine that can optionally raise an exception."""
        print(f"Task {name}: Starting...")
        await asyncio.sleep(0.5)  # Simulate some work

        if should_fail:
            print(f"Task {name}: Intentionally failing!")
            raise ValueError(f"Error in {name}")

        print(f"Task {name}: Completed successfully.")

    async def main():
        try:
            async with asyncio.TaskGroup() as tg:
                # Create a task that will fail
                tg.create_task(worker_task("Alpha", should_fail=True))
                # Create tasks that would otherwise succeed
                tg.create_task(worker_task("Beta"))
                tg.create_task(worker_task("Gamma"))
        except `ExceptionGroup` as eg:
            print(f"\nCaught an `ExceptionGroup`: {eg.exceptions}")
            for exc in eg.exceptions:
                print(f"  - {type(exc).__name__}: {exc}")
        except Exception as e:
            print(f"\nCaught a general exception: {e}")

    if __name__ == "__main__":
        asyncio.run(main())
```

Explanation: 

- `worker_task`: This asynchronous function simulates a task, and it can be configured to raise a `ValueError` to demonstrate failure. 
- `main` function and `asyncio.TaskGroup`: 
	- The `async with asyncio.TaskGroup() as tg:` statement creates a task group as a context manager. 
	- `tg.create_task()` adds coroutines to the task group. In this example, "Alpha" is set to fail. 

- Failure Propagation: 
	- When `worker_task("Alpha")` raises a `ValueError`, the `TaskGroup` automatically initiates cancellation for all other active tasks within the group (e.g., "Beta" and "Gamma"). 
	- The `TaskGroup` then waits for all tasks to either complete or be cancelled. 
	- Finally, the original exception (or an `ExceptionGroup` if multiple tasks fail) is re-raised when exiting the `async with` block. 

- Exception Handling: 
	- The `try...except ExceptionGroup` as eg: block catches the `ExceptionGroup` that is raised by the `TaskGroup` when one or more child tasks fail with exceptions. 
	- This allows for centralized handling of errors that occur within the task group. 

```bash
Output of the example: 
Task Alpha: Starting...
Task Beta: Starting...
Task Gamma: Starting...
Task Alpha: Intentionally failing!

Caught an ExceptionGroup: [ValueError('Error in Alpha')]
  -ValueError: Error in Alpha
```

This output demonstrates that "Alpha" fails as expected, and the `ExceptionGroup` containing the ValueError from "Alpha" is caught in the main function. The other tasks ("Beta" and "Gamma") are implicitly cancelled by the TaskGroup due to the failure of "Alpha", although their "Completed successfully" messages are not printed because they are cancelled before completion. 





---

# ✅ Challenges (Phase 2)

1. Write a coroutine `download_file(name, delay)` that simulates downloading files.

   * Run 3 downloads in parallel with `asyncio.gather`.
   * Add cancellation: cancel one download midway.

2. Use `asyncio.wait` to launch 5 workers or download_file and return as soon as the **first worker finishes**.

3. Write a program using `asyncio.TaskGroup` where one task fails (raises an exception).

   * Show how all other tasks get cancelled automatically.

---




## Here we covers these topics (we’ll follow this order):

* 3 — **Asynchronous I/O** (sleep, files, sockets, subprocesses, `aiofiles`)
* 4 — **Synchronization Primitives** (`Lock`, `Semaphore`, `Event`, `Condition`, producer/consumer)
* 5 — **Queues** (`asyncio.Queue`, `PriorityQueue`, `LifoQueue`, producer/consumer pattern\`)
* 6 — **Timeouts & Cancellations** (`task.cancel`, `CancelledError`, `wait_for`, patterns)
* 7 — **AsyncIO Streams** (TCP server/client, UDP, `StreamReader`/`StreamWriter`, chat example)
* 8 — **AsyncIO + Context Managers & Iterators** (`async with`, `async for`, custom async iterators, using `StreamReader` with `async for`)

---

# 3 — Asynchronous I/O (deep dive)

## Concept & analogy

I/O is waiting: network, disk, subprocess output.
**Analogy:** I/O is like ordering food at a food court. You place an order and wait for the stall to make it. Instead of standing idle, you walk to another stall (do other work). Async I/O is “keep moving while orders are being prepared.”

### `asyncio.sleep` — the non-blocking wait

`asyncio.sleep()` is a placeholder for any non-blocking wait. It yields control to the event loop so other coroutines can run.

**Example**

```python
# sleep_example.py
import asyncio   # import asyncio module

async def waiter(name, delay):
    # print start
    print(f"{name}: waiting for {delay} seconds")
    # non-blocking sleep; yields control to event loop
    await asyncio.sleep(delay)
    # resumes after delay
    print(f"{name}: done waiting")

async def main():
    # schedule two coroutines concurrently and wait for both
    await asyncio.gather(
        waiter("A", 2),
        waiter("B", 1),
    )

if __name__ == "__main__":
    # run the async main() on the event loop
    asyncio.run(main())
```

---

## Asynchronous file I/O — `aiofiles`

CPython file API is blocking; use `aiofiles` for async-style file IO (wraps blocking file ops in threads).

Install: `pip install aiofiles`

**Example: read & write files asynchronously**

```python
# aiofiles_example.py
import asyncio               # core async library
import aiofiles              # third-party async file I/O lib

async def write_file(path, data):
    # open file asynchronously for writing
    async with aiofiles.open(path, mode="w") as f:
        # write data (await because it's async)
        await f.write(data)

async def read_file(path):
    # open file asynchronously for reading
    async with aiofiles.open(path, mode="r") as f:
        # read entire file contents
        contents = await f.read()
        return contents

async def main():
    # write and read concurrently (writes then reads)
    await write_file("test.txt", "hello async world\n")
    content = await read_file("test.txt")
    print("File content:", content)

if __name__ == "__main__":
    asyncio.run(main())
```

**Note & pitfall:** `aiofiles` uses threadpool under the hood. For heavy file IO, explicit `run_in_executor` or streaming is better.

## deep explanation
`aiofiles` is a Python library that enables asynchronous file operations within asyncio applications, preventing blocking I/O from freezing your program. It provides a separate thread pool to execute standard, blocking file operations in the background, allowing your main event loop to remain responsive and handle other tasks concurrently. This is crucial for efficient, scalable applications that need to perform file I/O without stalling the application.   
Why `aiofiles` is needed 

- **Blocking I/O:** Standard file operations (like `open()`, `read()`, `write()`) are synchronous and "block" the executing thread, meaning the program waits for the operation to complete before moving on.   
- **Asyncio applications:** In asyncio, which uses an event loop for non-blocking execution, blocking operations can significantly hinder performance and responsiveness. 
- **Solution:** `aiofiles` addresses this by offloading these blocking file tasks to a separate thread pool, making them appear asynchronous to the main event loop.   

How it works 

**1. Asynchronous file objects:** `aiofiles` provides asynchronous equivalents of Python's standard file objects and functions (e.g., `aiofiles.open()`).   
**2. Thread pool delegation:** When you call an `aiofiles` method, such as `read()`, the operation is sent to a background thread pool to be executed.   
**3. Non-blocking behavior:** While the file operation runs in the background, your asyncio application can continue to run other tasks and respond to events.   
**4. Results:** Once the file operation is complete, the result is returned to the asyncio event loop without blocking it.   

Key benefits 

- **Improved Responsiveness:** Prevents file I/O from making your application unresponsive to user input or other tasks.   
- **Increased Scalability:** Allows your application to handle many file operations concurrently, improving overall throughput.   
- **Seamless Integration:** Integrates well with other asynchronous libraries, such as aiohttp for web requests.   
- **Efficiency:** Achieves better performance compared to purely synchronous code by allowing other tasks to run while I/O is in progress.   

- how do blocking operations hinder asyncio applications?
- Blocking operations hinder asyncio applications by halting the event loop, preventing other tasks from running and causing the entire application to become unresponsive. Asyncio is designed to handle many tasks concurrently by yielding control to an event loop, which can then execute other tasks while waiting for I/O-bound operations to complete. A single blocking call, however, stops this process, effectively defeating the purpose of asynchronous, non-blocking programming and leading to poor performance and a sluggish user experience.

**Example**
- Consider an asyncio application that makes several network requests:
- With non-blocking operations:
    - The program initiates multiple requests and uses await to wait for responses, yielding control to the event loop in the meantime. The event loop can then service other requests or tasks.
- With a blocking operation:
    - If you mistakenly use a synchronous sleep function (like time.sleep(10)) instead of an asynchronous one (like asyncio.sleep(10)), the entire event loop will pause for 10 seconds. No other requests can be processed during this time.

---

## Networking basics & sockets
Asyncio in Python provides a powerful framework for writing concurrent network applications using asynchronous I/O. It allows you to handle multiple network connections efficiently within a single thread, making it suitable for I/O-bound tasks like web servers, clients, and network automation.

Key Concepts:

**Coroutines:**
Functions defined with `async def` are coroutines. They can pause their execution using `await` and yield control back to the event loop, allowing other coroutines to run.

**Event Loop:**
The central component of `asyncio`, responsible for managing and scheduling the execution of coroutines and handling I/O events.

**Tasks:**
Coroutines wrapped in `asyncio.Task` objects. Tasks are scheduled by the event loop and represent independent units of execution.

**Streams:**
A high-level API in asyncio for working with network connections. `asyncio.open_connection()` and `asyncio.start_server()` are used to establish and manage TCP connections, providing `StreamReader` and `StreamWriter` objects for reading and writing data.

**Protocols:**
A lower-level API for implementing custom network protocols. You define classes that inherit from `asyncio.Protocol` and implement methods to handle connection events and data reception.

[Read More](https://heycoach.in/blog/asyncio-for-networking/)
<!-- Two primary styles in asyncio:

* **High-level streams API:** `asyncio.start_server`, `asyncio.open_connection` — easiest.
* **Low-level transports/protocols** or raw sockets for advanced use. -->

**TCP echo server & client (streams)** — commented

```python
# tcp_echo_server.py
import asyncio

async def handle_client(reader, writer):
    # read one line from client (until newline)
    data = await reader.readline()
    # decode bytes to str
    message = data.decode().rstrip()
    addr = writer.get_extra_info("peername")
    print(f"Received {message!r} from {addr}")

    # echo back the message
    writer.write(data)
    # ensure data is sent
    await writer.drain()

    # close the connection
    writer.close()
    await writer.wait_closed()

async def main():
    # start a TCP server on localhost:8888, using handle_client callback
    server = await asyncio.start_server(handle_client, "127.0.0.1", 8888)
    # show server sockets info
    addrs = ", ".join(str(sock.getsockname()) for sock in server.sockets)
    print(f"Serving on {addrs}")

    # serve forever until cancelled
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
```

Client:

```python
# tcp_echo_client.py
import asyncio

async def tcp_echo(message):
    # open connection to server
    reader, writer = await asyncio.open_connection("127.0.0.1", 8888)
    # send message with newline
    writer.write(f"{message}\n".encode())
    await writer.drain()                     # ensure it's sent

    # read echoed line
    data = await reader.readline()
    print("Received:", data.decode().rstrip())

    # close
    writer.close()
    await writer.wait_closed()

if __name__ == "__main__":
    asyncio.run(tcp_echo("hello from client"))
```

---

## Subprocesses: `asyncio.create_subprocess_exec`

Run subprocesses without blocking event loop, read stdout/stderr asynchronously.

**Example: call `ls` / `dir` and read output**

```python
# subprocess_example.py
import asyncio

async def run_cmd():
    # create subprocess; capture stdout and stderr pipes
    proc = await asyncio.create_subprocess_exec(
        "python", "--version",           # command and args
        stdout=asyncio.subprocess.PIPE,  # capture stdout
        stderr=asyncio.subprocess.PIPE   # capture stderr
    )

    # read stdout and stderr asynchronously
    stdout, stderr = await proc.communicate()
    print("Return code:", proc.returncode)
    print("STDOUT:", stdout.decode().strip())
    print("STDERR:", stderr.decode().strip())

if __name__ == "__main__":
    asyncio.run(run_cmd())
```

**Pitfalls:**

* Don’t block reading large subprocess output on `.read()`: prefer streaming or `.communicate()`.
* Beware of shell=True security risks.

---

## Short summary (Asynchronous I/O)

* `asyncio.sleep` simulates waiting without blocking.
* For file I/O use `aiofiles` or `run_in_executor`.
* For network use streams API.
* For subprocesses use `create_subprocess_exec` & `.communicate()`.

### Challenges (Asynchronous I/O)

1. Build an async downloader that fetches text from 3 URLs using `aiohttp` (or simulate with `asyncio.sleep`) and writes to separate files using `aiofiles`. (Requires `aiohttp` & `aiofiles`.)
2. Modify the TCP echo server to serve multiple messages per client (loop until client sends `"quit"`), using `async for` on `reader`.
3. Write an async script that runs 5 subprocesses (e.g., `python -c "print(...)"`) concurrently and aggregates their outputs.

---

# 4 — Synchronization Primitives

## Why we need them (analogy)

Multiple coroutines may access shared resources (e.g., a shared printer). **Analogy:** multiple people sending print jobs — you need a lock or the printer jams.

### `asyncio.Lock`

`asyncio.Lock` in Python provides a mechanism for synchronizing access to shared resources among coroutines within a single `asyncio` event loop. It functions as a mutex (mutual exclusion) lock, ensuring that only one coroutine can acquire the lock and access a critical section of code at any given time. 

#### **Key characteristics and usage:** 

* **Mutex for Coroutines:** `asyncio.Lock` is designed for use within asyncio applications to manage concurrency between coroutines. It is explicitly not thread-safe and should not be used for synchronization between threads; for that, `threading.Lock` is required. 
* **Acquiring and Releasing:** 
	* A coroutine acquires the lock using `await lock.acquire()`. If the lock is already held by another coroutine, the current coroutine will pause and wait until the lock is released. 
	* The lock is released using `lock.release()`. 

* **`async with` Statement (Preferred Method):** The most common and recommended way to use `asyncio.Lock` is with the `async with` statement. This ensures the lock is automatically acquired at the beginning of the block and released at the end, even if exceptions occur within the critical section. 

```python
    import asyncio

    async def critical_section(lock, name):
        async with lock:
            print(f"{name} acquired the lock and is accessing shared resource.")
            await asyncio.sleep(0.1)  # Simulate some work
            print(f"{name} released the lock.")

    async def main():
        lock = asyncio.Lock()
        await asyncio.gather(
            critical_section(lock, "Task 1"),
            critical_section(lock, "Task 2")
        )

    if __name__ == "__main__":
        asyncio.run(main())
```

* **Preventing Race Conditions:** `asyncio.Lock` is essential for preventing race conditions when multiple coroutines might attempt to modify shared data or access a resource simultaneously, leading to unpredictable or incorrect results. 

In summary: `asyncio.Lock` is a fundamental synchronization primitive in `asyncio` for managing exclusive access to shared resources among concurrently running coroutines within a single event loop, with the `async with` statement being the preferred usage pattern for safety and convenience. 



Exclusive access. Only one coroutine holds lock at a time.

**Example**

```python
# lock_example.py
import asyncio

async def safe_increment(name, counter, lock):
    # try to acquire lock
    async with lock:
        # inside critical section
        val = counter["value"]
        print(f"{name} sees {val}")
        await asyncio.sleep(0.1)  # simulate work
        counter["value"] = val + 1
        print(f"{name} incremented to {counter['value']}")

async def main():
    lock = asyncio.Lock()          # create lock
    counter = {"value": 0}         # shared resource (dict for mutability)
    # run 5 tasks that increment counter concurrently
    await asyncio.gather(
        *(safe_increment(f"task{i}", counter, lock) for i in range(5))
    )
    print("Final counter:", counter["value"])

if __name__ == "__main__":
    asyncio.run(main())
```

---

### `asyncio.Semaphore`

`asyncio.Semaphore` in Python is a synchronization primitive used in `asyncio` programs to limit the number of concurrent tasks accessing a shared resource. It operates by maintaining an internal counter, initialized with a specified `value` that represents the maximum number of concurrent acquisitions allowed. 

#### **How it works:** 

- **Initialization:** You create an `asyncio.Semaphore` instance by providing an integer `value` to its constructor, e.g., `semaphore = asyncio.Semaphore(5)`. This `value` sets the maximum number of tasks that can acquire the semaphore simultaneously. 
- **Acquiring the Semaphore:** 
	- Tasks attempt to acquire the semaphore using `await semaphore.acquire()` or, more commonly, within an `async with` statement: `async with semaphore:`. 
	- When a task acquires the semaphore, the internal counter is decremented. 
	- If the counter is greater than zero, the acquisition succeeds immediately. [1]  
	- If the counter is zero, the task blocks and waits until another task releases the semaphore, increasing the counter. 

- **Releasing the Semaphore:** 
	- Tasks release the semaphore using `semaphore.release()`. 
	- Releasing the semaphore increments the internal counter, potentially allowing a waiting task to acquire it. 
	- Using `async with semaphore:` automatically handles the release when the block is exited, even if exceptions occur. 

#### **Common Use Cases:** 

- **Rate Limiting:** Controlling the number of concurrent requests to an external API or a database to avoid exceeding limits. 
- **Resource Management:** Limiting access to resources that can only handle a certain number of concurrent operations, like database connections or file handles. 
- **Controlling Concurrency:** Ensuring that only a specific number of tasks are actively running at any given time, preventing resource exhaustion. 

Example: 
```python
import asyncio

async def worker(semaphore, name):
    print(f"{name}: Waiting to acquire semaphore...")
    async with semaphore:
        print(f"{name}: Acquired semaphore, working...")
        await asyncio.sleep(2)  # Simulate some work
        print(f"{name}: Released semaphore.")

async def main():
    # Allow a maximum of 2 concurrent workers
    semaphore = asyncio.Semaphore(2)

    tasks = [
        asyncio.create_task(worker(semaphore, "Worker A")),
        asyncio.create_task(worker(semaphore, "Worker B")),
        asyncio.create_task(worker(semaphore, "Worker C")),
        asyncio.create_task(worker(semaphore, "Worker D")),
    ]

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
```

In this example, only two `worker` tasks will be able to execute concurrently, as dictated by the `semaphore`'s initial value of 2. The other tasks will wait until a slot becomes available. 


[1] https://superfastpython.com/asyncio-semaphore/


Limits concurrent access to N coroutines (e.g., connection pool). **Analogy:** N identical printers; only N jobs can print at once.

**Example**

```python
# semaphore_example.py
import asyncio

async def limited_worker(i, sem):
    # acquire semaphore (decrements internal counter)
    async with sem:
        print(f"Worker {i} acquired slot")
        await asyncio.sleep(1)  # simulated task
        print(f"Worker {i} releasing slot")

async def main():
    sem = asyncio.Semaphore(2)   # max 2 concurrent workers
    await asyncio.gather(*(limited_worker(i, sem) for i in range(5)))

if __name__ == "__main__":
    asyncio.run(main())
```

---

### `asyncio.Event`

`asyncio.Event` in Python is an asynchronous synchronization primitive provided by the `asyncio` library. It functions similarly to a traditional `threading.Event`, but it is designed for use within `asyncio`'s single-threaded event loop to coordinate between multiple coroutines. 

**Key features and usage:**

- Internal Flag: An `asyncio.Event` object manages an internal boolean flag, which can be in either a "set" (True) or "clear" (False) state. 
- `set()` method: The `set()` method changes the internal flag to `True`. This unblocks any coroutines that are currently `await`ing the event. 
- `clear()` method: The `clear()` method changes the internal flag back to `False`. 
- `wait()` method: The `await event.wait()` method is a coroutine that blocks until the internal flag is set to `True`. If the flag is already `True` when `wait()` is called, it returns immediately. 
- `is_set()` method: The `is_set()` method returns the current state of the internal flag (`True` if set, `False` if clear). 

Example: 
```python
import asyncio

async def waiter(event, name):
    print(f"Coroutine {name}: Waiting for event...")
    await event.wait()
    print(f"Coroutine {name}: Event received!")

async def setter(event):
    await asyncio.sleep(1) # Simulate some work
    print("Setter: Setting the event...")
    event.set()

async def main():
    event = asyncio.Event()
    task1 = asyncio.create_task(waiter(event, "A"))
    task2 = asyncio.create_task(waiter(event, "B"))
    task_setter = asyncio.create_task(setter(event))

    await asyncio.gather(task1, task2, task_setter)

if __name__ == "__main__":
    asyncio.run(main())
```

**Explanation of the example:** 

- Two `waiter` coroutines are created, both `await`ing the `event.wait()`. They will pause execution until the event is set. 
- A `setter` coroutine is created, which, after a delay, calls `event.set()`. 
- When `event.set()` is called, both `waiter` coroutines are unblocked and resume their execution. 
- asyncio.gather() is used to run all tasks concurrently and wait for their completion. 

`asyncio.Event` is valuable for coordinating actions between different parts of an asynchronous program, allowing coroutines to signal and wait for specific conditions or events to occur. 

[Read more](https://superfastpython.com/asyncio-event/)



---

One coroutine signals others (like a starting pistol). Coroutines wait on `.wait()` until `.set()` is called.

**Example**

```python
# event_example.py
import asyncio

async def waiter(name, ev):
    print(f"{name} waiting for event")
    await ev.wait()            # wait until event is set
    print(f"{name} proceeding")

async def main():
    ev = asyncio.Event()
    # start waiters
    tasks = [asyncio.create_task(waiter(i, ev)) for i in ("A","B")]
    await asyncio.sleep(1)
    print("Setting event")
    ev.set()                   # wake all waiters
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
```

---

### `asyncio.Condition`

`asyncio.Condition` in Python is a synchronization primitive used in asynchronous programming with `asyncio`. It combines the functionality of an `asyncio.Lock` and an `asyncio.Event`, allowing tasks to wait for a specific condition to become true and then gain exclusive access to a shared resource.

**Key features and usage:** 

- **Combines Lock and Event:** 
A `Condition` object inherently includes a lock. When a task calls `await condition.acquire()`, it acquires the underlying lock. When it calls `await condition.wait()`, it releases the lock and suspends its execution until notified, then re-acquires the lock upon awakening. This ensures exclusive access to shared resources while waiting for a condition. 
- **Waiting for a Condition:** 
	- `await condition.wait()`: A task can call this to suspend its execution and wait for a notification from another task. It releases the lock before waiting and re-acquires it after being notified. 
	- `await condition.wait_for(predicate)`: This method waits until a `predicate` (a callable that returns a boolean) evaluates to `True`. The predicate is checked each time a notification is received. 

- **Notifying Waiting Tasks:** 
	- `condition.notify(n=1)`: Wakes up at most `n` tasks that are waiting on this condition. 
	- `condition.notify_all()`: Wakes up all tasks that are currently waiting on this condition. 

Example: 
```py
import asyncio

async def consumer(condition, item_list):
    async with condition:
        await condition.wait_for(lambda: len(item_list) > 0) # Wait until an item is available
        item = item_list.pop(0)
        print(f"Consumer consumed: {item}")

async def producer(condition, item_list):
    for i in range(3):
        await asyncio.sleep(0.5) # Simulate some work
        async with condition:
            item_list.append(f"item_{i}")
            print(f"Producer produced: item_{i}")
            condition.notify_all() # Notify all waiting consumers

async def main():
    item_list = []
    condition = asyncio.Condition()

    # Start consumers before producers to ensure they are waiting
    consumers = [asyncio.create_task(consumer(condition, item_list)) for _ in range(2)]
    producer_task = asyncio.create_task(producer(condition, item_list))

    await asyncio.gather(producer_task, *consumers)

if __name__ == "__main__":
    asyncio.run(main())
```
In this example, consumers use `condition.wait_for()` to wait until the `item_list` is not empty, while the producer adds items and uses `condition.notify_all()` to inform waiting consumers. The `async with condition:` statement ensures that the lock is acquired and released correctly around critical sections. 

[Read More](https://superfastpython.com/asyncio-condition-variable/)

---

Condition variable — combine a lock with notifications. Useful for producer/consumer signaling with more control.

**Example**

```python
# condition_example.py
import asyncio
from collections import deque

async def producer(cond, q):
    i = 0
    while i < 3:
        await asyncio.sleep(0.5)
        async with cond:
            q.append(i)
            print("Produced", i)
            # notify one or all waiters
            cond.notify()
        i += 1

async def consumer(cond, q):
    while True:
        async with cond:
            while not q:          # wait until queue has item
                await cond.wait()
            item = q.popleft()
        print("Consumed", item)
        if item == 2:
            break

async def main():
    cond = asyncio.Condition()
    q = deque()
    await asyncio.gather(producer(cond, q), consumer(cond, q))

if __name__ == "__main__":
    asyncio.run(main())
```

---
### **producer-consumer problem**

The producer-consumer problem in AsyncIO in Python involves coordinating asynchronous tasks (coroutines) that share a common data buffer, typically an asyncio.Queue. Producers generate data and add it to the queue, while consumers retrieve data from the queue and process it. This pattern is particularly useful for managing concurrent I/O-bound operations and for limiting the number of concurrent tasks.

#### **Core Components:**
**asyncio.Queue:**
- This is the central element for communication. It provides asynchronous methods like `put()` to add items and `get()` to retrieve items. These methods handle the necessary synchronization, ensuring producers don't add to a full queue and consumers don't try to retrieve from an empty queue.
**Producer Coroutines:**
- These coroutines are responsible for generating data. They use `await queue.put(item)` to add items to the shared queue.
**Consumer Coroutines:**
- These coroutines are responsible for processing data. They use `await queue.get()` to retrieve items from the shared queue and then perform their designated work.

#### **Example Implementation:**

```Python

import asyncio
import random

async def producer(queue: asyncio.Queue, num_items: int):
    """Generates items and puts them into the queue."""
    for i in range(num_items):
        item = f"Item-{i}"
        print(f"Producer: Putting {item} into the queue.")
        await queue.put(item)
        await asyncio.sleep(random.uniform(0.1, 0.5)) # Simulate work

async def consumer(queue: asyncio.Queue, consumer_id: int):
    """Retrieves items from the queue and processes them."""
    while True:
        item = await queue.get()
        if item is None: # Sentinel value to signal termination
            print(f"Consumer {consumer_id}: Received termination signal.")
            break
        print(f"Consumer {consumer_id}: Processing {item}.")
        await asyncio.sleep(random.uniform(0.2, 0.8)) # Simulate work
        queue.task_done() # Indicate that the item has been processed

async def main():
    queue = asyncio.Queue(maxsize=5) # Limit queue size
    num_items = 10
    num_consumers = 3

    # Start producer task
    producer_task = asyncio.create_task(producer(queue, num_items))

    # Start consumer tasks
    consumer_tasks = [
        asyncio.create_task(consumer(queue, i)) for i in range(num_consumers)
    ]

    # Wait for the producer to finish
    await producer_task

    # Add sentinel values to signal consumers to terminate
    for _ in range(num_consumers):
        await queue.put(None)

    # Wait for all consumers to finish
    await asyncio.gather(*consumer_tasks)
    print("All tasks completed.")

if __name__ == "__main__":
    asyncio.run(main())
```

#### **Key Concepts:**
**Concurrency:**
Producers and consumers run concurrently, making progress independently.

**Synchronization:**
`asyncio.Queue` handles the synchronization, preventing race conditions and ensuring data integrity.

**Flow Control:**
`maxsize` in `asyncio.Queue` can be used to limit the buffer size, preventing producers from overwhelming consumers or memory usage.

**Termination:**
Using a sentinel value (like `None` in the example) is a common way to signal consumers to stop processing when the producer is finished.

**queue.task_done()** and **queue.join()**:
These methods can be used to track the completion of items in the queue and wait until all queued items have been processed by consumers.

---

### Producer-Consumer recap

* Use `Queue` (next section) for simpler implementations: `Queue` handles locking & waiting internally.
* Use `Condition` when you need custom wake logic.

### Challenges (Synchronization Primitives)

1. Implement a shared resource pool with `Semaphore` that limits to 3 concurrent users; each user prints a message while holding a slot.
2. Build a small system where a monitor coroutine waits on an `Event` to start multiple worker coroutines simultaneously.
3. Re-implement the producer/consumer above using `Condition`, then rewrite using `asyncio.Queue` and compare simplicity and correctness.

---

# 5 — Queues

`asyncio.Queue` in Python provides an asynchronous, non-thread-safe queue implementation designed for use within asyncio applications. It functions similarly to the standard library's queue.Queue but is tailored for async/await syntax. 

**Key Features and Usage:** 

- **First-In, First-Out (FIFO):** Items are retrieved in the order they were added, by default. 
- **Asynchronous Operations:** 
	- await put(item): Adds an item to the queue. If the queue is full (when maxsize is set and reached), this operation will await until space becomes available. 
	- await get(): Removes and returns an item from the queue. If the queue is empty, this operation will await until an item is available. 

- **Bounded or Unbounded:** 
	- asyncio.Queue(maxsize=0): Creates an unbounded queue (default). 
	- asyncio.Queue(maxsize=N): Creates a bounded queue that can hold at most N items. 

- **Producer-Consumer Pattern:** `asyncio.Queue` is commonly used to implement the producer-consumer pattern in asynchronous applications. Producers add items to the queue, and consumer coroutines get items for processing. This allows for concurrent task execution and flow control. 
- **Not Thread-Safe:** Unlike `queue.Queue`, `asyncio.Queue` is not designed for inter-thread communication. It's intended for managing tasks within a single asyncio event loop. 
- **`task_done()` and `join()`:** Similar to `queue.Queue`, `asyncio.Queue` provides `task_done()` to indicate that a retrieved item has been processed and `await join()` to block until all items previously added to the queue have been marked as done. 

Example: 
```py
import asyncio

async def producer(queue):
    for i in range(5):
        print(f"Producing: {i}")
        await queue.put(i)
        await asyncio.sleep(0.1) # Simulate some work

async def consumer(queue):
    while True:
        item = await queue.get()
        print(f"Consuming: {item}")
        await asyncio.sleep(0.2) # Simulate some work
        queue.task_done()
        if item == 4: # Example condition to stop consumer
            break

async def main():
    queue = asyncio.Queue(maxsize=3) # Bounded queue
    
    producer_task = asyncio.create_task(producer(queue))
    consumer_task = asyncio.create_task(consumer(queue))

    await producer_task
    await queue.join() # Wait for all produced items to be processed
    consumer_task.cancel() # Stop the consumer gracefully

if __name__ == "__main__":
    asyncio.run(main())
```

---

## Why queues?

Queues give safe producer/consumer communication without manual locks. **Analogy:** a conveyor belt — producers put items on the belt, consumers pick them up.

### `asyncio.Queue`

* `put()`/`get()` are coroutines (awaitable).
* Thread-safe for asyncio coroutines.

**Producer/Consumer example**

```python
# queue_example.py
import asyncio
import random

async def producer(queue, n):
    for i in range(n):
        await asyncio.sleep(random.random())   # simulate variable production time
        item = f"item-{i}"
        await queue.put(item)                  # put item on queue
        print(f"Produced {item}")
    # signal consumers to stop
    await queue.put(None)                      # sentinel

async def consumer(queue):
    while True:
        item = await queue.get()               # wait for item
        if item is None:
            # put sentinel back for other consumers and exit
            await queue.put(None)
            break
        print(f"Consumed {item}")
        await asyncio.sleep(0.1)               # simulate processing

async def main():
    q = asyncio.Queue()
    await asyncio.gather(producer(q, 5), consumer(q))

if __name__ == "__main__":
    asyncio.run(main())
```

---

### `PriorityQueue` & `LifoQueue`

Same API but different ordering semantics.

**PriorityQueue example**

```python
# priority_queue_example.py
import asyncio

async def producer(q):
    # put(item, priority)
    await q.put((2, "low-priority"))
    await q.put((0, "high-priority"))
    await q.put((1, "medium"))

async def consumer(q):
    while not q.empty():
        prio, item = await q.get()
        print("Got:", item)
        q.task_done()

async def main():
    q = asyncio.PriorityQueue()
    await producer(q)
    await consumer(q)

if __name__ == "__main__":
    asyncio.run(main())
```

---

### Challenges (Queues)

1. Implement a pipeline: producer → worker pool (N concurrency) → aggregator. Use `asyncio.Queue` for stages.
2. Use `PriorityQueue` to process urgent tasks first. Simulate with random priorities.
3. Implement LIFO queue for last-in-first-served scenario (e.g., undo stack simulation).

---

# 6 — Timeouts & Cancellations

## Cancellation model & `CancelledError` (analogy)

Cancellation is telling a worker to stop: like calling a waiter to cancel an order mid-prep. The worker receives the cancellation and can cleanup.

### Cancelling tasks

```python
# cancel_example.py
import asyncio

async def long_task():
    try:
        print("long_task: started")
        await asyncio.sleep(5)   # long-running
        print("long_task: finished")
    except asyncio.CancelledError:
        # cleanup on cancellation
        print("long_task: was cancelled, cleaning up")
        # re-raise so caller knows it was cancelled
        raise

async def main():
    task = asyncio.create_task(long_task())
    await asyncio.sleep(1)      # let it start
    task.cancel()               # request cancellation
    try:
        await task
    except asyncio.CancelledError:
        print("main: confirmed task cancelled")

if __name__ == "__main__":
    asyncio.run(main())
```

**Key:** Always catch `CancelledError` if you need cleanup; re-raise afterwards in most cases.

---

### `asyncio.wait_for` — timeout wrapper

Wrap an awaitable and raise `asyncio.TimeoutError` if it takes too long.

```python
# wait_for_example.py
import asyncio

async def task():
    await asyncio.sleep(3)
    return "done"

async def main():
    try:
        # wait for task to finish within 1 second -> will timeout
        result = await asyncio.wait_for(task(), timeout=1.0)
        print("result:", result)
    except asyncio.TimeoutError:
        print("operation timed out")

if __name__ == "__main__":
    asyncio.run(main())
```

**Pattern:** For critical operations wrap with `wait_for`, or use `shield` to protect a subtask from cancellation.

---

### `asyncio.shield`

Protects an inner awaitable from cancellation triggered by outer `wait_for` or parent cancellation.

```python
# shield_example.py
import asyncio

async def protected():
    await asyncio.sleep(2)
    return "protected done"

async def main():
    try:
        # shield protects 'protected()' so wait_for won't cancel it,
        # but wait_for can still raise TimeoutError for the wrapper
        result = await asyncio.wait_for(asyncio.shield(protected()), timeout=1.0)
        print("Result:", result)
    except asyncio.TimeoutError:
        print("Timeout but protected coroutine keeps running in background")
        # optionally await it later
        res = await protected()
        print("Finally got:", res)

if __name__ == "__main__":
    asyncio.run(main())
```

---

### Timeout patterns

* Use `wait_for` for single awaitable timeouts.
* For multiple tasks: use `asyncio.wait` with timeout param to collect done/pending sets.
* Always handle `TimeoutError` and consider `return_exceptions=True` if using `gather`.

### Challenges (Timeouts & Cancellations)

1. Build a function that calls an unreliable remote operation wrapped with `wait_for`. On timeout, retry up to N times with backoff.
2. Create a supervisor coroutine that launches worker tasks and cancels them if a shutdown event occurs.
3. Demonstrate `shield`: run a long background operation that must survive a short `wait_for` timeout used by the starter.

---

# 7 — AsyncIO Streams (networking deeper)

## Streams recap

* `asyncio.start_server(handler, host, port)` gives you server; `handler(reader, writer)` per connection.
* `asyncio.open_connection(host, port)` creates `StreamReader, StreamWriter` client pair.

### Chat server (multi-client) example (simple)

```python
# chat_server.py
import asyncio

clients = set()  # set of writer objects

async def handle_client(reader, writer):
    addr = writer.get_extra_info("peername")
    print("Client connected:", addr)
    clients.add(writer)
    try:
        while True:
            # read a line; breaks on EOF
            data = await reader.readline()
            if not data:
                break
            msg = data.decode().rstrip()
            print(f"Received {msg} from {addr}")
            # broadcast to other clients
            for w in clients:
                if w is writer:
                    continue
                w.write(f"{addr}: {msg}\n".encode())
                await w.drain()
    except asyncio.CancelledError:
        pass
    finally:
        print("Client disconnected:", addr)
        clients.remove(writer)
        writer.close()
        await writer.wait_closed()

async def main():
    server = await asyncio.start_server(handle_client, '127.0.0.1', 9999)
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
```

Client: reuse `tcp_echo_client.py`, but loop to let user type messages.

---

### UDP — `DatagramProtocol` (connectionless)

UDP needs different API: `create_datagram_endpoint` with Protocol class.

**Example**

```python
# udp_server.py
import asyncio

class EchoServerProtocol:
    def connection_made(self, transport):
        self.transport = transport
    def datagram_received(self, data, addr):
        message = data.decode()
        print("Received", message, "from", addr)
        self.transport.sendto(data, addr)   # echo back

async def main():
    loop = asyncio.get_running_loop()
    # create UDP endpoint
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: EchoServerProtocol(),
        local_addr=("127.0.0.1", 9998)
    )
    try:
        await asyncio.Future()  # run forever
    finally:
        transport.close()

if __name__ == "__main__":
    asyncio.run(main())
```

---

### `StreamReader` with `async for`

You can iterate over lines using `async for line in reader:` pattern (Python 3.8+?).

**Example**

```python
# stream_reader_for.py
import asyncio

async def handle(reader, writer):
    async for line in reader:    # read until EOF
        print("Line:", line.decode().rstrip())
    writer.close()

async def main():
    server = await asyncio.start_server(handle, '127.0.0.1', 8881)
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
```

### Challenges (AsyncIO Streams)

1. Build a simple chat server + client (support multiple clients and broadcasting). Add nicknames.
2. Create a TCP file transfer: client sends filename, server streams file in chunks; client writes chunks to disk with `aiofiles`.
3. Build a UDP-based discovery service where clients broadcast a query and servers respond with a service description.

---

# 8 — AsyncIO + Context Managers & Iterators

## `async with` — async context managers

Used when entering/exiting requires `await` (e.g., files, network servers).

**Examples previously shown:** `async with aiofiles.open(...)`, `async with server:`.

### Custom async context manager

```python
# async_context.py
class AsyncCtx:
    async def __aenter__(self):
        print("enter: acquiring resource")
        await asyncio.sleep(0.1)
        return "resource"
    async def __aexit__(self, exc_type, exc, tb):
        print("exit: releasing resource")
        await asyncio.sleep(0.1)

async def main():
    async with AsyncCtx() as res:
        print("Using", res)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

## `async for` and custom async iterator

`async for` iterates over async iterators (objects implementing `__aiter__` and `__anext__`).

**Custom async iterator example**

```python
# async_iterator.py
class AsyncCounter:
    def __init__(self, n):
        self.n = n
    def __aiter__(self):
        self.i = 0
        return self
    async def __anext__(self):
        if self.i >= self.n:
            raise StopAsyncIteration
        await asyncio.sleep(0.2)
        v = self.i
        self.i += 1
        return v

async def main():
    async for num in AsyncCounter(3):
        print("Got", num)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

## Using `StreamReader` with `async for`

(Shown previously) — `async for line in reader` can read incoming lines until EOF.

---

### Challenges (Context Managers & Iterators)

1. Implement an async resource pool context manager (`async with pool.acquire()`) that yields a resource and returns it when `__aexit__` is called.
2. Write a custom async iterator that reads lines from an `asyncio.StreamReader` and yields parsed JSON objects.
3. Use `async with` and `TaskGroup` together to manage a group of tasks that share a resource from the pool above.

---

# Final notes, pitfalls & best practice hints (short)

* Avoid blocking calls inside coroutines — use `asyncio.to_thread` or `run_in_executor` if you must call blocking code.
* Use `asyncio.Queue` for most producer/consumer needs — simpler and less error-prone than Condition/Locks.
* Always handle `CancelledError` if the coroutine holds resources that must be cleaned.
* Prefer high-level streams API for networking unless you need socket-level control.
* Use `TaskGroup` (python 3.11+) for structured concurrency: it avoids many cancellation surprises.
* For file IO: `aiofiles` is convenient but it uses threads; for huge file throughput consider specialized strategies.

---

If you want now, I can:

* Walk **one challenge** with you step-by-step (pick which), **or**
* Provide full working implementations for all suggested challenges, one by one.

Which challenge would you like me to code & explain first (I’ll give fully commented code and run-through)?

