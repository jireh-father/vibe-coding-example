"""
API 클라이언트 유틸리티
"""
import httpx
import asyncio
import json
from typing import Dict, Any, Optional, AsyncGenerator
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
        """HTTP 요청 실행 (일반 JSON 응답용)"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            import logging
            logger = logging.getLogger(__name__)
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                logger.info(f"API 요청 시작: {method.upper()} {url}")
                if data:
                    logger.debug(f"요청 데이터: {data}")
                
                if method.upper() == "GET":
                    response = await client.get(url, params=data)
                elif method.upper() == "POST":
                    response = await client.post(url, json=data)
                else:
                    raise ValueError(f"지원하지 않는 HTTP 메서드: {method}")
                
                logger.info(f"API 응답 상태: {response.status_code}")
                logger.debug(f"응답 헤더: {dict(response.headers)}")
                
                response.raise_for_status()
                response_data = response.json()
                logger.debug(f"응답 데이터: {response_data}")
                return response_data
                
        except httpx.TimeoutException:
            return {"error": "요청 시간이 초과되었습니다."}
        except httpx.HTTPStatusError as e:
            return {"error": f"HTTP 오류: {e.response.status_code}"}
        except Exception as e:
            return {"error": f"연결 오류: {str(e)}"}
    
    async def _stream_request(
        self, 
        method: str, 
        endpoint: str, 
        data: Optional[Dict[str, Any]] = None
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """SSE 스트리밍 요청 실행"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            import logging
            logger = logging.getLogger(__name__)
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                logger.info(f"SSE 스트리밍 요청 시작: {method.upper()} {url}")
                if data:
                    logger.debug(f"요청 데이터: {data}")
                
                if method.upper() == "POST":
                    async with client.stream("POST", url, json=data) as response:
                        response.raise_for_status()
                        
                        async for line in response.aiter_lines():
                            if line.startswith("data: "):
                                try:
                                    # SSE 데이터 파싱
                                    data_str = line[6:]  # "data: " 제거
                                    if data_str.strip():
                                        event_data = json.loads(data_str)
                                        yield event_data
                                except json.JSONDecodeError as e:
                                    logger.warning(f"JSON 파싱 오류: {e}, 데이터: {data_str}")
                                    continue
                else:
                    raise ValueError(f"스트리밍은 POST 메서드만 지원합니다: {method}")
                    
        except httpx.TimeoutException:
            yield {"error": "요청 시간이 초과되었습니다."}
        except httpx.HTTPStatusError as e:
            yield {"error": f"HTTP 오류: {e.response.status_code}"}
        except Exception as e:
            yield {"error": f"연결 오류: {str(e)}"}
    
    async def health_check(self) -> Dict[str, Any]:
        """서버 상태 확인"""
        return await self._make_request("GET", "/health")
    
    async def send_message_stream(self, message: str, session_id: str) -> AsyncGenerator[Dict[str, Any], None]:
        """메시지 전송 (스트리밍)"""
        data = {
            "message": message,
            "session_id": session_id
        }
        async for event in self._stream_request("POST", "/chat", data):
            yield event
    
    async def send_message(self, message: str, session_id: str) -> Dict[str, Any]:
        """메시지 전송 (스트리밍을 모아서 최종 응답만 반환)"""
        final_response = {"message": "", "events": []}
        
        async for event in self.send_message_stream(message, session_id):
            final_response["events"].append(event)
            
            # 에러가 있으면 즉시 반환
            if "error" in event:
                return event
            
            # 메시지 이벤트인 경우 최종 응답으로 설정
            if event.get("event_type") == "message":
                final_response["message"] = event.get("data", "")
        
        return final_response
    
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

def sync_send_message_stream(message: str, session_id: str):
    """동기 메시지 전송 (스트리밍)"""
    client = APIClient()
    
    async def stream_wrapper():
        events = []
        async for event in client.send_message_stream(message, session_id):
            events.append(event)
        return events
    
    return asyncio.run(stream_wrapper())

def sync_search_products(query: str) -> Dict[str, Any]:
    """동기 상품 검색"""
    client = APIClient()
    return asyncio.run(client.search_products(query)) 