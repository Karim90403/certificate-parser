import json
import time
from json import JSONDecodeError

from telegram import Bot
from loguru import logger
from src.common.config import settings
from src.parsing.certificates import get_certificates_data
from src.utils.decorators import asyncio_run

bot = Bot(token=settings.project.token)  # Замените settings.telegram_bot_token на ваш токен


def get_actual_certificates(product_name: str):
    certificates: list[dict] = get_certificates_data(product_name)
    with open(f"{product_name}.json", "r") as file:
        try:
            old_certificates = json.load(file)
        except JSONDecodeError:
            old_certificates = []
        actual_certificates = [certificate for certificate in certificates if certificate not in old_certificates]
        if certificates:
            with open(f"{product_name}.json", "w") as file:
                json.dump(certificates, file, ensure_ascii=False, indent=2)
        return actual_certificates


@asyncio_run
async def send_certificates_data():
    try:
        for product_name in settings.project.product_names_list:
            certificates = get_actual_certificates(product_name)
            messages: list[str] = []
            for certificate in certificates:
                messages.append(
                    f"№ Сертификата: {certificate.get('number')}\n"
                    f"Ссылка на сертификат: {certificate.get('url')}\n"
                    f"Устройство: {certificate.get('indetification_name')}\n"
                    f"Кому Выдан: {certificate.get('applicant')}\n"
                    f"Изготовитель: {certificate.get('manufactorer')}\n"
                    f"Когда выдан: {certificate.get('date')}\n"
                    f"Статус сертификата: {certificate.get('status')}\n"
                    f"Страны лабораторий: {', '.join(set([lab.get('country') for lab in certificate.get('testing_labs', {}).get('testing_labs', [])]))}"
                )

            updates = await bot.get_updates()
            for message in messages:
                for update in updates:
                    chat_id = update.message.chat_id
                    await bot.send_message(chat_id=chat_id, text=message)
                    time.sleep(1)  # Пауза между отправкой сообщений
            time.sleep(1)  # Пауза между отправкой сообщений
        logger.info("Successfully ended sending data")
    except Exception as e:
        logger.opt(exception=e).error(e)


if __name__ == "__main__":
    send_certificates_data()
