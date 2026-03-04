# 📅 한국 공휴일 조회 서비스 (kr-rest-days)

공공데이터포털의 '특일 정보 조회 API'를 활용하여 한국의 공휴일 정보를 쉽고 빠르게 조회할 수 있는 웹 서비스입니다. 

## ✨ 주요 기능

- **유연한 기간 조회:**
  - `From & To`: 특정 기간(년/월) 내의 모든 공휴일 조회 (예: 2025/01 ~ 2026/12)
  - `Year Only`: 특정 연도의 전체 공휴일 조회 (예: 2025)
  - `Month Only`: 특정 월의 공휴일 조회 (예: 2025/05)
  - `From Only`: 특정 시점부터 현재 연도 말까지의 공휴일 조회
- **엑셀 복사 (TSV):** 조회된 결과를 클릭 한 번으로 클립보드에 복사하여 엑셀이나 스프레드시트에 바로 붙여넣을 수 있습니다.

## 🛠 기술 스택

- **Language:** Python 3.11+
- **Package Manager:** [uv](https://github.com/astral-sh/uv) (추천)
- **Backend:** FastAPI, Uvicorn
- **Frontend:** HTML5, Vanilla CSS, JavaScript, Jinja2
- **API Client:** HTTPX (Async)
- **Data Validation:** Pydantic v2
- **Logging:** Loguru

## 🚀 시작하기

### 1. 사전 준비
공공데이터포털에서 [한국천문연구원_특일 정보](https://www.data.go.kr/data/15012690/openapi.do) API 서비스 키를 발급받아야 합니다.

### 2. 환경 설정
프로젝트 루트에 `.env` 파일을 생성하고 발급받은 API 키를 입력합니다.
```env
DATA_GO_API_KEY=발급받은_서비스_키_입력
```

### 3. 의존성 설치
`uv`를 사용하여 가상 환경 구축 및 패키지를 설치합니다.
```powershell
# 가상 환경 생성 및 패키지 동기화
uv sync --all-extras
```

### 4. 서버 실행
```powershell
uv run uvicorn src.kr_rest_days.main:app --reload
```
서버가 실행되면 브라우저에서 `http://127.0.0.1:8000`에 접속합니다.

## 🧪 테스트 실행
비즈니스 로직(기간 필터링 등) 검증을 위한 단위 테스트를 실행할 수 있습니다.
```powershell
uv run pytest
```

## 📂 프로젝트 구조
```text
kr-rest-days/
├── src/
│   └── kr_rest_days/
│       ├── main.py        # FastAPI 엔트리포인트 및 라우팅
│       ├── service.py     # 기간 필터링 및 비즈니스 로직
│       ├── client.py      # 공공데이터 API 통신 (HTTPX)
│       ├── models.py      # Pydantic 데이터 모델
│       ├── config.py      # 환경 변수 및 설정 관리
│       ├── static/        # CSS (Toss Style)
│       └── templates/     # HTML 템플릿 (Jinja2)
├── tests/                 # Pytest 테스트 코드
├── .env                   # API 키 설정
├── pyproject.toml         # 프로젝트 의존성 관리
└── README.md
```

## 📝 라이선스
데이터의 출처는 [공공데이터포털](https://data.go.kr)입니다.
