import asyncio
import time

import schedule
from loguru import logger

from common.config import settings
from src.utils.send_sertificates_data import send_certificates_data

if __name__ == "__main__":
    if settings.project.debug:
        asyncio.get_event_loop().run_until_complete(send_certificates_data())
    else:
        schedule.every().day.at("13:00").do(send_certificates_data)  # Укажите желаемое время отправки
        logger.info("Start a bot...")
        while True:
            schedule.run_pending()
            time.sleep(1)
