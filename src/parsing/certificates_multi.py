import time
from functools import lru_cache

import requests
from common.config import settings
from common.headers import get_headers
from loguru import logger


class MultiRequest:
    @staticmethod
    def _get_multi(category: str, ids: list) -> dict:
        query = {"items": {category: [{"id": ids}]}}
        time.sleep(1)
        response = requests.post(
            "https://pub.fsa.gov.ru/nsi/api/multi", cookies=settings.project.cookies, headers=get_headers(), json=query
        )
        if response.status_code == 503:
            logger.error(response.text)
            raise
        return response.json()

    @classmethod
    def get_tnved_codes(cls, tnveds_ids: list[str]) -> list[str]:
        return [
            tnved.get("code", "") + " " + tnved.get("name", "")
            for tnved in cls._get_multi(category="tnved", ids=tnveds_ids).get("tnved", [])
        ]

    @classmethod
    @lru_cache
    def get_country(cls, country_id: str):
        res = cls._get_multi(category="oksm", ids=[country_id]).get("oksm")
        if len(res) == 1:
            return res[0].get("shortName")
        else:
            logger.warning("Invalid country!")
            return None
