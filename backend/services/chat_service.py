"""채팅 서비스 모듈"""
import json
import logging
from typing import AsyncGenerator

from ..schemas.chat import ChatRequest, StreamingEvent

logger = logging.getLogger(__name__)


class ChatService:
    """채팅 관련 비즈니스 로직을 처리하는 서비스 클래스"""
    
    async def process_message(self, request: ChatRequest) -> AsyncGenerator[StreamingEvent, None]:
        """
        사용자 메시지를 처리하고 응답을 스트리밍 형태로 반환
        
        Args:
            request: 사용자 채팅 요청
            
        Yields:
            StreamingEvent: 스트리밍 이벤트
        """
        logger.info(f"Processing message for session {request.session_id}: {request.message}")
        
        try:
            # 상태 업데이트 이벤트 전송
            yield StreamingEvent(
                event_type="thinking",
                data="메시지를 처리 중입니다...",
                session_id=request.session_id
            )
            
            # Agent 호출하여 응답 스트리밍
            async for event in self._call_agent(request):
                yield event
                
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            yield StreamingEvent(
                event_type="error",
                data=f"메시지 처리 중 오류가 발생했습니다: {str(e)}",
                session_id=request.session_id
            )
    
    async def _call_agent(self, request: ChatRequest) -> AsyncGenerator[StreamingEvent, None]:
        """
        AI Agent를 호출하여 응답을 생성
        
        Args:
            request: 사용자 채팅 요청
            
        Yields:
            StreamingEvent: Agent의 응답 스트리밍 이벤트
        """
        # 스텁 구현 - 실제 Agent 통합 전까지 사용할 임시 구현
        # 실제 구현에서는 이 부분이 LangGraph Agent와 연동될 예정
        if True:  # 항상 실행
            raise NotImplementedError("Agent 구현이 필요합니다")
            
        # 코드가 실행되지 않는 스텁 응답 (테스트용)
        # 실제로는 이 코드는 실행되지 않음
        yield StreamingEvent(
            event_type="message",
            data="테스트 응답입니다",
            session_id=request.session_id
        ) 