"""채팅 라우터 테스트 모듈"""
import json
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi.testclient import TestClient

from backend.main import app
from backend.schemas.chat import ChatRequest, StreamingEvent


client = TestClient(app)


def test_chat_endpoint():
    """채팅 엔드포인트 테스트"""
    # ChatService.process_message 모의 설정
    with patch('backend.routers.chat.ChatService') as mock_service_class:
        mock_service = MagicMock()
        mock_service_class.return_value = mock_service
        
        async def fake_streaming_response():
            yield StreamingEvent(
                event_type="message",
                data="검색 중입니다...",
                session_id="user123"
            )
            yield StreamingEvent(
                event_type="message",
                data="아이폰 15의 최저가는 1,000,000원입니다.",
                session_id="user123"
            )
            
        # process_message 메서드 모킹
        mock_service.process_message.return_value = fake_streaming_response()
        
        # 채팅 API 호출
        response = client.post(
            "/chat",
            json={
                "message": "아이폰 15 최저가 알려줘",
                "session_id": "user123",
                "image_url": None
            },
            headers={"Accept": "text/event-stream"}
        )
        
        # 응답 확인
        assert response.status_code == 200
        assert "text/event-stream" in response.headers["content-type"]
        
        # 서비스 호출 검증
        called_with = mock_service.process_message.call_args[0][0]
        assert isinstance(called_with, ChatRequest)
        assert called_with.message == "아이폰 15 최저가 알려줘"
        assert called_with.session_id == "user123"


def test_chat_endpoint_invalid_request():
    """잘못된 요청 처리 테스트"""
    response = client.post(
        "/chat",
        json={
            # message 필드 누락
            "session_id": "user123"
        }
    )
    assert response.status_code == 422  # Validation Error 