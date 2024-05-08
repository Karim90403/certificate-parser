from typing import List

import requests
from loguru import logger

from src.common.config import settings
from src.common.headers import get_headers
from src.parsing.certificates_detail import get_certificate_detail
from src.parsing.status_ids import get_status_ids


def get_certificates_data(product_name) -> List[dict]:
    query = {
        "size": 100,
        "page": 0,
        "filter": {
            "columnsSearch": [
                {
                    "column": "productFullName",
                    "search": product_name,
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

    res = requests.post(
        "https://pub.fsa.gov.ru/api/v1/rss/common/certificates/get",
        cookies=settings.project.cookies,
        headers=get_headers(),
        json=query,
    )
    response_dict = res.json()

    if response_dict.get("total") == 0:
        raise ValueError("No certificates in response")

    logger.info(f"Starting parsing certificates with product_name = {product_name}, total = {response_dict.get('total')}...")

    return [
        dict(
            url=f"https://pub.fsa.gov.ru/rss/certificate/view/{item.get('id')}/baseInfo",
            status=get_status_ids()[item.get("idStatus")],
            number=item.get("number"),
            date=item.get("date"),
            end_date=item.get("endDate"),
            applicant=item.get("applicantName"),
            manufactorer=item.get("manufacterName"),
            indetification_name=item.get("productIdentificationName"),
            testing_labs=get_certificate_detail(item.get("id")),
        ) for item in response_dict.get("items")
    ]
