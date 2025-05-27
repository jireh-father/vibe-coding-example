# 🛒 PriceFinder Agent

최저가 쇼핑 AI Agent - 스마트한 가격 비교와 상품 추천 서비스

## 📋 프로젝트 개요

PriceFinder Agent는 사용자가 원하는 상품의 최저가를 찾아주고, 다양한 쇼핑몰의 가격을 비교하여 최적의 구매 결정을 도와주는 AI Agent입니다.

## 🏗️ 프로젝트 구조

```
vibe_coding_tutorial/
├── src/
│   ├── api/              # FastAPI 백엔드 서버
│   │   ├── __init__.py
│   │   └── main.py
│   └── agent/            # AI Agent 로직
│       ├── __init__.py
│       └── core.py
├── frontend/             # Streamlit 프론트엔드
│   ├── components/       # UI 컴포넌트
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
│   ├── test_api/
│   ├── test_agent/
│   └── test_ui/
├── .github/workflows/   # GitHub Actions 설정
│   └── test-and-report.yml # 테스트 및 커버리지 리포트
├── .venv/               # 가상환경
├── requirements.txt     # 의존성 관리
├── pytest.ini          # 테스트 설정
└── README.md
```

## 🚀 시작하기

### 1. 환경 설정

```bash
# 가상환경 활성화
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# 의존성 설치
pip install -r requirements.txt
```

### 2. 서버 실행

#### FastAPI 백엔드 서버
```bash
cd src/api
python main.py
```
또는
```bash
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

#### Streamlit 프론트엔드
```bash
streamlit run frontend/app.py
```

### 3. 테스트 실행

```bash
# 전체 테스트 실행
pytest

# 특정 모듈 테스트
pytest tests/test_api/
pytest tests/test_agent/
pytest tests/test_ui/

# 커버리지 리포트 생성
pytest --cov=src --cov=frontend --cov-report=term-missing
```

## 🔄 CI/CD 통합

이 프로젝트는 GitHub Actions를 사용하여 지속적 통합(CI)을 구현합니다:

- 모든 브랜치에 대한 push 이벤트에서 테스트 실행
- main 브랜치로의 PR에서 테스트 실행
- 테스트 결과 및 커버리지 리포트를 Discord로 전송

### Discord 웹훅 설정

1. Discord 서버에서 채널 설정 > 통합 > 웹후크 생성
2. GitHub 저장소 설정 > Secrets and variables > Actions > New repository secret
3. 이름: `DISCORD_WEBHOOK_URL`, 값: Discord 웹후크 URL

자세한 내용은 [테스트 및 커버리지 리포트 워크플로우](.github/workflows/test-and-report.yml)를 참조하세요.

## 🛠️ 기술 스택

### 백엔드
- **FastAPI**: 고성능 웹 API 프레임워크
- **LangGraph**: AI Agent 워크플로우 관리
- **LangChain**: LLM 통합 프레임워크
- **MCP Adapters**: Model Context Protocol 통합

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
- 검색 기록 관리

### 2. 상품 검색 및 비교
- 다중 쇼핑몰 가격 비교
- 상품 정보 요약
- 최저가 추천

### 3. 사용자 경험
- 반응형 웹 디자인
- 빠른 검색 버튼
- 직관적인 UI/UX

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
# API 설정
API_HOST=localhost
API_PORT=8000

# Google Gemini API
GOOGLE_API_KEY=your_gemini_api_key_here

# 개발 설정
DEBUG=true
LOG_LEVEL=INFO
```

## 📝 API 문서

FastAPI 서버 실행 후 다음 URL에서 API 문서를 확인할 수 있습니다:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

## 📞 연락처

프로젝트 관련 문의사항이 있으시면 이슈를 생성해 주세요.


