import requests
import os
from dotenv import load_dotenv
from src.utils.logger import get_logger

load_dotenv()
logger = get_logger(__name__)

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

def send_slack_message(message: str, level: str = "info") -> bool:
    """
    Slack으로 메시지 전송
    Args:
        message: 전송할 메시지
        level: info / warning / error
    """
    if not SLACK_WEBHOOK_URL:
        logger.warning("SLACK_WEBHOOK_URL 환경변수가 없습니다.")
        return False

    # 레벨별 이모지
    emoji = {
        "info": "✅",
        "warning": "⚠️",
        "error": "🚨"
    }.get(level, "✅")

    payload = {
        "text": f"{emoji} *[subway-pipeline]* {message}"
    }

    try:
        response = requests.post(SLACK_WEBHOOK_URL, json=payload, timeout=5)
        if response.status_code == 200:
            logger.info("Slack 알림 전송 완료")
            return True
        else:
            logger.error(f"Slack 전송 실패: {response.status_code}")
            return False

    except Exception as e:
        logger.error(f"Slack 전송 에러: {e}")
        return False


if __name__ == "__main__":
    send_slack_message("파이프라인 테스트 메시지입니다.", "info")
    send_slack_message("데이터 없음 경고입니다.", "warning")
    send_slack_message("수집 실패 에러입니다.", "error")