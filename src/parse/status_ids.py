from functools import lru_cache

import requests

from src.common.requests_data import cookies
from src.parse.headers import get_headers


@lru_cache(typed=True)
def get_status_ids() -> dict:
    response = requests.post('https://pub.fsa.gov.ru/nsi/api/status/get', cookies=cookies, headers=get_headers(), json={})
    id_dict = {}

    for item in response.json().get("items"):
        id_dict[item.get('id')] = item.get('name')

    if len(id_dict.keys()) == 0:
        raise ValueError("No id founded, maybe changed cookies or url")

    return id_dict
