import requests
from tqdm import tqdm

from collect_user_data import collect_user_data


def sync_collector(from_user_id: int, to_user_id: int) -> list:

    HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko)'}
    users_data = []
    # tdqm это progress bar
    for user_id in tqdm(range(from_user_id, to_user_id+1)):
        response = requests.get(f'http://azmlm.com/users{user_id}/', headers=HEADERS)

        user_data = collect_user_data(html=response.content)
        if user_data:
            users_data.append(user_data)

    return users_data