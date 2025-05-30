"""채팅 관련 API 라우터"""
import json
import logging
from fastapi import APIRouter, Depends, HTTPException
from sse_starlette.sse import EventSourceResponse

from ..schemas.chat import ChatRequest
from ..services.chat_service import ChatService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chat", tags=["chat"])

# ChatService 싱글톤 인스턴스
_chat_service_instance = None


def get_chat_service() -> ChatService:
    """ChatService 의존성 주입 (싱글톤)"""
    global _chat_service_instance
    
    if _chat_service_instance is None:
        try:
            _chat_service_instance = ChatService()
        except ValueError as e:
            logger.error(f"ChatService 초기화 실패: {str(e)}")
            raise HTTPException(
                status_code=500, 
                detail=f"서비스 초기화 실패: {str(e)}"
            )
    
    return _chat_service_instance


@router.post("")
async def chat(
    request: ChatRequest,
    chat_service: ChatService = Depends(get_chat_service)
) -> EventSourceResponse:
    """
    채팅 메시지를 처리하고 스트리밍 응답을 반환
    
    Args:
        request: 채팅 요청 데이터
        chat_service: 채팅 서비스 인스턴스
        
    Returns:
        EventSourceResponse: 스트리밍 응답
    """
    logger.info(f"Chat request received: {request.message}")
    
    async def event_generator():
        try:
            async for event in chat_service.process_message(request):
                # StreamingEvent를 JSON으로 직렬화하여 SSE 이벤트로 전송
                print("yield event from process_message", event)
                print("yield event from process_message.model_dump_json()", event.model_dump_json())
                yield {
                    "event": "message",
                    "data": event.model_dump_json()
                }
        except Exception as e:
            import traceback
            traceback.print_exc()
            logger.error(f"Error in chat stream: {str(e)}")
            yield {
                "event": "error",
                "data": json.dumps({
                    "event_type": "error",
                    "data": f"스트리밍 중 오류가 발생했습니다: {str(e)}",
                    "session_id": request.session_id
                })
            }
    
    return EventSourceResponse(event_generator()) 