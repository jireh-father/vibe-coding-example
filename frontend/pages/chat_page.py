"""
메인 채팅 페이지
"""
import streamlit as st
from frontend.components.chat_interface import ChatInterface
from frontend.components.product_card import ProductCard
from frontend.utils.session_manager import SessionManager

class ChatPage:
    """채팅 페이지 클래스"""
    
    def __init__(self):
        self.session_manager = SessionManager()
        self.chat_interface = ChatInterface(self.session_manager)
        self.product_card = ProductCard()
    
    def render_header(self) -> None:
        """헤더 렌더링"""
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <h1>🛒 PriceFinder Agent</h1>
            <p style="font-size: 1.2rem; color: #666;">
                최저가 쇼핑 AI Agent와 대화하며 최적의 상품을 찾아보세요!
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    def render_quick_actions(self) -> None:
        """빠른 액션 버튼들"""
        st.subheader("🚀 빠른 검색")
        
        col1, col2, col3, col4 = st.columns(4)
        
        quick_searches = [
            ("📱 스마트폰", "아이폰 15 최저가"),
            ("💻 노트북", "게이밍 노트북 추천"),
            ("🎧 이어폰", "무선 이어폰 비교"),
            ("⌚ 스마트워치", "애플워치 할인")
        ]
        
        for i, (icon_text, query) in enumerate(quick_searches):
            with [col1, col2, col3, col4][i]:
                if st.button(icon_text, key=f"quick_{i}", use_container_width=True):
                    # 빠른 검색 실행
                    self.session_manager.add_message("user", query)
                    self.session_manager.add_search_history(query)
                    st.rerun()
    
    def render_status_info(self) -> None:
        """상태 정보 표시"""
        with st.expander("ℹ️ 시스템 정보", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**세션 ID:** {st.session_state.get('session_id', 'N/A')[:8]}...")
                st.write(f"**메시지 수:** {len(self.session_manager.get_messages())}")
            
            with col2:
                st.write(f"**검색 기록:** {len(self.session_manager.get_search_history())}개")
                st.write(f"**현재 상품:** {len(self.session_manager.get_current_products())}개")
    
    def render_products_section(self) -> None:
        """상품 섹션 렌더링"""
        current_products = self.session_manager.get_current_products()
        
        if current_products:
            st.divider()
            
            # 탭으로 다양한 뷰 제공
            tab1, tab2, tab3 = st.tabs(["🛍️ 상품 목록", "💰 가격 비교", "📊 요약"])
            
            with tab1:
                self.product_card.render_product_grid(current_products)
            
            with tab2:
                self.product_card.render_price_comparison(current_products)
            
            with tab3:
                self.product_card.render_product_summary(current_products)
    
    def render(self) -> None:
        """페이지 전체 렌더링"""
        # 헤더
        self.render_header()
        
        # 빠른 액션
        self.render_quick_actions()
        
        # 상태 정보
        self.render_status_info()
        
        st.divider()
        
        # 채팅 인터페이스
        self.chat_interface.render()
        
        # 상품 섹션
        self.render_products_section() 