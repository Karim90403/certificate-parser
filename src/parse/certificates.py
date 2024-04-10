from typing import List

import requests

from src.common.requests_data import search_query, search_cookies
from src.parse.headers import get_headers
from src.parse.ids import get_id_dict


def get_certificates_data() -> List[dict]:
    res = requests.post(
        'https://pub.fsa.gov.ru/api/v1/rss/common/certificates/get',
        cookies=search_cookies,
        headers=get_headers(),
        json=search_query,
    )
    response_dict = res.json()

    if response_dict.get('total') == 0:
        raise ValueError('No certificates in response')

    # TODO: check more value in response
    id_dict = get_id_dict()

    return [
        dict(
            url=f"https://pub.fsa.gov.ru/rss/certificate/view/{item.get('id')}/baseInfo",
            status=id_dict[item.get('idStatus')],
            number=item.get('number'),
            date=item.get('date'),
            end_date=item.get('endDate'),
            applicant=item.get('applicantName'),
            indetification_name=item.get('productIdentificationName')
        ) for item in response_dict.get('items')
    ]