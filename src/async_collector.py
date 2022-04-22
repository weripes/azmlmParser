from collect_user_data import collect_user_data
from tqdm import tqdm

import asyncio
import aiohttp


class AsyncCollector:

    def __init__(self):
        self.users_data = [] # Тут будут храниться данные о пользователях
        self.url = 'http://azmlm.com/users{}/' # Сюда потом удробно помещать число через format
        self.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko)'}

    # Принимает число которое подставляет в
    # ссылку и собирает данные о пользователе
    async def __collect_page_data(self, session, user_id: int):
        url = self.url.format(user_id)
        async with session.get(url=url, headers=self.headers) as response:
            html = await response.content.read()
            user_data = collect_user_data(html=html)
            if user_data:
                self.users_data.append(user_data)

    async def __create_tasks(self, from_user_id: int, to_user_id: int) -> list | list:
        # Создание сессии
        async with aiohttp.ClientSession() as session:
            tasks = []
            # Тут создается список заданий для asyncio, выполнить
            # функции __collect_page_data с задаными параметрами
            for user_id in range(from_user_id, to_user_id+1):
                task = asyncio.create_task(self.__collect_page_data(session=session, user_id=user_id))
                tasks.append(task)

            # Это progress bar (tqdm)
            [await f for f in tqdm(asyncio.as_completed(tasks), total=len(tasks))]
            return tasks

    def start_collector(self, from_user_id: int, to_user_id: int) -> list:
        loop = asyncio.get_event_loop()
        loop = loop.run_until_complete(
            self.__create_tasks(
                from_user_id=from_user_id,
                to_user_id=to_user_id
            )
        )
        """
        self.users_data сделан просто для удобного общения между
        функциями, каждая task'а сохраняет сюда данные одного
        пользователя. После окончания всех task'ов, возвращаем
        полный список и очищаем self.users_data 
        """
        users_data = self.users_data
        self.users_data = []
        return users_data