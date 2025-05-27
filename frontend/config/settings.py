"""
앱 설정 및 상수 정의
"""
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class AppConfig:
    """앱 기본 설정"""
    PAGE_TITLE: str = "PriceFinder Agent"
    PAGE_ICON: str = "🛒"
    LAYOUT: str = "wide"
    
    # 색상 테마
    PRIMARY_COLOR: str = "#FF6B6B"
    SECONDARY_COLOR: str = "#4ECDC4"
    BACKGROUND_COLOR: str = "#F7F9FC"
    TEXT_COLOR: str = "#2C3E50"
    
    # API 설정
    API_BASE_URL: str = "http://localhost:8000"
    
    # 채팅 설정
    MAX_MESSAGES: int = 100
    DEFAULT_WELCOME_MESSAGE: str = "안녕하세요! 최저가 쇼핑 도우미입니다. 어떤 상품을 찾고 계신가요?"

@dataclass
class UIMessages:
    """UI 메시지 상수"""
    CHAT_INPUT_PLACEHOLDER: str = "상품을 검색해보세요... (예: 아이폰 15, 노트북)"
    LOADING_MESSAGE: str = "검색 중입니다..."
    ERROR_MESSAGE: str = "죄송합니다. 오류가 발생했습니다. 다시 시도해주세요."
    NO_RESULTS_MESSAGE: str = "검색 결과가 없습니다. 다른 키워드로 시도해보세요."

@dataclass
class StyleConfig:
    """스타일 설정"""
    CHAT_CONTAINER_HEIGHT: int = 600
    SIDEBAR_WIDTH: int = 300
    
    # CSS 클래스
    USER_MESSAGE_CLASS: str = "user-message"
    BOT_MESSAGE_CLASS: str = "bot-message"
    PRODUCT_CARD_CLASS: str = "product-card" 