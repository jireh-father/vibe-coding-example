"""채팅 서비스 테스트 모듈"""
import pytest
from unittest.mock import AsyncMock, patch

from backend.schemas.chat import ChatRequest, StreamingEvent
from backend.services.chat_service import ChatService


@pytest.fixture
def chat_service():
    """ChatService 픽스처"""
    return ChatService()


@pytest.mark.asyncio
async def test_process_message(chat_service):
    """메시지 처리 테스트"""
    request = ChatRequest(
        message="아이폰 15 최저가 알려줘",
        session_id="user123",
        image_url=None
    )
    
    # Agent 호출 모의 설정
    with patch('backend.services.chat_service.ChatService._call_agent') as mock_call_agent:
        async def fake_agent_generator():
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
            yield StreamingEvent(
                event_type="products",
                data='[{"name":"Apple 아이폰 15","price":1000000,"store":"애플스토어","url":"https://apple.com/iphone15","image_url":"https://example.com/iphone15.jpg"}]',
                session_id="user123"
            )
        
        mock_call_agent.return_value = fake_agent_generator()
        
        # 서비스 호출 및 응답 확인
        responses = []
        async for response in chat_service.process_message(request):
            responses.append(response)
        
        # 응답 검증
        assert len(responses) == 4  # thinking 이벤트 + 3개의 모의 응답
        assert responses[0].event_type == "thinking"
        assert responses[1].event_type == "message"
        assert responses[1].data == "검색 중입니다..."
        assert responses[3].event_type == "products"
        
        # Agent 호출 검증
        mock_call_agent.assert_called_once_with(request)


@pytest.mark.asyncio
async def test_call_agent():
    """Agent 호출 테스트 (실제 구현 전 스텁)"""
    # 이 테스트는 Agent 구현 후 업데이트 필요
    # 현재는 서비스가 정상적으로 구현되었는지 확인하는 용도로만 사용
    chat_service = ChatService()
    request = ChatRequest(
        message="아이폰 15 최저가 알려줘",
        session_id="user123",
        image_url=None
    )
    
    # 현재는 스텁 구현이므로 NotImplementedError 예외 발생 예상
    with pytest.raises(NotImplementedError):
        async for _ in chat_service._call_agent(request):
            break  # 첫 번째 yield만 시도 