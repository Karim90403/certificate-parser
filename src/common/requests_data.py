from src.common.config import settings

# Search

search_cookies = {
    '_ym_uid': '1712313037677828500',
    '_ym_d': '1712313037',
    '_ym_isad': '2',
    'JSESSIONID': 'DC362F4A51390945B72B0EABA3824421',
}

search_query = {
    'size': 100,
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

# Extract id table
id_cookies = {
    '_ym_uid': '1712313037677828500',
    '_ym_d': '1712313037',
    '_ym_isad': '2',
    'JSESSIONID': 'node071ofy1mx7fc99nlj1m82xofw125117.node0',
}