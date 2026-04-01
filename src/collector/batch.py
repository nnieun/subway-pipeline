import requests
import os
import json
from dotenv import load_dotenv
from datetime import datetime
from src.utils.logger import get_logger

load_dotenv()

logger = get_logger(__name__)
DATA_GO_API_KEY = os.getenv("DATA_GO_API_KEY")

def fetch_subway_notices() -> list:
    """지하철 알림정보 수집"""
    base_url = "https://apis.data.go.kr/B553766/ntce/getNtceList"
    request_url = f"{base_url}?serviceKey={DATA_GO_API_KEY}"

    params = {
        'dataType': 'JSON',
        'pageNo': 1,
        'numOfRows': 100,
    }

    try:
        logger.info("알림정보 수집 시작")
        response = requests.get(request_url, params=params, timeout=10)

        if response.status_code == 200:
            data = response.json()
            items = data.get('response', {}).get('body', {}).get('items', {})

            if isinstance(items, dict):
                result = items.get('item', [])
            else:
                result = items

            if isinstance(result, dict):
                result = [result]

            for item in result:
                item['collected_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if len(result) > 0:
                logger.info(f"알림정보 {len(result)}건 수집 완료")
            else:
                logger.warning("수집된 알림정보 없음")
            return result

        else:
            logger.error(f"수집 실패: 상태코드 {response.status_code}")
            return []

    except Exception as e:
        logger.error(f"에러 발생: {e}")
        return []


if __name__ == "__main__":
    notices = fetch_subway_notices()
    if notices:
        logger.info(json.dumps(notices[0], ensure_ascii=False, indent=2))