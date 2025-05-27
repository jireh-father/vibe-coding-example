import pytest
from src.agent.core import PriceFinderAgent

@pytest.fixture
def agent():
    """Agent 인스턴스 픽스처"""
    return PriceFinderAgent()

@pytest.mark.asyncio
async def test_process_message(agent):
    """메시지 처리 테스트"""
    result = await agent.process_message("테스트 메시지", "session_123")
    
    assert "response" in result
    assert "session_id" in result
    assert result["session_id"] == "session_123"
    assert "테스트 메시지" in result["response"]

@pytest.mark.asyncio
async def test_search_products(agent):
    """상품 검색 테스트"""
    result = await agent.search_products("노트북")
    
    assert "products" in result
    assert "message" in result
    assert isinstance(result["products"], list)
    assert "노트북" in result["message"] 