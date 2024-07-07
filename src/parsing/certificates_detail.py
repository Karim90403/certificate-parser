import time

import requests
from common.config import settings
from common.headers import get_headers
from loguru import logger
from parsing.certificates_multi import MultiRequest


def safe_get_response(certificate_id: str):
    response = requests.get(
        f"https://pub.fsa.gov.ru/api/v1/rss/common/certificates/{certificate_id}",
        cookies=settings.project.cookies,
        headers=get_headers(),
    )
    if response.status_code != 200:
        print(f"{response.status_code}, reload process")
        time.sleep(2)
        return safe_get_response(certificate_id)
    return response.json()


def get_certificate_detail(certificate_id: str) -> dict:
    response_dict = safe_get_response(certificate_id)

    logger.info(f"Parsing certificate: {certificate_id}...")
    time.sleep(0.5)

    return dict(
        identifications=[
            dict(
                name=identification.get("name"),
                type=identification.get("type"),
                codes=MultiRequest.get_tnved_codes(identification.get("idTnveds")),
                description=identification.get("description"),
            )
            for identification in response_dict.get("product", {}).get("identifications", [])
        ],
        testing_labs=[
            dict(
                name=lab.get("fullName"),
                country=MultiRequest.get_country(lab.get("idAccredPlace")),
            )
            for lab in response_dict.get("testingLabs", [])
        ],
        certification_authority_name=response_dict.get("certificationAuthority", {}).get("fullName"),
    )
