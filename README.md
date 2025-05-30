# 🛒 PriceFinder Agent

최저가 쇼핑 AI Agent - 스마트한 가격 비교와 상품 추천 서비스

## 📋 프로젝트 개요

PriceFinder Agent는 사용자가 원하는 상품의 최저가를 찾아주고, 다양한 쇼핑몰의 가격을 비교하여 최적의 구매 결정을 도와주는 AI Agent입니다.

## ��️ 프로젝트 구조

```
vibe-coding-example/
├── backend/             # FastAPI 백엔드 서버
│   ├── __init__.py
│   ├── main.py          # 애플리케이션 진입점
│   ├── routers/         # API 라우터
│   │   ├── __init__.py
│   │   └── chat.py      # 채팅 API
│   ├── schemas/         # Pydantic 스키마
│   │   ├── __init__.py
│   │   └── chat.py      # 채팅 스키마
│   ├── services/        # 비즈니스 로직 서비스
│   │   ├── __init__.py
│   │   └── chat_service.py  # 채팅 서비스
│   └── agents/          # AI Agent 로직
│       ├── __init__.py
│       ├── shopping_agent.py    # 쇼핑 에이전트
│       ├── prompts/     # 프롬프트 템플릿
│       │   ├── __init__.py
│       │   └── shopping_prompts.py
│       └── config/      # 에이전트 설정
│           ├── __init__.py
│           └── mcp_config.py
├── frontend/            # Streamlit 프론트엔드
│   ├── components/      # UI 컴포넌트
│   │   ├── __init__.py
│   │   ├── chat_interface.py
│   │   └── product_card.py
│   ├── pages/           # 페이지 컴포넌트
│   │   ├── __init__.py
│   │   └── chat_page.py
│   ├── utils/           # 유틸리티 함수
│   │   ├── __init__.py
│   │   ├── session_manager.py
│   │   └── api_client.py
│   ├── config/          # 설정 파일
│   │   ├── __init__.py
│   │   └── settings.py
│   ├── styles/          # CSS 스타일
│   │   ├── __init__.py
│   │   └── custom.css
│   ├── __init__.py
│   └── app.py           # 메인 Streamlit 앱
├── tests/               # 테스트 코드
│   ├── test_backend/    # 백엔드 테스트
│   │   ├── test_routers/
│   │   ├── test_services/
│   │   ├── test_schemas/
│   │   └── test_agents/
│   └── test_frontend/   # 프론트엔드 테스트
│       ├── test_components/
│       └── test_utils/
├── .github/workflows/   # GitHub Actions 설정
├── .env                 # 환경 변수 (gitignore)
├── requirements.txt     # 의존성 관리
├── pytest.ini          # 테스트 설정
└── README.md
```

## 🚀 시작하기

### 1. 환경 설정

```bash
# 의존성 설치
pip install -r requirements.txt
```

### 2. 환경 변수 설정

`.env` 파일을 생성하여 다음 변수들을 설정하세요:

```env
# Google Gemini API
GOOGLE_API_KEY=your_actual_google_api_key_here

# Brave Search API (선택사항)
BRAVE_API_KEY=your_actual_brave_api_key_here

# 환경 설정
ENVIRONMENT=development
```

### 3. 서버 실행

#### 🔧 FastAPI 백엔드 서버 실행

```bash
# 방법 1: uvicorn 직접 실행 (권장)
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# 방법 2: Python 모듈로 실행
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# 방법 3: main.py 직접 실행
cd backend
python main.py
```

백엔드 서버가 실행되면 다음 URL에서 확인할 수 있습니다:
- API 문서: http://localhost:8000/docs
- 대체 API 문서: http://localhost:8000/redoc
- 헬스체크: http://localhost:8000/health

#### 🎨 Streamlit 프론트엔드 실행

```bash
# Streamlit 앱 실행
streamlit run frontend/app.py

# 또는 포트 지정
streamlit run frontend/app.py --server.port 8501
```

프론트엔드가 실행되면 브라우저에서 http://localhost:8501 로 접속할 수 있습니다.

### 4. 통합 테스트

```bash
# Chat Service와 Shopping Agent 연결 테스트
python test_chat_integration.py
```

### 5. 단위 테스트 실행

```bash
# 전체 테스트 실행
pytest

# 특정 모듈 테스트
pytest tests/test_backend/test_agents/
pytest tests/test_backend/test_services/
pytest tests/test_backend/test_routers/

# 커버리지 리포트 생성
pytest --cov=backend --cov=frontend --cov-report=term-missing

# 상세 테스트 출력
pytest -v
```

## 🔄 개발 워크플로우

### 로컬 개발 환경 실행 순서

1. **환경 변수 설정**: `.env` 파일에 API 키 설정
2. **백엔드 실행**: `uvicorn backend.main:app --reload`
3. **프론트엔드 실행**: `streamlit run frontend/app.py`
4. **테스트**: 브라우저에서 http://localhost:8501 접속하여 채팅 테스트

### API 테스트

```bash
# cURL로 채팅 API 테스트
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{
       "message": "아이폰 15 최저가 검색해줘",
       "session_id": "test-session-123"
     }'
```

## 🛠️ 기술 스택

### 백엔드
- **FastAPI**: 고성능 웹 API 프레임워크
- **LangGraph**: AI Agent 워크플로우 관리 (create_react_agent)
- **LangChain**: LLM 통합 프레임워크
- **langchain-mcp-adapters**: Model Context Protocol 통합
- **Google Gemini 2.5 Flash**: 대화형 AI 모델
- **MCP Servers**: 웹 검색, 브라우저 자동화, 파일시스템 접근

### 프론트엔드
- **Streamlit**: 빠른 웹 앱 개발 프레임워크
- **HTTPX**: 비동기 HTTP 클라이언트
- **Custom CSS**: 맞춤형 스타일링

### 개발 도구
- **Pytest**: 테스트 프레임워크
- **Python-dotenv**: 환경 변수 관리
- **Pydantic**: 데이터 검증
- **GitHub Actions**: 지속적 통합 및 테스트 자동화

## 📱 주요 기능

### 1. 채팅 인터페이스
- 자연어로 상품 검색 요청
- 실시간 대화형 상호작용
- 스트리밍 응답 (SSE)

### 2. 상품 검색 및 비교
- 다중 쇼핑몰 가격 비교
- 상품 정보 요약
- 최저가 추천
- 리뷰 분석

### 3. AI Agent 기능
- **상품 검색**: 일반적인 상품 최저가 검색
- **가격 비교**: 여러 쇼핑몰 가격 비교 및 추천
- **리뷰 분석**: 상품 리뷰 분석 및 장단점 요약

## 🧪 개발 원칙

### TDD (Test-Driven Development)
- 테스트 코드 우선 작성
- Red-Green-Refactor 사이클
- 높은 테스트 커버리지 유지

### Clean Architecture
- 계층별 책임 분리
- 의존성 역전 원칙
- 비즈니스 로직과 프레임워크 분리

### SOLID 원칙
- 단일 책임 원칙
- 개방/폐쇄 원칙
- 리스코프 치환 원칙
- 인터페이스 분리 원칙
- 의존성 역전 원칙

## 🔧 환경 변수

`.env` 파일을 생성하여 다음 변수들을 설정하세요:

```env
# Google Gemini API (필수)
GOOGLE_API_KEY=your_actual_google_api_key_here

# Brave Search API (선택사항 - 웹 검색 기능 향상)
BRAVE_API_KEY=your_actual_brave_api_key_here

# 환경 설정
ENVIRONMENT=development
```

## 🚨 문제 해결

### 일반적인 문제들

1. **API 키 오류**: `.env` 파일에 올바른 API 키가 설정되었는지 확인
2. **포트 충돌**: 8000번(백엔드) 또는 8501번(프론트엔드) 포트가 사용 중인지 확인
3. **의존성 오류**: `pip install -r requirements.txt`로 모든 패키지 재설치

### 로그 확인

```bash
# 백엔드 로그 확인 (uvicorn 실행 시 콘솔에 출력)
# 프론트엔드 로그 확인 (streamlit 실행 시 콘솔에 출력)
```

## 📞 지원

문제가 발생하면 다음을 확인해주세요:
1. 환경 변수 설정 확인
2. 의존성 설치 확인
3. 포트 사용 상태 확인
4. 테스트 실행으로 기본 기능 확인