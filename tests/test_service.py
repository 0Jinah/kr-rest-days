import pytest
from unittest.mock import AsyncMock, patch
from datetime import date
from kr_rest_days.service import HolidayService
from kr_rest_days.models import HolidayItem

# 가짜 공휴일 데이터 생성 유틸리티
def create_mock_holiday(locdate: int, name: str) -> HolidayItem:
    return HolidayItem(
        dateKind="01",
        dateName=name,
        isHoliday="Y",
        locdate=locdate,
        seq=1
    )

@pytest.fixture
def holiday_service():
    return HolidayService()

@pytest.mark.asyncio
async def test_get_holidays_from_to(holiday_service):
    """케이스 1: From & To (yyyy/mm) 기간 조회 테스트"""
    mock_data = [
        create_mock_holiday(20240101, "신정"),
        create_mock_holiday(20240209, "설날"),
        create_mock_holiday(20240301, "삼일절"),
    ]
    
    with patch.object(holiday_service.client, 'fetch_holidays', new_callable=AsyncMock) as mock_fetch:
        mock_fetch.return_value = mock_data
        
        # 2024/01 ~ 2024/02 기간 조회
        results = await holiday_service.get_holidays(from_date_str="2024/01", to_date_str="2024/02")
        
        assert len(results) == 2
        assert results[0].date_name == "신정"
        assert results[1].date_name == "설날"

@pytest.mark.asyncio
async def test_get_holidays_year_only(holiday_service):
    """케이스 4: 년도(yyyy)만 입력 시 해당 연도 전체 조회 테스트"""
    mock_data = [create_mock_holiday(20240505, "어린이날")]
    
    with patch.object(holiday_service.client, 'fetch_holidays', new_callable=AsyncMock) as mock_fetch:
        mock_fetch.return_value = mock_data
        
        results = await holiday_service.get_holidays(from_date_str="2024")
        
        assert len(results) == 1
        assert results[0].date_name == "어린이날"
        mock_fetch.assert_called_with(2024)

@pytest.mark.asyncio
async def test_get_holidays_to_only(holiday_service):
    """케이스 3: To (yyyy/mm)만 입력 시 해당 월만 조회 테스트"""
    mock_data = [create_mock_holiday(20241225, "크리스마스")]
    
    with patch.object(holiday_service.client, 'fetch_holidays', new_callable=AsyncMock) as mock_fetch:
        mock_fetch.return_value = mock_data
        
        results = await holiday_service.get_holidays(to_date_str="2024/12")
        
        assert len(results) == 1
        assert results[0].date_name == "크리스마스"
        # To만 있을 때는 해당 월(12)을 인자로 호출해야 함
        mock_fetch.assert_called_with(2024, 12)

@pytest.mark.asyncio
async def test_get_holidays_invalid_input(holiday_service):
    """잘못된 입력값 처리 테스트"""
    results = await holiday_service.get_holidays(from_date_str="abcd")
    assert results == []
