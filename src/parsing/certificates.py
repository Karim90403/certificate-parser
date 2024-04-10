from typing import List

import requests
from loguru import logger

from src.common.config import settings
from src.common.headers import get_headers
from src.parsing.certificates_detail import get_certificate_detail
from src.parsing.status_ids import get_status_ids

search_query = {
    "size": 100,
    "page": 0,
    "filter": {
        "columnsSearch": [
            {
                "column": "productFullName",
                "search": settings.project.column_search,
            },
        ],
    },
    "columnsSort": [
        {
            "column": "date",
            "sort": "DESC",
        },
    ],
}


def get_certificates_data() -> List[dict]:
    res = requests.post(
        "https://pub.fsa.gov.ru/api/v1/rss/common/certificates/get",
        cookies=settings.project.cookies,
        headers=get_headers(),
        json=search_query,
    )
    response_dict = res.json()

    if response_dict.get("total") == 0:
        raise ValueError("No certificates in response")

    logger.info(f"Starting parsing {response_dict.get('total')} certificates...")

    return [
        dict(
            url=f"https://pub.fsa.gov.ru/rss/certificate/view/{item.get('id')}/baseInfo",
            status=get_status_ids()[item.get("idStatus")],
            number=item.get("number"),
            date=item.get("date"),
            end_date=item.get("endDate"),
            applicant=item.get("applicantName"),
            indetification_name=item.get("productIdentificationName"),
            testing_labs=get_certificate_detail(item.get("id")),
        ) for item in response_dict.get("items")
    ]
