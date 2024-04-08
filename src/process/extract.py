import json

import requests

from src.common.config import settings

cookies = {
    '_ym_uid': '1712313037677828500',
    '_ym_d': '1712313037',
    '_ym_isad': '2',
    'JSESSIONID': 'DC362F4A51390945B72B0EABA3824421',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJpc3MiOiIwMjI3YjIyNi03YzhiLTQzOTQtYjc4OS02ZGM0MTUxMGUzOGEiLCJzdWIiOiJhbm9ueW1vdXMiLCJleHAiOjE3MTI2MzEyNjB9.tg-QDkn5hCLOhnLXOI1Bg8v6CqjpZRsj8znnxD-PUEB6FhIBk9t2Gai0k6HKN1QjJINY18bxGte9YEHMGXGDHA',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    # 'Cookie': '_ym_uid=1712313037677828500; _ym_d=1712313037; _ym_isad=2; JSESSIONID=DC362F4A51390945B72B0EABA3824421',
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

json_data = {
    'size': 10,
    'page': 0,
    'filter': {
        'regDate': {
            'minDate': '',
            'maxDate': '',
        },
        'endDate': {
            'minDate': '',
            'maxDate': '',
        },
        'columnsSearch': [
            {
                'column': 'productFullName',
                'search': settings.project.column_search,
            },
        ],
    },
    'columnsSort': [
        {
            'column': 'date',
            'sort': 'DESC',
        },
    ],
}


def run_web_extractor():
    response = requests.post(
        'https://pub.fsa.gov.ru/api/v1/rss/common/certificates/get',
        cookies=cookies,
        headers=headers,
        json=json_data,
    )

    print(response.status_code)
    print(response.text)
