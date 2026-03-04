from pydantic import BaseModel, Field, validator
from typing import List, Optional, Union
from datetime import date

class HolidayItem(BaseModel):
    date_kind: str = Field(..., alias="dateKind")
    date_name: str = Field(..., alias="dateName")
    is_holiday: str = Field(..., alias="isHoliday")
    locdate: int  # 예: 20240101
    seq: int

    @property
    def formatted_date(self) -> date:
        """YYYYMMDD 정수형 날짜를 date 객체로 변환"""
        s_date = str(self.locdate)
        return date(year=int(s_date[:4]), month=int(s_date[4:6]), day=int(s_date[6:8]))

class HolidayItems(BaseModel):
    # 아이템이 하나일 경우 객체로, 여러 개일 경우 리스트로 올 수 있음
    item: Union[List[HolidayItem], HolidayItem, None] = None

class HolidayBody(BaseModel):
    items: Optional[HolidayItems] = None
    num_of_rows: int = Field(..., alias="numOfRows")
    page_no: int = Field(..., alias="pageNo")
    total_count: int = Field(..., alias="totalCount")

class HolidayHeader(BaseModel):
    result_code: str = Field(..., alias="resultCode")
    result_msg: str = Field(..., alias="resultMsg")

class HolidayResponse(BaseModel):
    header: HolidayHeader
    body: HolidayBody

class HolidayApiResponse(BaseModel):
    response: HolidayResponse
