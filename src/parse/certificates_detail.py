from typing import List

import requests

from src.common.requests_data import cookies
from src.parse.certificates_multi import MultiRequest
from src.parse.headers import get_headers
from src.parse.status_ids import get_status_ids


def get_certificate_detail(certificate_id: str) -> dict:
    headers = get_headers()
    headers["Referer"] = f"https://pub.fsa.gov.ru/rss/certificate/view/{certificate_id}/product"

    response = requests.get(f"https://pub.fsa.gov.ru/api/v1/rss/common/certificates/{certificate_id}", cookies=cookies,
                            headers=get_headers())
    response_dict = response.json()

    return dict(
        identifications=[
            dict(
                name=identification.get("name"),
                type=identification.get("type"),
                codes=MultiRequest.get_tnved_codes(certificate_id, identification.get("idTnveds")),
                description=identification.get("description"),

            ) for identification in response_dict.get('product', {}).get('identifications', [])],
        testing_labs=[
            dict(
                name=lab.get("fullName"),
                country=MultiRequest.get_country(certificate_id, lab.get("idAccredPlace")),
            )
            for lab in response_dict.get('testingLabs', [])],
        certification_authority_name=response_dict.get('certificationAuthority', {}).get("fullName")
    )
