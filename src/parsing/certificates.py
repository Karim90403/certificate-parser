from typing import List

import requests
from common.config import settings
from common.headers import get_headers
from loguru import logger
from parsing.certificates_detail import get_certificate_detail
from parsing.status_ids import get_status_ids


def get_certificates_data() -> List[dict]:
    query = {
        "size": settings.project.max_response_size,
        "page": 0,
        "filter": {
            "idGroupEEU": settings.project.searched_id,
        },
        "columnsSort": [
            {
                "column": "date",
                "sort": "DESC",
            },
        ],
    }
    # Максимальный размер скачиваемых данных и группы по которым мы ищем задаются в среде приложения

    res = requests.post(
        "https://pub.fsa.gov.ru/api/v1/rss/common/certificates/get",
        cookies=settings.project.cookies,
        headers=get_headers(),
        json=query,
    )
    response_dict = res.json()

    if response_dict.get("total") == 0:
        raise ValueError("No certificates in response")

    logger.info(
        f"Starting parsing certificates with product_name = {settings.project.product_name}, total = {response_dict.get('total')}..."
    )

    return [
        dict(
            url=f"https://pub.fsa.gov.ru/rss/certificate/view/{item.get('id')}/baseInfo",
            status=get_status_ids().get(item.get("idStatus"), "Invalid id"),
            number=item.get("number"),
            date=item.get("date"),
            end_date=item.get("endDate"),
            applicant=item.get("applicantName"),
            manufactorer=item.get("manufacterName"),
            indetification_name=item.get("productIdentificationName"),
            testing_labs=get_certificate_detail(item.get("id")),
        )
        for item in response_dict.get("items")
    ]
