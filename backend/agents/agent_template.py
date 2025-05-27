from typing import Dict, Any, List, Optional
from abc import ABC, abstractmethod
import datetime

class AgentTemplate(ABC):
    """에이전트 기본 추상 클래스
    
    모든 특화된 에이전트는 이 클래스를 상속받아 구현해야 합니다.
    """
    
    def __init__(self):
        """에이전트 초기화"""
        self.session_state = {}
    
    @abstractmethod
    async def process_message(self, message: str, session_id: str, 
                             context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """사용자 메시지 처리 추상 메서드
        
        Args:
            message: 사용자 입력 메시지
            session_id: 세션 식별자
            context: 추가 컨텍스트 정보 (선택 사항)
            
        Returns:
            처리 결과를 포함한 딕셔너리
        """
        pass
    
    @abstractmethod
    async def initialize_session(self, session_id: str) -> Dict[str, Any]:
        """세션 초기화 추상 메서드
        
        Args:
            session_id: 세션 식별자
            
        Returns:
            초기화된 세션 정보
        """
        pass
    
    async def update_session_state(self, session_id: str, 
                                  updates: Dict[str, Any]) -> Dict[str, Any]:
        """세션 상태 업데이트
        
        Args:
            session_id: 세션 식별자
            updates: 업데이트할 상태 정보
            
        Returns:
            업데이트된 세션 상태
        """
        if session_id not in self.session_state:
            self.session_state[session_id] = {}
            
        self.session_state[session_id].update(updates)
        return self.session_state[session_id]
    
    async def get_session_state(self, session_id: str) -> Dict[str, Any]:
        """세션 상태 조회
        
        Args:
            session_id: 세션 식별자
            
        Returns:
            현재 세션 상태
        """
        if session_id not in self.session_state:
            self.session_state[session_id] = {}
            
        return self.session_state[session_id]

    @abstractmethod
    async def run(self, query: str, **kwargs) -> Dict[str, Any]:
        """
        에이전트 실행 메서드
        
        Args:
            query: 사용자 쿼리
            **kwargs: 추가 인자
            
        Returns:
            Dict[str, Any]: 응답 결과
        """
        pass
