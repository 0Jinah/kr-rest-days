import httpx
from loguru import logger
from typing import List, Optional
from .models import HolidayApiResponse, HolidayItem
from .config import settings

class HolidayClient:
    def __init__(self):
        self.endpoint = settings.API_ENDPOINT
        self.api_key = settings.DATA_GO_API_KEY

    async def fetch_holidays(self, year: int, month: Optional[int] = None) -> List[HolidayItem]:
        """
        공공데이터 API를 호출하여 공휴일 정보를 가져옵니다.
        """
        params = {
            "ServiceKey": self.api_key,
            "solYear": year,
            "_type": "json",
            "numOfRows": 100,  # 한 번에 충분히 가져옴
        }
        if month:
            params["solMonth"] = f"{month:02d}"

        async with httpx.AsyncClient() as client:
            try:
                logger.info(f"API 호출: year={year}, month={month}")
                response = await client.get(self.endpoint, params=params)
                response.raise_for_status()
                
                data = response.json()
                api_response = HolidayApiResponse.model_validate(data)
                
                if api_response.response.header.result_code != "00":
                    logger.error(f"API 에러: {api_response.response.header.result_msg}")
                    return []

                items_obj = api_response.response.body.items
                if not items_obj or not items_obj.item:
                    return []

                # 단일 아이템일 경우와 리스트일 경우 대응
                if isinstance(items_obj.item, list):
                    return items_obj.item
                else:
                    return [items_obj.item]

            except Exception as e:
                logger.exception(f"API 호출 중 예외 발생: {e}")
                return []
