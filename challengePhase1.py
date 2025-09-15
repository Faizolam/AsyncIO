import requests
import asyncio
import time


# def fetchSync():
#     results = []
#     for i in range(1, 5):
#         response = requests.get(f'https://jsonplaceholder.typicode.com/todos/{i}')
#         results.append(response.json())  # Parse and store JSON result
#         time.sleep(2)
#     return results

# fetchSync()


# def fetchSync():
#     for i in range(1 , 5):
#         response = requests.get(f'https://jsonplaceholder.typicode.com/todos/{i}')
#         print(response.status_code)
#         print(response.json())
#         time.sleep(1)
#     # return response.text


# fetchSync()
# ---------------------------------------------------------------------

# import time
# async def fetchAsync():
#     start = time.time()
#     for i in range(1, 5):
#         response = requests.get(f'https://jsonplaceholder.typicode.com/todos/{i}')
#         print( response.json())
#         print( response.status_code)
#         await asyncio.sleep(1)
#     end = time.time()
#     print(f"Took {end - start:.2f} seconds")
    

# asyncio.run(fetchAsync())

# --------------------------------------------------

import time
def fetch_url(url):
    print(f"Fetching {url}...")
    time.sleep(2)   # Simulating network delay
    print(f"Done: {url}")

def main():
    start = time.time()

    fetch_url("https://example.com/1")
    fetch_url("https://example.com/2")
    fetch_url("https://example.com/3")

    end = time.time()
    print(f"Took {end - start:.2f} seconds \n")

print("===================Sync===================")
main()

## ----------------------------------------------------------------
import asyncio
async def fetch_url(url):
    print(f"Fetching {url}...")
    await asyncio.sleep(2)   # Non-blocking delay
    print(f"Done: {url}")

async def main():
    start = asyncio.get_running_loop().time()

    await asyncio.gather(
        fetch_url("https://example.com/1"),
        fetch_url("https://example.com/2"),
        fetch_url("https://example.com/3")
    )

    end = asyncio.get_running_loop().time()
    print(f"Took {end - start:.2f} seconds")

print("===================Async===================")
asyncio.run(main())

