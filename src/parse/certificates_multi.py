import requests

from src.common.requests_data import cookies
from src.parse.headers import get_headers


class MultiRequest:
    @staticmethod
    def get_services_multi(certificate_id: str, category: str, ids: list) -> dict:
        headers = get_headers()
        headers["Origin"] = "https://pub.fsa.gov.ru"
        headers["Referer"] = f"https://pub.fsa.gov.ru/rss/certificate/view/{certificate_id}/testingLabs"

        query = {'items': {category: [{"id": ids}]}}
        response = requests.post('https://pub.fsa.gov.ru/nsi/api/multi', cookies=cookies, headers=headers, json=query)
        return response.json()

    @classmethod
    def get_tnved_codes(cls, certificate_id: str, tnveds_ids: list[str]) -> list[str]:
        return [tnved.get("code", "") + " " + tnved.get("name", "") for tnved in
                cls.get_services_multi(certificate_id=certificate_id, category="tnved", ids=tnveds_ids).get("tnved")]

    @classmethod
    def get_country(cls, certificate_id: str, country_id: str):
        res = cls.get_services_multi(certificate_id=certificate_id, category="oksm", ids=[country_id]).get("oksm")
        if len(res) == 1:
            return res[0].get("shortName")
        else:
            return None
