from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from typing import Optional
from .service import HolidayService

app = FastAPI(title="한국 공휴일 조회 서비스")

# 파일 경로 설정
BASE_DIR = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

service = HolidayService()

@app.get("/", response_class=HTMLResponse)
async def index(
    request: Request,
    from_date: Optional[str] = Query(None, alias="from"),
    to_date: Optional[str] = Query(None, alias="to")
):
    holidays = []
    error_msg = None
    
    # 검색 조건이 하나라도 있으면 조회 수행
    if from_date or to_date:
        holidays = await service.get_holidays(from_date, to_date)
        if not holidays:
            error_msg = "조회된 공휴일 정보가 없거나 입력 형식이 잘못되었습니다."

    return templates.TemplateResponse(
        "index.html", 
        {
            "request": request, 
            "holidays": holidays, 
            "from_val": from_date or "", 
            "to_val": to_date or "",
            "error_msg": error_msg
        }
    )
