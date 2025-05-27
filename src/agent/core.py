from typing import Dict, Any

class PriceFinderAgent:
    """최저가 쇼핑 Agent 기본 클래스"""
    
    def __init__(self):
        self.session_state = {}
    
    async def process_message(self, message: str, session_id: str) -> Dict[str, Any]:
        """메시지 처리 기본 메서드"""
        return {
            "response": f"메시지 '{message}' 처리 중... (구현 예정)",
            "session_id": session_id
        }
    
    async def search_products(self, query: str) -> Dict[str, Any]:
        """상품 검색 기본 메서드"""
        return {
            "products": [],
            "message": f"'{query}' 상품 검색 기능 구현 예정"
        } 