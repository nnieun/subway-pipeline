import requests
import os
import json
from dotenv import load_dotenv
from datetime import datetime
from src.utils.logger import get_logger

load_dotenv()

logger = get_logger(__name__)
SEOUL_API_KEY = os.getenv("SEOUL_API_KEY")

STATIONS = ["강남", "홍대입구", "신촌", "잠실", "건대입구"]

def fetch_realtime_arrival(station_name: str) -> list:
    """특정 역의 실시간 도착 정보 수집"""
    url = f"http://swopenapi.seoul.go.kr/api/subway/{SEOUL_API_KEY}/json/realtimeStationArrival/0/10/{station_name}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        items = data.get('realtimeArrivalList', [])

        for item in items:
            item['collected_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        logger.info(f"{station_name} {len(items)}건 수집 완료")
        return items

    except Exception as e:
        logger.error(f"{station_name} 수집 실패: {e}")
        return []

def collect_all_stations() -> list:
    """전체 역 수집"""
    results = []
    for station in STATIONS:
        items = fetch_realtime_arrival(station)
        results.extend(items)
    return results


if __name__ == "__main__":
    results = collect_all_stations()
    if results:
        logger.info(json.dumps(results[0], ensure_ascii=False, indent=2))
    else:
        logger.warning("데이터 없음")