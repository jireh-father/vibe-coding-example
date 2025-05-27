"""
채팅 인터페이스 컴포넌트
"""
import streamlit as st
from typing import List, Dict, Any
from frontend.config.settings import UIMessages
from frontend.utils.session_manager import SessionManager
from frontend.utils.api_client import sync_send_message

class ChatInterface:
    """채팅 인터페이스 클래스"""
    
    def __init__(self, session_manager: SessionManager):
        self.session_manager = session_manager
        self.ui_messages = UIMessages()
    
    def render_messages(self) -> None:
        """메시지 목록 렌더링"""
        messages = self.session_manager.get_messages()
        
        for message in messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    def render_input(self) -> None:
        """입력 영역 렌더링"""
        if prompt := st.chat_input(self.ui_messages.CHAT_INPUT_PLACEHOLDER):
            # 사용자 메시지 추가
            self.session_manager.add_message("user", prompt)
            self.session_manager.add_search_history(prompt)
            
            # 사용자 메시지 표시
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # 봇 응답 처리
            self._handle_bot_response(prompt)
    
    def _handle_bot_response(self, user_message: str) -> None:
        """봇 응답 처리"""
        with st.chat_message("assistant"):
            # 로딩 메시지 표시
            with st.spinner(self.ui_messages.LOADING_MESSAGE):
                try:
                    # API 호출
                    response = sync_send_message(
                        user_message, 
                        st.session_state.session_id
                    )
                    
                    if "error" in response:
                        bot_message = self.ui_messages.ERROR_MESSAGE
                    else:
                        bot_message = response.get("response", "응답을 받지 못했습니다.")
                    
                except Exception as e:
                    bot_message = f"{self.ui_messages.ERROR_MESSAGE}\n상세 오류: {str(e)}"
                
                # 봇 메시지 표시 및 저장
                st.markdown(bot_message)
                self.session_manager.add_message("assistant", bot_message)
    
    def render_sidebar_history(self) -> None:
        """사이드바에 검색 기록 표시"""
        with st.sidebar:
            st.subheader("🔍 최근 검색")
            
            search_history = self.session_manager.get_search_history()
            
            if search_history:
                for i, query in enumerate(reversed(search_history[-5:])):  # 최근 5개만 표시
                    if st.button(f"📝 {query}", key=f"history_{i}"):
                        # 검색 기록 클릭 시 해당 쿼리로 검색
                        self.session_manager.add_message("user", query)
                        self._handle_bot_response(query)
                        st.rerun()
            else:
                st.write("검색 기록이 없습니다.")
            
            # 세션 초기화 버튼
            if st.button("🗑️ 대화 초기화"):
                self.session_manager.clear_session()
                st.rerun()
    
    def render(self) -> None:
        """전체 채팅 인터페이스 렌더링"""
        # 사이드바 렌더링
        self.render_sidebar_history()
        
        # 메인 채팅 영역
        st.title("🛒 PriceFinder Agent")
        st.write("최저가 쇼핑 AI Agent와 대화해보세요!")
        
        # 메시지 표시
        self.render_messages()
        
        # 입력 영역
        self.render_input() 