"""
API 클라이언트 유틸리티
"""
import httpx
import asyncio
from typing import Dict, Any, Optional
from frontend.config.settings import AppConfig

class APIClient:
    """API 클라이언트 클래스"""
    
    def __init__(self):
        self.config = AppConfig()
        self.base_url = self.config.API_BASE_URL
        self.timeout = 30.0
    
    async def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """HTTP 요청 실행"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                if method.upper() == "GET":
                    response = await client.get(url, params=data)
                elif method.upper() == "POST":
                    response = await client.post(url, json=data)
                else:
                    raise ValueError(f"지원하지 않는 HTTP 메서드: {method}")
                
                response.raise_for_status()
                return response.json()
                
        except httpx.TimeoutException:
            return {"error": "요청 시간이 초과되었습니다."}
        except httpx.HTTPStatusError as e:
            return {"error": f"HTTP 오류: {e.response.status_code}"}
        except Exception as e:
            return {"error": f"연결 오류: {str(e)}"}
    
    async def health_check(self) -> Dict[str, Any]:
        """서버 상태 확인"""
        return await self._make_request("GET", "/health")
    
    async def send_message(self, message: str, session_id: str) -> Dict[str, Any]:
        """메시지 전송"""
        data = {
            "message": message,
            "session_id": session_id
        }
        return await self._make_request("POST", "/chat", data)
    
    async def search_products(self, query: str) -> Dict[str, Any]:
        """상품 검색"""
        data = {"query": query}
        return await self._make_request("POST", "/search", data)

# 동기 래퍼 함수들 (Streamlit에서 사용)
def sync_health_check() -> Dict[str, Any]:
    """동기 헬스체크"""
    client = APIClient()
    return asyncio.run(client.health_check())

def sync_send_message(message: str, session_id: str) -> Dict[str, Any]:
    """동기 메시지 전송"""
    client = APIClient()
    return asyncio.run(client.send_message(message, session_id))

def sync_search_products(query: str) -> Dict[str, Any]:
    """동기 상품 검색"""
    client = APIClient()
    return asyncio.run(client.search_products(query)) 