import asyncio
import requests
import random



url = "https://httpbin.org/delay/1"

class AsyncRequester:
    def __init__(self):
        self.max_thread = 5
        self.semaphore = asyncio.Semaphore(self.max_thread)  # Ограничение до 5 потоков одновременно
        self.session = requests.Session()
        self.tasks_ids = dict()
        self.lock = asyncio.Lock() 

    def GetAsync(self,params):
        return self.session.get(
            url=params.get('url'),
            data=params.get('data','')
            )

    def SetOptions(self):
        self.session.cookies.set('cookie_name', 'cookie_value')

    async def SetNumberTask(self,i):
        async with self.lock:
            for thread_id in range(1, self.max_thread + 1):
                if thread_id not in self.tasks_ids:
                    self.tasks_ids[thread_id] = i
                    return thread_id
            return -10


    async def UnsetNumberTasks(self,thread_id):
        async with self.lock:
            del self.tasks_ids[thread_id]

        
    async def my_async_function(self,i):
        async with self.semaphore:
            thread_id = await self.SetNumberTask(i)

            random_number = random.randint(0, 5)

            print(f"[{thread_id} {i}] Start")
            loop = asyncio.get_event_loop()
            params = {
                "data": f"test{i}",
                "url": f"https://httpbin.org/delay/{random_number}",
            } 
            
            response = await loop.run_in_executor(None, self.GetAsync, params)
            print(f"[{thread_id} {i}] End {random_number}")
            await self.UnsetNumberTasks(thread_id)

    async def run(self):
        tasks = [self.my_async_function(i) for i in range(30)]
        await asyncio.gather(*tasks)

# Запуск асинхронной функции
async def main():
    requester = AsyncRequester()
    requester.SetOptions()
    await requester.run()

asyncio.run(main())

