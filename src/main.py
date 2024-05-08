import time

import schedule
from loguru import logger

from src.utils.send_sertificates_data import send_certificates_data

if __name__ == "__main__":
    schedule.every().day.at("13:48").do(send_certificates_data)  # Укажите желаемое время отправки
    logger.info("Start a bot...")
    while True:
        schedule.run_pending()
        time.sleep(1)
