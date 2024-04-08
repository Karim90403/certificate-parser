from src.common.logger import init_logging
from src.process.extract import run_web_extractor

if __name__ == "__main__":
    init_logging()
    run_web_extractor()
