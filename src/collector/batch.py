import requests
import os
import json
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

DATA_GO_API_KEY = os.getenv("DATA_GO_API_KEY")

def fetch_subway_notices():
    """지하철 알림정보 수집"""
    base_url = "https://apis.data.go.kr/B553766/ntce/getNtceList"
    request_url = f"{base_url}?serviceKey={DATA_GO_API_KEY}"

    params = {
        'dataType': 'JSON',
        'pageNo': 1,
        'numOfRows': 100,
    }

    try:
        print(f"[{datetime.now()}] 알림정보 수집 시작")
        response = requests.get(request_url, params=params, timeout=10)

        if response.status_code == 200:
            data = response.json()
            items = data.get('response', {}).get('body', {}).get('items', {})

            # items가 딕셔너리면 item 꺼내기
            if isinstance(items, dict):
                result = items.get('item', [])
            else:
                result = items

            # 1건이면 리스트로 감싸기
            if isinstance(result, dict):
                result = [result]

            # 수집 시간 추가
            for item in result:
                item['collected_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if len(result) > 0:
                print(f"[{datetime.now()}] 알림정보 {len(result)}건 수집 완료")
            else:
                print(f"[{datetime.now()}] 수집된 알림정보 없음")
            return result

        else:
            print(f"실패: 상태코드 {response.status_code}")
            return []

    except Exception as e:
        print(f"에러 발생: {e}")
        return []


if __name__ == "__main__":
    notices = fetch_subway_notices()
    if notices:
        print(json.dumps(notices[0], ensure_ascii=False, indent=2))
    else:
        print("데이터 없음")