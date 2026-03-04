from datetime import date, datetime
from typing import List, Optional
from loguru import logger
from .client import HolidayClient
from .models import HolidayItem

class HolidayService:
    def __init__(self):
        self.client = HolidayClient()

    async def get_holidays(
        self, 
        from_date_str: Optional[str] = None, 
        to_date_str: Optional[str] = None
    ) -> List[HolidayItem]:
        """
        사용자 입력 조건에 따라 공휴일 목록을 반환합니다.
        
        조회 로직:
        1. From & To (yyyy/mm): 해당 기간 내 공휴일 조회
        2. From only (yyyy/mm): 해당 년월부터 최신 데이터(현재 연도 말)까지 조회
        3. To only (yyyy/mm): 해당 년월의 공휴일만 조회
        4. Year only (yyyy): 해당 연도의 전체 데이터 조회
        """
        
        # 1. 입력 값 정규화 및 분석
        from_dt = self._parse_date_input(from_date_str)
        to_dt = self._parse_date_input(to_date_str)
        
        # To가 연도(yyyy)만 입력된 경우, 해당 연도의 말일로 설정하여 기간 검색에 포함되게 함
        if to_date_str and len(to_date_str.strip()) == 4 and to_dt:
            to_dt = to_dt.replace(month=12, day=31)

        logger.info(f"조회 요청 분석: from={from_dt}, to={to_dt}")

        all_holidays: List[HolidayItem] = []

        # 케이스 1: From & To 모두 입력된 경우 (최우선 순위)
        if from_dt and to_dt:
            # 시작 연도부터 종료 연도까지 모두 조회
            for year in range(from_dt.year, to_dt.year + 1):
                year_holidays = await self.client.fetch_holidays(year)
                all_holidays.extend(year_holidays)
            
            # 기간 필터링 (from_dt <= holiday <= to_dt)
            return [
                h for h in all_holidays 
                if from_dt.date() <= h.formatted_date <= to_dt.date()
            ]

        # 케이스 4: From 또는 To 중 하나만 연도(yyyy)로 입력된 경우
        if (from_date_str and len(from_date_str.strip()) == 4) or (to_date_str and len(to_date_str.strip()) == 4):
            year = int(from_date_str) if from_date_str and len(from_date_str.strip()) == 4 else int(to_date_str)
            return await self.client.fetch_holidays(year)

        # 케이스 2: From만 입력된 경우 (From ~ 현재 연도 말까지)
        if from_dt and not to_dt:
            current_year = datetime.now().year
            for year in range(from_dt.year, current_year + 1):
                year_holidays = await self.client.fetch_holidays(year)
                all_holidays.extend(year_holidays)
            
            return [h for h in all_holidays if h.formatted_date >= from_dt.date()]

        # 케이스 3: To만 입력된 경우 (해당 년월만 조회)
        if not from_dt and to_dt:
            return await self.client.fetch_holidays(to_dt.year, to_dt.month)

        return []

    def _parse_date_input(self, date_str: Optional[str]) -> Optional[datetime]:
        """yyyy/mm 또는 yyyy 형식의 문자열을 datetime 객체로 변환"""
        if not date_str:
            return None
        
        date_str = date_str.strip()
        try:
            if len(date_str) == 4:  # yyyy
                return datetime.strptime(date_str, "%Y")
            elif "/" in date_str:  # yyyy/mm
                return datetime.strptime(date_str, "%Y/%m")
            elif "-" in date_str:  # yyyy-mm
                return datetime.strptime(date_str, "%Y-%m")
            else:
                return None
        except ValueError:
            logger.warning(f"잘못된 날짜 형식 입력: {date_str}")
            return None
