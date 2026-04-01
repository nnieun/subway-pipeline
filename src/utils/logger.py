import logging
import os
from datetime import datetime


def get_logger(name: str) -> logging.Logger:

    logger = logging.getLogger(name)

    # 이미 핸들러가 있으면 중복 방지
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    # 로그 폴더 생성
    os.makedirs("logs", exist_ok=True)

    # 포맷 설정
    formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s] %(name)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # 콘솔 출력
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # 파일 저장 (날짜별)
    today = datetime.now().strftime("%Y-%m-%d")
    file_handler = logging.FileHandler(
        f"logs/{today}.log",
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger