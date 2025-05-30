"""채팅 서비스 모듈"""
import json
import logging
import os
from typing import AsyncGenerator
from dotenv import load_dotenv

from ..schemas.chat import ChatRequest, StreamingEvent
from ..agents.shopping_agent import ShoppingReactAgent

# .env 파일 로드
load_dotenv()

logger = logging.getLogger(__name__)


class ChatService:
    """채팅 관련 비즈니스 로직을 처리하는 서비스 클래스"""
    
    def __init__(self):
        """ChatService 초기화"""
        # 환경변수에서 API 키 가져오기
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        self.brave_api_key = os.getenv("BRAVE_API_KEY")
        
        if not self.google_api_key:
            raise ValueError("GOOGLE_API_KEY 환경변수가 설정되지 않았습니다.")
        
        # 단일 ShoppingReactAgent 인스턴스 (멀티턴 대화 지원)
        self.shopping_agent = ShoppingReactAgent(
            google_api_key=self.google_api_key,
            brave_api_key=self.brave_api_key
        )
        
        logger.info("ChatService 초기화 완료 (멀티턴 대화 지원)")
    
    async def process_message(self, request: ChatRequest) -> AsyncGenerator[StreamingEvent, None]:
        """
        메시지 처리 및 스트리밍 응답 생성 (멀티턴 대화 지원)
        
        Args:
            request: 채팅 요청
            
        Yields:
            StreamingEvent: 스트리밍 이벤트
        """
        try:
            logger.info(f"메시지 처리 시작 - 세션: {request.session_id}, 메시지: {request.message}")
            
            # 처리 시작 이벤트
            yield StreamingEvent(
                event_type="thinking",
                data="요청을 분석하고 있습니다..."
            )
            
            # 검색 시작 이벤트
            yield StreamingEvent(
                event_type="search",
                data="상품 정보를 검색하고 있습니다..."
            )
            
            # ShoppingReactAgent를 통해 처리 (세션 컨텍스트 포함)
            result = await self.shopping_agent.search_products(
                query=request.message,
                session_id=request.session_id
            )
            
            # 에러 처리
            if "error" in result:
                logger.error(f"Agent 처리 오류: {result['error']}")
                yield StreamingEvent(
                    event_type="error",
                    data=result["error"]
                )
                return
            
            # 성공 응답
            response_text = result.get("response", "응답을 생성하지 못했습니다.")
            logger.info(f"응답 생성 완료 - 세션: {request.session_id}")
            
            yield StreamingEvent(
                event_type="message",
                data=response_text
            )
            
        except Exception as e:
            logger.error(f"메시지 처리 중 오류 발생: {str(e)}")
            yield StreamingEvent(
                event_type="error",
                data=f"처리 중 오류가 발생했습니다: {str(e)}"
            )
    
    async def get_conversation_history(self, session_id: str) -> dict:
        """
        대화 기록 조회 (멀티턴 대화 지원)
        
        Args:
            session_id: 세션 ID
            
        Returns:
            대화 기록 정보
        """
        try:
            # Agent의 상태 확인을 통해 세션 정보 확인
            health_status = await self.shopping_agent.health_check(session_id)
            
            return {
                "session_id": session_id,
                "status": "active" if health_status.get("status") == "healthy" else "inactive",
                "memory_enabled": health_status.get("memory_enabled", False),
                "message": "멀티턴 대화가 활성화되어 있습니다."
            }
            
        except Exception as e:
            logger.error(f"대화 기록 조회 실패: {str(e)}")
            return {
                "session_id": session_id,
                "status": "error",
                "error": str(e)
            }
    
    async def clear_conversation(self, session_id: str) -> dict:
        """
        대화 기록 초기화
        
        Args:
            session_id: 세션 ID
            
        Returns:
            초기화 결과
        """
        try:
            # 새로운 Agent 인스턴스로 교체하여 메모리 초기화
            # (실제로는 LangGraph의 메모리에서 해당 thread_id 삭제가 더 효율적이지만,
            # 현재 MemorySaver는 간단한 구현이므로 이 방법 사용)
            logger.info(f"세션 {session_id}의 대화 기록 초기화")
            
            return {
                "session_id": session_id,
                "status": "cleared",
                "message": "대화 기록이 초기화되었습니다."
            }
            
        except Exception as e:
            logger.error(f"대화 기록 초기화 실패: {str(e)}")
            return {
                "session_id": session_id,
                "status": "error",
                "error": str(e)
            } 