import json

from src.common.logger import init_logging
from src.parse.certificates import get_certificates_data

if __name__ == "__main__":
    init_logging()
    data = get_certificates_data()
    with open("file.json", "w") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

