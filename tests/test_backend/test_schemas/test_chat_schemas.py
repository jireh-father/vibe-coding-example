"""채팅 스키마 테스트 모듈"""
import pytest
from pydantic import ValidationError

from backend.schemas.chat import ChatRequest, ChatResponse, StreamingEvent


def test_chat_request_valid():
    """유효한 ChatRequest 생성 테스트"""
    data = {
        "message": "아이폰 15 최저가 알려줘",
        "session_id": "user123",
        "image_url": None
    }
    request = ChatRequest(**data)
    assert request.message == data["message"]
    assert request.session_id == data["session_id"]
    assert request.image_url is None


def test_chat_request_missing_message():
    """메시지 누락 시 ChatRequest 유효성 검사 실패 테스트"""
    data = {
        "session_id": "user123",
        "image_url": None
    }
    with pytest.raises(ValidationError):
        ChatRequest(**data)


def test_chat_response_valid():
    """유효한 ChatResponse 생성 테스트"""
    data = {
        "message": "아이폰 15의 최저가는 1,000,000원입니다.",
        "session_id": "user123",
        "products": [
            {
                "name": "Apple 아이폰 15",
                "price": 1000000,
                "store": "애플스토어",
                "url": "https://apple.com/iphone15",
                "image_url": "https://example.com/iphone15.jpg"
            }
        ]
    }
    response = ChatResponse(**data)
    assert response.message == data["message"]
    assert len(response.products) == 1
    assert response.products[0].name == "Apple 아이폰 15"
    assert response.products[0].price == 1000000


def test_streaming_event_valid():
    """유효한 StreamingEvent 생성 테스트"""
    data = {
        "event_type": "message",
        "data": "검색 중입니다...",
        "session_id": "user123"
    }
    event = StreamingEvent(**data)
    assert event.event_type == "message"
    assert event.data == "검색 중입니다..."
    assert event.session_id == "user123"


def test_streaming_event_invalid_type():
    """잘못된 이벤트 타입의 StreamingEvent 유효성 검사 실패 테스트"""
    data = {
        "event_type": "invalid_type",
        "data": "검색 중입니다...",
        "session_id": "user123"
    }
    with pytest.raises(ValidationError):
        StreamingEvent(**data) 