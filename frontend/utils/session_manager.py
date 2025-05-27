"""
Streamlit 세션 상태 관리
"""
import streamlit as st
from typing import List, Dict, Any
from frontend.config.settings import AppConfig

class SessionManager:
    """세션 상태 관리 클래스"""
    
    def __init__(self):
        self.config = AppConfig()
    
    def initialize_session(self) -> None:
        """세션 상태 초기화"""
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": self.config.DEFAULT_WELCOME_MESSAGE
                }
            ]
        
        if "session_id" not in st.session_state:
            import uuid
            st.session_state.session_id = str(uuid.uuid4())
        
        if "search_history" not in st.session_state:
            st.session_state.search_history = []
        
        if "current_products" not in st.session_state:
            st.session_state.current_products = []
    
    def add_message(self, role: str, content: str) -> None:
        """메시지 추가"""
        message = {"role": role, "content": content}
        st.session_state.messages.append(message)
        
        # 메시지 수 제한
        if len(st.session_state.messages) > self.config.MAX_MESSAGES:
            # 첫 번째 메시지(환영 메시지)는 유지하고 오래된 메시지 삭제
            st.session_state.messages = (
                st.session_state.messages[:1] + 
                st.session_state.messages[-(self.config.MAX_MESSAGES-1):]
            )
    
    def get_messages(self) -> List[Dict[str, str]]:
        """메시지 목록 반환"""
        return st.session_state.messages
    
    def add_search_history(self, query: str) -> None:
        """검색 기록 추가"""
        if query not in st.session_state.search_history:
            st.session_state.search_history.append(query)
            # 최근 10개만 유지
            if len(st.session_state.search_history) > 10:
                st.session_state.search_history = st.session_state.search_history[-10:]
    
    def get_search_history(self) -> List[str]:
        """검색 기록 반환"""
        return st.session_state.search_history
    
    def set_current_products(self, products: List[Dict[str, Any]]) -> None:
        """현재 상품 목록 설정"""
        st.session_state.current_products = products
    
    def get_current_products(self) -> List[Dict[str, Any]]:
        """현재 상품 목록 반환"""
        return st.session_state.current_products
    
    def clear_session(self) -> None:
        """세션 초기화"""
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        self.initialize_session() 