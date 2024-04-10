import requests

from src.common.requests_data import id_cookies
from src.parse.headers import get_headers


def get_id_dict() -> dict:
    response = requests.post('https://pub.fsa.gov.ru/nsi/api/status/get', cookies=id_cookies, headers=get_headers(), json={})
    id_dict = {}

    for item in response.json().get("items"):
        id_dict[item.get('id')] = item.get('name')

    if len(id_dict.keys()) == 0:
        raise ValueError("No id founded, maybe changed cookies or url")

    return id_dict
