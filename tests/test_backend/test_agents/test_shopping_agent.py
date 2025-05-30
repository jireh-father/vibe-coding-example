"""
최저가 쇼핑 React Agent 테스트
"""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
import os
import sys

# 프로젝트 루트를 Python 경로에 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from backend.agents.shopping_agent import ShoppingReactAgent
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
BRAVE_API_KEY = os.getenv("BRAVE_API_KEY")

class TestShoppingReactAgent:
    """ShoppingReactAgent 테스트 클래스"""
    
    @pytest.fixture
    def agent(self):
        """테스트용 Agent 인스턴스"""
        return ShoppingReactAgent(
            google_api_key=GOOGLE_API_KEY,
            brave_api_key=BRAVE_API_KEY
        )
    
    @pytest.mark.asyncio
    async def test_agent_initialization(self, agent):
        """Agent 초기화 테스트"""
        # Given: MCP 클라이언트 모킹
        with patch('backend.agents.shopping_agent.MultiServerMCPClient') as mock_client_class:
            mock_client = MagicMock()
            mock_client.get_tools = AsyncMock(return_value=[])
            mock_client_class.return_value = mock_client
            
            with patch('backend.agents.shopping_agent.create_react_agent') as mock_create_agent:
                mock_create_agent.return_value = MagicMock()
                
                # When: Agent 초기화
                await agent.initialize()
                
                # Then: Agent가 정상적으로 초기화됨
                assert agent.client is not None
                assert agent.agent is not None
                mock_client.get_tools.assert_called_once()
                mock_create_agent.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_search_products_success(self, agent):
        """상품 검색 성공 테스트"""
        # Given: 모킹된 Agent 응답
        mock_response = {
            "messages": [
                {"content": "아이폰 15 검색 결과입니다."},
                {"content": "최저가 상품을 찾았습니다: 아이폰 15 Pro 128GB - 1,200,000원"}
            ]
        }
        
        with patch.object(agent, 'agent') as mock_agent:
            mock_agent.ainvoke = AsyncMock(return_value=mock_response)
            
            # When: 상품 검색 실행
            result = await agent.search_products("아이폰 15")
            
            # Then: 올바른 결과 반환
            assert result["query"] == "아이폰 15"
            assert "response" in result
            assert "full_messages" in result
            assert result["response"] == mock_response["messages"][-1]["content"]
            mock_agent.ainvoke.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_search_products_without_initialization(self, agent):
        """초기화 없이 검색 시 자동 초기화 테스트"""
        # Given: Agent가 초기화되지 않은 상태
        assert agent.agent is None
        
        with patch.object(agent, 'initialize') as mock_initialize:
            mock_initialize.return_value = None
            agent.agent = MagicMock()
            agent.agent.ainvoke = AsyncMock(return_value={"messages": [{"content": "test"}]})
            
            # When: 상품 검색 실행
            await agent.search_products("테스트 상품")
            
            # Then: 자동으로 초기화됨
            mock_initialize.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_compare_and_recommend_with_budget(self, agent):
        """예산 기반 추천 테스트"""
        # Given: 예산이 있는 추천 요청
        budget = 1000000
        query = "노트북"
        
        mock_response = {
            "messages": [{"content": f"예산 {budget:,}원 내에서 {query} 추천 결과"}]
        }
        
        with patch.object(agent, 'agent') as mock_agent:
            mock_agent.ainvoke = AsyncMock(return_value=mock_response)
            
            # When: 예산 기반 추천 실행
            result = await agent.compare_and_recommend(query, budget)
            
            # Then: 올바른 결과 반환
            assert result["query"] == query
            assert result["budget"] == budget
            assert "recommendation" in result
            
            # 호출된 프롬프트에 예산 정보가 포함되었는지 확인
            call_args = mock_agent.ainvoke.call_args[0][0]
            assert f"예산: {budget:,}원" in call_args["messages"][0][1]
    
    @pytest.mark.asyncio
    async def test_analyze_product_reviews(self, agent):
        """상품 리뷰 분석 테스트"""
        # Given: 리뷰 분석 요청
        query = "삼성 갤럭시 S24"
        
        mock_response = {
            "messages": [{"content": f"{query} 리뷰 분석 결과: 장점 - 카메라 성능 우수, 단점 - 배터리 수명"}]
        }
        
        with patch.object(agent, 'agent') as mock_agent:
            mock_agent.ainvoke = AsyncMock(return_value=mock_response)
            
            # When: 리뷰 분석 실행
            result = await agent.analyze_product_reviews(query)
            
            # Then: 올바른 결과 반환
            assert result["query"] == query
            assert "analysis" in result
            assert "full_messages" in result
    
    @pytest.mark.asyncio
    async def test_mcp_tools_integration(self):
        """기존 MCP 서버 연동 테스트"""
        # Given: MCP 클라이언트 설정
        from backend.agents.config.mcp_config import MCP_SERVER_CONFIG
        
        # When & Then: 설정이 올바르게 구성되었는지 확인
        assert "web_search" in MCP_SERVER_CONFIG
        assert "browser" in MCP_SERVER_CONFIG
        assert "filesystem" in MCP_SERVER_CONFIG
        
        # 각 서버 설정 검증
        web_search_config = MCP_SERVER_CONFIG["web_search"]
        assert web_search_config["command"] == "npx"
        assert "@modelcontextprotocol/server-web-search" in web_search_config["args"]
        assert web_search_config["transport"] == "stdio"
    
    @pytest.mark.asyncio
    async def test_cleanup(self, agent):
        """리소스 정리 테스트"""
        # Given: 초기화된 Agent
        agent.client = MagicMock()
        
        # When: 정리 실행
        await agent.cleanup()
        
        # Then: 에러 없이 완료됨 (현재는 pass 구현)
        assert True  # cleanup이 에러 없이 실행됨을 확인
    
    def test_agent_creation_with_api_keys(self):
        """API 키를 사용한 Agent 생성 테스트"""
        # Given: API 키들
        google_key = "test-google-key"
        brave_key = "test-brave-key"
        
        # When: Agent 생성
        agent = ShoppingReactAgent(google_key, brave_key)
        
        # Then: 올바르게 설정됨
        assert agent.brave_api_key == brave_key
        # SecretStr 객체의 경우 get_secret_value()로 접근
        try:
            assert str(agent.model.google_api_key) == google_key or agent.model.google_api_key.get_secret_value() == google_key
        except AttributeError:
            # google_api_key가 직접 문자열인 경우
            assert agent.google_api_key == google_key
        assert agent.client is None
        assert agent.agent is None
        assert agent.memory is not None  # 메모리 초기화 확인
    
    def test_agent_creation_without_brave_key(self):
        """Brave API 키 없이 Agent 생성 테스트"""
        # Given: Google API 키만
        google_key = "test-google-key"
        
        # When: Agent 생성
        agent = ShoppingReactAgent(google_key)
        
        # Then: 올바르게 설정됨
        assert agent.brave_api_key is None
        assert agent.google_api_key == google_key
        assert agent.memory is not None  # 메모리 초기화 확인
    
    @pytest.mark.asyncio
    async def test_search_products_success(self):
        """상품 검색 성공 테스트 (멀티턴 대화 지원)"""
        # Given: Agent와 모의 응답
        agent = ShoppingReactAgent("test-key")
        session_id = "test-session-123"
        
        # Mock agent 설정
        mock_agent = AsyncMock()
        mock_response = {
            "messages": [
                MagicMock(content="아이폰 15 최저가는 1,081,410원입니다.")
            ]
        }
        mock_agent.ainvoke.return_value = mock_response
        agent.agent = mock_agent
        
        # When: 상품 검색 실행
        result = await agent.search_products("아이폰 15", session_id)
        
        # Then: 올바른 결과 반환
        assert result["query"] == "아이폰 15"
        assert result["session_id"] == session_id
        assert "아이폰 15 최저가" in result["response"]
        assert "full_messages" in result
        
        # Agent가 올바른 config로 호출되었는지 확인
        mock_agent.ainvoke.assert_called_once()
        call_args = mock_agent.ainvoke.call_args
        assert call_args[1]["config"]["configurable"]["thread_id"] == session_id
    
    @pytest.mark.asyncio
    async def test_search_products_error(self):
        """상품 검색 실패 테스트"""
        # Given: Agent와 에러 상황
        agent = ShoppingReactAgent("test-key")
        session_id = "test-session-123"
        
        # Mock agent가 예외 발생
        mock_agent = AsyncMock()
        mock_agent.ainvoke.side_effect = Exception("네트워크 오류")
        agent.agent = mock_agent
        
        # When: 상품 검색 실행
        result = await agent.search_products("아이폰 15", session_id)
        
        # Then: 에러 정보 포함된 결과 반환
        assert result["query"] == "아이폰 15"
        assert result["session_id"] == session_id
        assert "error" in result
        assert "네트워크 오류" in result["error"]
    
    @pytest.mark.asyncio
    async def test_compare_and_recommend_success(self):
        """상품 비교 및 추천 성공 테스트 (멀티턴 대화 지원)"""
        # Given: Agent와 모의 응답
        agent = ShoppingReactAgent("test-key")
        session_id = "test-session-456"
        
        mock_agent = AsyncMock()
        mock_response = {
            "messages": [
                MagicMock(content="예산 100만원으로 아이폰 14를 추천합니다.")
            ]
        }
        mock_agent.ainvoke.return_value = mock_response
        agent.agent = mock_agent
        
        # When: 비교 및 추천 실행
        result = await agent.compare_and_recommend("아이폰", 1000000, session_id)
        
        # Then: 올바른 결과 반환
        assert result["query"] == "아이폰"
        assert result["budget"] == 1000000
        assert result["session_id"] == session_id
        assert "아이폰 14를 추천" in result["recommendation"]
        
        # 세션 컨텍스트 확인
        call_args = mock_agent.ainvoke.call_args
        assert call_args[1]["config"]["configurable"]["thread_id"] == session_id
    
    @pytest.mark.asyncio
    async def test_analyze_product_reviews_success(self):
        """상품 리뷰 분석 성공 테스트 (멀티턴 대화 지원)"""
        # Given: Agent와 모의 응답
        agent = ShoppingReactAgent("test-key")
        session_id = "test-session-789"
        
        mock_agent = AsyncMock()
        mock_response = {
            "messages": [
                MagicMock(content="아이폰 15 리뷰 분석: 카메라 성능이 우수합니다.")
            ]
        }
        mock_agent.ainvoke.return_value = mock_response
        agent.agent = mock_agent
        
        # When: 리뷰 분석 실행
        result = await agent.analyze_product_reviews("아이폰 15", session_id)
        
        # Then: 올바른 결과 반환
        assert result["query"] == "아이폰 15"
        assert result["session_id"] == session_id
        assert "카메라 성능" in result["analysis"]
        
        # 세션 컨텍스트 확인
        call_args = mock_agent.ainvoke.call_args
        assert call_args[1]["config"]["configurable"]["thread_id"] == session_id
    
    @pytest.mark.asyncio
    async def test_get_product_details_success(self):
        """상품 상세 정보 조회 성공 테스트 (멀티턴 대화 지원)"""
        # Given: Agent와 모의 응답
        agent = ShoppingReactAgent("test-key")
        session_id = "test-session-abc"
        
        mock_agent = AsyncMock()
        mock_response = {
            "messages": [
                MagicMock(content="아이폰 15 상세 정보: 128GB, 블루 색상")
            ]
        }
        mock_agent.ainvoke.return_value = mock_response
        agent.agent = mock_agent
        
        # When: 상세 정보 조회 실행
        result = await agent.get_product_details("아이폰 15", "https://example.com/iphone15", session_id)
        
        # Then: 올바른 결과 반환
        assert result["query"] == "아이폰 15"
        assert result["url"] == "https://example.com/iphone15"
        assert result["session_id"] == session_id
        assert "128GB" in result["details"]
        
        # 세션 컨텍스트 확인
        call_args = mock_agent.ainvoke.call_args
        assert call_args[1]["config"]["configurable"]["thread_id"] == session_id
    
    @pytest.mark.asyncio
    async def test_health_check_success(self):
        """상태 확인 성공 테스트 (멀티턴 대화 지원)"""
        # Given: Agent와 모의 응답
        agent = ShoppingReactAgent("test-key")
        session_id = "test-session-health"
        
        mock_agent = AsyncMock()
        mock_response = {
            "messages": [
                MagicMock(content="안녕하세요! 도움이 필요하시면 말씀해주세요.")
            ]
        }
        mock_agent.ainvoke.return_value = mock_response
        agent.agent = mock_agent
        
        # When: 상태 확인 실행
        result = await agent.health_check(session_id)
        
        # Then: 올바른 상태 정보 반환
        assert result["status"] == "healthy"
        assert result["session_id"] == session_id
        assert result["memory_enabled"] == True
        assert "안녕하세요" in result["test_response"]
        
        # 세션 컨텍스트 확인
        call_args = mock_agent.ainvoke.call_args
        assert call_args[1]["config"]["configurable"]["thread_id"] == session_id
    
    @pytest.mark.asyncio
    async def test_health_check_failure(self):
        """상태 확인 실패 테스트"""
        # Given: Agent와 에러 상황
        agent = ShoppingReactAgent("test-key")
        session_id = "test-session-error"
        
        # _initialize_agent에서 예외 발생하도록 설정
        with patch.object(agent, '_initialize_agent', side_effect=Exception("초기화 실패")):
            # When: 상태 확인 실행
            result = await agent.health_check(session_id)
            
            # Then: 에러 상태 반환
            assert result["status"] == "unhealthy"
            assert result["session_id"] == session_id
            assert result["memory_enabled"] == False
            assert "초기화 실패" in result["error"]
    
    @pytest.mark.asyncio
    async def test_multi_turn_conversation_context(self):
        """멀티턴 대화 컨텍스트 유지 테스트"""
        # Given: Agent와 동일한 세션 ID
        agent = ShoppingReactAgent("test-key")
        session_id = "multi-turn-session"
        
        mock_agent = AsyncMock()
        agent.agent = mock_agent
        
        # 첫 번째 대화
        mock_agent.ainvoke.return_value = {
            "messages": [MagicMock(content="아이폰 15 정보를 찾았습니다.")]
        }
        result1 = await agent.search_products("아이폰 15", session_id)
        
        # 두 번째 대화 (같은 세션)
        mock_agent.ainvoke.return_value = {
            "messages": [MagicMock(content="256GB 모델은 더 비쌉니다.")]
        }
        result2 = await agent.search_products("256GB는 얼마야?", session_id)
        
        # Then: 두 호출 모두 같은 thread_id 사용
        assert mock_agent.ainvoke.call_count == 2
        
        # 모든 호출이 같은 session_id를 thread_id로 사용했는지 확인
        calls = mock_agent.ainvoke.call_args_list
        for call in calls:
            assert call[1]["config"]["configurable"]["thread_id"] == session_id
        
        # 결과 검증
        assert result1["session_id"] == session_id
        assert result2["session_id"] == session_id
    
    @pytest.mark.asyncio
    async def test_different_sessions_isolated(self):
        """서로 다른 세션의 격리 테스트"""
        # Given: Agent와 서로 다른 세션 ID들
        agent = ShoppingReactAgent("test-key")
        session_id_1 = "session-1"
        session_id_2 = "session-2"
        
        mock_agent = AsyncMock()
        agent.agent = mock_agent
        
        # 첫 번째 세션에서 검색
        mock_agent.ainvoke.return_value = {
            "messages": [MagicMock(content="세션 1 응답")]
        }
        result1 = await agent.search_products("아이폰", session_id_1)
        
        # 두 번째 세션에서 검색
        mock_agent.ainvoke.return_value = {
            "messages": [MagicMock(content="세션 2 응답")]
        }
        result2 = await agent.search_products("갤럭시", session_id_2)
        
        # Then: 서로 다른 thread_id 사용
        calls = mock_agent.ainvoke.call_args_list
        thread_id_1 = calls[0][1]["config"]["configurable"]["thread_id"]
        thread_id_2 = calls[1][1]["config"]["configurable"]["thread_id"]
        
        assert thread_id_1 == session_id_1
        assert thread_id_2 == session_id_2
        assert thread_id_1 != thread_id_2
        
        # 결과도 각각 올바른 세션 ID 포함
        assert result1["session_id"] == session_id_1
        assert result2["session_id"] == session_id_2


if __name__ == "__main__":
    pytest.main([__file__]) 