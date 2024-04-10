from functools import lru_cache

import requests
from loguru import logger

from src.common.config import settings
from src.common.headers import get_headers


@lru_cache(typed=True)
def get_status_ids() -> dict:
    response = requests.post("https://pub.fsa.gov.ru/nsi/api/status/get", cookies=settings.project.cookies,
                             headers=get_headers(), json={})
    id_dict = {}

    for item in response.json().get("items"):
        id_dict[item.get("id")] = item.get("name")

    if len(id_dict.keys()) == 0:
        logger.error("No id's were found")
        exit()

    return id_dict
