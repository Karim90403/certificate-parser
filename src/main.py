import json
from loguru import logger

from src.common.logger import init_logging
from src.parsing.certificates import get_certificates_data

if __name__ == "__main__":
    init_logging()
    try:
        data = get_certificates_data()
        with open("file.json", "w") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.opt(exception=e).error(e)

