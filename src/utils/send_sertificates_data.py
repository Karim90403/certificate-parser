import time

import pandas as pd
from common.config import settings
from loguru import logger
from parsing.certificates import get_certificates_data
from telegram import Bot
from utils.decorators import asyncio_run

bot = Bot(token=settings.project.token)  # Замените settings.telegram_bot_token на ваш токен


def create_exel_tables(certificates: list[dict]):
    certificates_data = [
        {
            "№ Сертификата": certificate.get("number"),
            "Ссылка на сертификат": certificate.get("url"),
            "Кому Выдан": certificate.get("applicant"),
            "Изготовитель": certificate.get("manufactorer"),
            "Когда выдан": certificate.get("date"),
            "Статус сертификата": certificate.get("status"),
            "Страны лабораторий": ", ".join(
                set([lab.get("country") for lab in certificate.get("testing_labs", {}).get("testing_labs", [])])
            ),
        }
        for certificate in certificates
    ]

    df = pd.DataFrame(certificates_data)
    df.to_excel(f"{settings.project.product_name}.xlsx", index=False)


@asyncio_run
async def send_certificates_data():
    try:
        certificates: list[dict] = get_certificates_data()
        create_exel_tables(certificates)
        updates = await bot.get_updates()
        for update in updates:
            chat_id = update.message.chat_id
            await bot.send_document(chat_id=chat_id, document=f"{settings.project.product_name}.xlsx")
            time.sleep(1)  # Пауза между отправкой сообщений
        logger.info("Successfully ended sending data")
    except Exception as e:
        logger.opt(exception=e).error(e)


if __name__ == "__main__":
    send_certificates_data()
