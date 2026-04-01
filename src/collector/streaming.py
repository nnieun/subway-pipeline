import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

SEOUL_API_KEY = os.getenv("SEOUL_API_KEY")

# 수집할 역 목록 (2호선 주요역만 타겟팅)
STATIONS = ["강남", "홍대입구", "신촌", "잠실", "건대입구"]

def fetch_realtime_arrival(station_name: str) -> dict:
    """특정 역의 실시간 도착 정보 수집"""
    url = f"http://swopenapi.seoul.go.kr/api/subway/{SEOUL_API_KEY}/json/realtimeStationArrival/0/10/{station_name}"
    
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        data = res.json()
        
        # 수집 시간 추가
        data["collected_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data["station_name"] = station_name
        
        print(f"[{data['collected_at']}] {station_name} 수집 완료 - {len(data.get('realtimeArrivalList', []))}건")
        return data
    
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] {station_name} 수집 실패: {e}")
        return {}

def collect_all_stations() -> list:
    """전체 역 수집"""
    results = []
    for station in STATIONS:
        data = fetch_realtime_arrival(station)
        if data:
            results.append(data)
    return results

if __name__ == "__main__":
    results = collect_all_stations()
    print(json.dumps(results, ensure_ascii=False, indent=2))