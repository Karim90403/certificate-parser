import requests
from loguru import logger

from src.common.config import settings
from src.parsing.certificates_multi import MultiRequest
from src.common.headers import get_headers


def get_certificate_detail(certificate_id: str) -> dict:
    response = requests.get(f"https://pub.fsa.gov.ru/api/v1/rss/common/certificates/{certificate_id}",
                            cookies=settings.project.cookies,
                            headers=get_headers())
    response_dict = response.json()

    logger.info(f"Parsing certificate: {certificate_id}...")

    return dict(
        identifications=[
            dict(
                name=identification.get("name"),
                type=identification.get("type"),
                codes=MultiRequest.get_tnved_codes(identification.get("idTnveds")),
                description=identification.get("description"),

            ) for identification in response_dict.get("product", {}).get("identifications", [])],
        testing_labs=[
            dict(
                name=lab.get("fullName"),
                country=MultiRequest.get_country(lab.get("idAccredPlace")),
            )
            for lab in response_dict.get("testingLabs", [])],
        certification_authority_name=response_dict.get("certificationAuthority", {}).get("fullName")
    )
