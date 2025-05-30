"""
최저가 쇼핑 전문 React Agent
"""
import logging
from typing import Dict, Any, Optional, List
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

from .config.mcp_config import get_mcp_config_with_api_keys
from .prompts.shopping_prompts import (
    SHOPPING_SYSTEM_PROMPT,
    get_search_prompt,
    get_comparison_prompt,
    get_review_analysis_prompt
)

logger = logging.getLogger(__name__)


class ShoppingReactAgent:
    """최저가 쇼핑 전문 React Agent"""
    
    def __init__(self, google_api_key: str, brave_api_key: str = None):
        """
        Agent 초기화
        
        Args:
            google_api_key: Google Gemini API 키
            brave_api_key: Brave Search API 키 (선택사항)
        """
        self.google_api_key = google_api_key
        self.brave_api_key = brave_api_key
        
        # LLM 모델 초기화
        self.model = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp",
            google_api_key=google_api_key,
            temperature=0.1
        )
        
        # 멀티턴 대화를 위한 메모리 초기화
        self.memory = MemorySaver()
        
        # MCP 클라이언트와 Agent는 지연 초기화
        self.client = None
        self.agent = None
        
        logger.info("ShoppingReactAgent 초기화 완료")
    
    async def _initialize_agent(self):
        """Agent 지연 초기화 (MCP 서버 연결 및 도구 설정)"""
        if self.agent is not None:
            return
        
        try:
            # MCP 설정 가져오기
            mcp_config = get_mcp_config_with_api_keys(self.brave_api_key)
            
            # MultiServerMCPClient 초기화
            self.client = MultiServerMCPClient(mcp_config)
            
            # MCP 도구 로드
            tools = await self.client.get_tools()
            logger.info(f"사용 가능한 도구 수: {len(tools)}")
            
            # React Agent 생성 (메모리 포함)
            self.agent = create_react_agent(
                model=self.model,
                tools=tools,
                prompt=SHOPPING_SYSTEM_PROMPT,
                checkpointer=self.memory  # 멀티턴 대화를 위한 메모리 추가
            )
            
            logger.info("React Agent 초기화 완료")
            
        except Exception as e:
            logger.error(f"Agent 초기화 실패: {str(e)}")
            raise
    
    async def search_products(self, query: str, session_id: str) -> Dict[str, Any]:
        """
        상품 검색 (멀티턴 대화 지원)
        
        Args:
            query: 검색 쿼리
            session_id: 세션 ID (thread_id로 사용)
            
        Returns:
            검색 결과
        """
        await self._initialize_agent()
        
        try:
            # 검색용 프롬프트 생성
            search_prompt = get_search_prompt(query)
            
            # 세션별 컨텍스트 설정
            config = {"configurable": {"thread_id": session_id}}
            
            response = await self.agent.ainvoke({
                "messages": [("user", f"다음 상품의 최저가를 찾아주세요: {query}")]
            }, config=config)
            
            # LangGraph 응답에서 마지막 메시지 추출
            messages = response.get("messages", [])
            if messages:
                last_message = messages[-1]
                if hasattr(last_message, 'content'):
                    content = last_message.content
                elif isinstance(last_message, dict):
                    content = last_message.get('content', str(last_message))
                else:
                    content = str(last_message)
            else:
                content = "응답을 받지 못했습니다."
            
            return {
                "query": query,
                "session_id": session_id,
                "response": content,
                "full_messages": messages
            }
            
        except Exception as e:
            logger.error(f"상품 검색 실패: {str(e)}")
            return {
                "query": query,
                "session_id": session_id,
                "error": f"검색 중 오류가 발생했습니다: {str(e)}"
            }
    
    async def compare_and_recommend(self, query: str, budget: float, session_id: str) -> Dict[str, Any]:
        """
        상품 비교 및 추천 (멀티턴 대화 지원)
        
        Args:
            query: 상품 쿼리
            budget: 예산
            session_id: 세션 ID
            
        Returns:
            비교 및 추천 결과
        """
        await self._initialize_agent()
        
        try:
            # 비교용 프롬프트 생성
            prompt = get_comparison_prompt(query, budget)
            
            # 세션별 컨텍스트 설정
            config = {"configurable": {"thread_id": session_id}}
            
            response = await self.agent.ainvoke({
                "messages": [("user", prompt)]
            }, config=config)
            
            # LangGraph 응답에서 마지막 메시지 추출
            messages = response.get("messages", [])
            if messages:
                last_message = messages[-1]
                if hasattr(last_message, 'content'):
                    content = last_message.content
                elif isinstance(last_message, dict):
                    content = last_message.get('content', str(last_message))
                else:
                    content = str(last_message)
            else:
                content = "응답을 받지 못했습니다."
            
            return {
                "query": query,
                "budget": budget,
                "session_id": session_id,
                "recommendation": content,
                "full_messages": messages
            }
            
        except Exception as e:
            logger.error(f"상품 비교 실패: {str(e)}")
            return {
                "query": query,
                "budget": budget,
                "session_id": session_id,
                "error": f"비교 중 오류가 발생했습니다: {str(e)}"
            }
    
    async def analyze_product_reviews(self, query: str, session_id: str) -> Dict[str, Any]:
        """
        상품 리뷰 분석 (멀티턴 대화 지원)
        
        Args:
            query: 상품 쿼리
            session_id: 세션 ID
            
        Returns:
            리뷰 분석 결과
        """
        await self._initialize_agent()
        
        try:
            # 리뷰 분석용 프롬프트 생성
            prompt = get_review_analysis_prompt(query)
            
            # 세션별 컨텍스트 설정
            config = {"configurable": {"thread_id": session_id}}
            
            response = await self.agent.ainvoke({
                "messages": [("user", prompt)]
            }, config=config)
            
            # LangGraph 응답에서 마지막 메시지 추출
            messages = response.get("messages", [])
            if messages:
                last_message = messages[-1]
                if hasattr(last_message, 'content'):
                    content = last_message.content
                elif isinstance(last_message, dict):
                    content = last_message.get('content', str(last_message))
                else:
                    content = str(last_message)
            else:
                content = "응답을 받지 못했습니다."
            
            return {
                "query": query,
                "session_id": session_id,
                "analysis": content,
                "full_messages": messages
            }
            
        except Exception as e:
            logger.error(f"리뷰 분석 실패: {str(e)}")
            return {
                "query": query,
                "session_id": session_id,
                "error": f"리뷰 분석 중 오류가 발생했습니다: {str(e)}"
            }
    
    async def get_product_details(self, query: str, url: str, session_id: str) -> Dict[str, Any]:
        """
        상품 상세 정보 조회 (멀티턴 대화 지원)
        
        Args:
            query: 상품 쿼리
            url: 상품 URL
            session_id: 세션 ID
            
        Returns:
            상품 상세 정보
        """
        await self._initialize_agent()
        
        try:
            prompt = f"다음 URL의 상품 상세 정보를 조회해주세요: {url}\n상품명: {query}"
            
            # 세션별 컨텍스트 설정
            config = {"configurable": {"thread_id": session_id}}
            
            response = await self.agent.ainvoke({
                "messages": [("user", prompt)]
            }, config=config)
            
            # LangGraph 응답에서 마지막 메시지 추출
            messages = response.get("messages", [])
            if messages:
                last_message = messages[-1]
                if hasattr(last_message, 'content'):
                    content = last_message.content
                elif isinstance(last_message, dict):
                    content = last_message.get('content', str(last_message))
                else:
                    content = str(last_message)
            else:
                content = "응답을 받지 못했습니다."
            
            return {
                "query": query,
                "url": url,
                "session_id": session_id,
                "details": content,
                "full_messages": messages
            }
            
        except Exception as e:
            logger.error(f"상품 상세 정보 조회 실패: {str(e)}")
            return {
                "query": query,
                "url": url,
                "session_id": session_id,
                "error": f"상세 정보 조회 중 오류가 발생했습니다: {str(e)}"
            }
    
    async def health_check(self, session_id: str) -> Dict[str, Any]:
        """
        Agent 상태 확인 (멀티턴 대화 지원)
        
        Args:
            session_id: 세션 ID
            
        Returns:
            상태 정보
        """
        try:
            await self._initialize_agent()
            
            # 세션별 컨텍스트 설정
            config = {"configurable": {"thread_id": session_id}}
            
            # 간단한 테스트 쿼리 실행
            test_response = await self.agent.ainvoke({
                "messages": [("user", "안녕하세요")]
            }, config=config)
            
            # LangGraph 응답에서 마지막 메시지 추출
            messages = test_response.get("messages", [])
            if messages:
                last_message = messages[-1]
                if hasattr(last_message, 'content'):
                    content = last_message.content
                elif isinstance(last_message, dict):
                    content = last_message.get('content', str(last_message))
                else:
                    content = str(last_message)
            else:
                content = "응답을 받지 못했습니다."
            
            return {
                "status": "healthy",
                "message": "Agent가 정상적으로 작동 중입니다.",
                "session_id": session_id,
                "test_response": content,
                "memory_enabled": True
            }
            
        except Exception as e:
            logger.error(f"상태 확인 실패: {str(e)}")
            return {
                "status": "unhealthy",
                "error": str(e),
                "session_id": session_id,
                "memory_enabled": False
            } 