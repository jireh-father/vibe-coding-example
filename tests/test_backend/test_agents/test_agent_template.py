import pytest
import datetime
from backend.agents.agent_template import AgentTemplate


class MockAgent(AgentTemplate):
    """테스트용 에이전트 구현 클래스"""
    
    async def process_message(self, message: str, session_id: str, context=None):
        """메시지 처리 메서드 구현"""
        await self.update_session_state(session_id, {"last_message": message})
        return {
            "response": f"'{message}'에 대한 응답입니다.",
            "session_id": session_id,
            "timestamp": datetime.datetime.now().isoformat()
        }
    
    async def initialize_session(self, session_id: str):
        """세션 초기화 메서드 구현"""
        session_data = {
            "created_at": datetime.datetime.now().isoformat(),
            "messages": [],
            "preferences": {
                "sort_by": "price_low",
                "max_results": 5
            }
        }
        await self.update_session_state(session_id, session_data)
        return session_data
    
    async def search_products(self, query: str):
        """상품 검색 메서드 구현"""
        return {
            "products": [
                {"name": f"{query} 상품1", "price": 10000},
                {"name": f"{query} 상품2", "price": 20000}
            ],
            "message": f"{query}에 대한 검색 결과입니다."
        }
    
    async def run(self, query: str, **kwargs):
        """실행 메서드 구현"""
        return {
            "result": f"{query} 실행 결과",
            "timestamp": datetime.datetime.now().isoformat()
        }


@pytest.fixture
def agent():
    """Agent 인스턴스 픽스처"""
    return MockAgent()


@pytest.mark.asyncio
async def test_process_message(agent):
    """메시지 처리 테스트"""
    result = await agent.process_message("테스트 메시지", "session_123")
    
    assert "response" in result
    assert "session_id" in result
    assert result["session_id"] == "session_123"
    assert "테스트 메시지" in result["response"]
    
    # 세션 상태 업데이트 확인
    session_state = await agent.get_session_state("session_123")
    assert "last_message" in session_state
    assert session_state["last_message"] == "테스트 메시지"


@pytest.mark.asyncio
async def test_initialize_session(agent):
    """세션 초기화 테스트"""
    result = await agent.initialize_session("new_session")
    
    assert "created_at" in result
    assert "messages" in result
    assert "preferences" in result
    assert isinstance(result["messages"], list)
    
    # 세션 상태 확인
    session_state = await agent.get_session_state("new_session")
    assert session_state == result


@pytest.mark.asyncio
async def test_update_session_state(agent):
    """세션 상태 업데이트 테스트"""
    session_id = "test_session"
    
    # 초기 업데이트
    state1 = await agent.update_session_state(session_id, {"key1": "value1"})
    assert "key1" in state1
    assert state1["key1"] == "value1"
    
    # 추가 업데이트
    state2 = await agent.update_session_state(session_id, {"key2": "value2"})
    assert "key1" in state2
    assert "key2" in state2
    assert state2["key1"] == "value1"
    assert state2["key2"] == "value2"
    
    # 값 변경
    state3 = await agent.update_session_state(session_id, {"key1": "updated"})
    assert state3["key1"] == "updated"
    assert state3["key2"] == "value2"


@pytest.mark.asyncio
async def test_run(agent):
    """run 메서드 테스트"""
    result = await agent.run("테스트 쿼리")
    
    assert "result" in result
    assert "테스트 쿼리" in result["result"]
    assert "timestamp" in result