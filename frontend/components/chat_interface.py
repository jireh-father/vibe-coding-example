"""
채팅 인터페이스 컴포넌트
"""
import streamlit as st
import time
from typing import List, Dict, Any
from frontend.config.settings import UIMessages
from frontend.utils.session_manager import SessionManager
from frontend.utils.api_client import sync_send_message, sync_send_message_stream

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
            self._handle_bot_response_stream(prompt)
    
    def _handle_bot_response_stream(self, user_message: str) -> None:
        """봇 응답 처리 (스트리밍)"""
        with st.chat_message("assistant"):
            # 응답 컨테이너 생성
            response_container = st.empty()
            status_container = st.empty()
            
            try:
                # 스트리밍 응답 처리
                events = sync_send_message_stream(user_message, st.session_state.session_id)
                
                current_message = ""
                current_status = "처리 중..."
                
                for event in events:
                    if "error" in event:
                        # 에러 처리
                        error_message = f"❌ 오류: {event['error']}"
                        response_container.markdown(error_message)
                        self.session_manager.add_message("assistant", error_message)
                        return
                    
                    event_type = event.get("event_type", "")
                    event_data = event.get("data", "")
                    
                    if event_type == "thinking":
                        current_status = f"🤔 {event_data}"
                        status_container.info(current_status)
                    
                    elif event_type == "search":
                        current_status = f"🔍 {event_data}"
                        status_container.info(current_status)
                    
                    elif event_type == "message":
                        current_message = event_data
                        status_container.empty()  # 상태 메시지 제거
                        response_container.markdown(current_message)
                    
                    elif event_type == "error":
                        error_message = f"❌ {event_data}"
                        status_container.empty()
                        response_container.markdown(error_message)
                        self.session_manager.add_message("assistant", error_message)
                        return
                    
                    # 약간의 지연으로 스트리밍 효과
                    time.sleep(0.1)
                
                # 최종 메시지가 있으면 저장
                if current_message:
                    self.session_manager.add_message("assistant", current_message)
                else:
                    # 메시지가 없으면 기본 오류 메시지
                    fallback_message = "응답을 받지 못했습니다."
                    response_container.markdown(fallback_message)
                    self.session_manager.add_message("assistant", fallback_message)
                
            except Exception as e:
                # 예외 처리
                error_message = f"❌ 연결 오류: {str(e)}"
                status_container.empty()
                response_container.markdown(error_message)
                self.session_manager.add_message("assistant", error_message)
    
    def _handle_bot_response(self, user_message: str) -> None:
        """봇 응답 처리 (기존 방식 - 백업용)"""
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
                        bot_message = f"❌ {response['error']}"
                    else:
                        bot_message = response.get("message", "응답을 받지 못했습니다.")
                    
                except Exception as e:
                    bot_message = f"❌ 연결 오류: {str(e)}"
                
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
                        self._handle_bot_response_stream(query)
                        st.rerun()
            else:
                st.write("검색 기록이 없습니다.")
            
            # 세션 초기화 버튼
            if st.button("🗑️ 대화 초기화"):
                self.session_manager.clear_session()
                st.rerun()
    
    def render_quick_buttons(self) -> None:
        """빠른 검색 버튼들"""
        st.subheader("🚀 빠른 검색")
        
        col1, col2, col3 = st.columns(3)
        
        quick_searches = [
            "아이폰 15 최저가",
            "삼성 갤럭시 S24",
            "노트북 추천",
            "무선 이어폰",
            "게이밍 마우스",
            "스마트워치"
        ]
        
        for i, search_term in enumerate(quick_searches):
            col = [col1, col2, col3][i % 3]
            with col:
                if st.button(f"🔍 {search_term}", key=f"quick_{i}"):
                    self.session_manager.add_message("user", search_term)
                    self.session_manager.add_search_history(search_term)
                    self._handle_bot_response_stream(search_term)
                    st.rerun()
    
    def render(self) -> None:
        """전체 채팅 인터페이스 렌더링"""
        # 사이드바 렌더링
        self.render_sidebar_history()
        
        # 메인 채팅 영역
        st.title("🛒 PriceFinder Agent")
        st.write("최저가 쇼핑 AI Agent와 대화해보세요!")
        
        # 빠른 검색 버튼 (메시지가 없을 때만 표시)
        if not self.session_manager.get_messages():
            self.render_quick_buttons()
        
        # 메시지 표시
        self.render_messages()
        
        # 입력 영역
        self.render_input() 