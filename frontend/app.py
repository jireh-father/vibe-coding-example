"""
PriceFinder Agent - 메인 Streamlit 앱
"""
import streamlit as st
import sys
import os

# 프로젝트 루트 경로를 시스템 경로에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

# 앱 설정
from frontend.config.settings import AppConfig
st.set_page_config(
    page_title=AppConfig.PAGE_TITLE,
    page_icon=AppConfig.PAGE_ICON,
    layout=AppConfig.LAYOUT,
    initial_sidebar_state="collapsed"
)

# 상대 경로로 임포트
from frontend.pages.chat_page import ChatPage
from frontend.utils.session_manager import SessionManager

def main():
    """메인 앱 실행"""
    # 세션 관리자 초기화
    session_manager = SessionManager()
    session_manager.initialize_session()
    
    # 메인 페이지 렌더링
    chat_page = ChatPage()
    chat_page.render()

if __name__ == "__main__":
    main() 