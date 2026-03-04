# 한국 공휴일 정보 조회

## 프로젝트 개요
**kr-rest-days**는 한국의 공휴일 정보를 제공하는 웹서비스 입니다.
공휴일 정보는 `공공데이터포털(data.go.kr)`에서 제공하는 한국천문연구원_특일 정보 API의 공휴일 정보 조회(/getRestDeInfo)를 사용합니다.

### 외부 API 상세
- **엔드포인트:** `https://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getRestDeInfo`
- **주요 요청 파라미터:**
  - `solYear`: 조회할 연도 (yyyy)
  - `solMonth`: 조회할 월 (mm, 선택 사항)
  - `ServiceKey`: 공공데이터포털에서 발급받은 인증키 (환경변수 `DATA_GO_API_KEY` 사용)
  - `_type`: 응답 형식 (json 권장)

### 주요 기술 스택
- **언어:** Python 3.11 (이상 필수)
- **패키지 관리:** `uv` (pip 대신 uv 사용 필수)
- **백엔드 프레임워크:** FastAPI (비동기 처리 및 빠른 API 개발)
- **프론트엔드:** HTML5, Vanilla CSS, JavaScript (현대적이고 깔끔한 UI)
- **로깅:** Loguru
- **HTTP 클라이언트:** HTTPX (비동기 외부 API 요청)
- **데이터 검증:** Pydantic (입력 값 및 API 응답 검증)
- **환경 변수 관리:** python-dotenv

## 커뮤니케이션 가이드라인
- **응답 언어:** 모든 기술적 설명 및 대화는 **한국어(ko_kr)**로 진행하십시오.

## 개발 및 실행 규칙
### 1. 코딩 컨벤션
- **포맷팅:** `Black` (Line length: 120자)
- **임포팅:** `isort` (Black 프로필 적용)
- **로깅:** 모든 모듈에서 `loguru.logger`를 사용하여 표준화된 로그 출력
- **타입힌팅:** 적극적인 Python Type Hinting 사용

## 기술 설계 (Technical Design)

### 1. 웹 인터페이스 요구사항
- **입력 폼:** From(yyyy/mm)과 To(yyyy/mm) 입력 필드 제공
- **조회 로직:**
  - `From & To`: 해당 기간 내 공휴일 조회
  - `From only`: 해당 년월부터 최신 데이터까지 조회
  - `To only`: 해당 년월의 공휴일만 조회
  - `Year only (yyyy)`: From 또는 To에 년도만 입력 시, 해당 연도의 전체 데이터 조회

### 2. 시스템 아키텍처
- **Web Layer (FastAPI):** 사용자 요청을 처리하고 결과를 시각화된 HTML로 응답
- **API Wrapper Layer:** 공공데이터 API 통신 및 XML-to-JSON 변환
- **Service Layer:** 사용자 입력 조건(From/To)에 따른 필터링 및 비즈니스 로직 처리
- **Data Model Layer:** 공휴일 정보를 정의하는 Pydantic 모델

### 3. 디렉토리 구조
```text
kr-rest-days/
├── src/
│   └── kr_rest_days/
│       ├── main.py        # FastAPI 엔트리포인트
│       ├── client.py      # 외부 API 통신
│       ├── models.py      # Pydantic 모델
│       ├── service.py     # 조회 로직 (From/To 필터링)
│       ├── static/        # CSS, JS 파일
│       └── templates/     # HTML 템플릿 (Jinja2)
├── tests/
├── .env
├── pyproject.toml
└── GEMINI.md
```

## 개발 로드맵 (Roadmap)
1. **[Phase 1] 환경 구축:** 프로젝트 초기화 및 의존성 설정
2. **[Phase 2] API 클라이언트:** 공공데이터 API 연동 및 데이터 모델링
3. **[Phase 3] 백엔드 서비스:** 입력 조건(From/To, Year-only)에 따른 조회 엔진 구현
4. **[Phase 4] 프론트엔드 UI:** 조회 폼 및 결과 리스트를 포함한 웹 페이지 개발 (Vanilla CSS)
5. **[Phase 5] 통합 및 배포:** 전체 기능 검증 및 로컬 실행 환경 구축