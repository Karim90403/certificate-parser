from functools import lru_cache

import requests
from loguru import logger


@lru_cache(typed=True)
def get_headers():
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Origin': 'https://pub.fsa.gov.ru',
        'Pragma': 'no-cache',
        'Referer': 'https://pub.fsa.gov.ru/rss/certificate',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
        'lkId': '',
        'orgId': '',
    }

    res = requests.post('https://pub.fsa.gov.ru/login', headers=headers,
                        json={'username': 'anonymous', 'password': 'hrgesf7HDR67Bd', })
    headers['Authorization'] = res.headers.get('Authorization')

    logger.info('Successfully logged in!')

    return headers
