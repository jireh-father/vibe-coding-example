"""
상품 카드 컴포넌트
"""
import streamlit as st
from typing import Dict, Any, List

class ProductCard:
    """상품 카드 클래스"""
    
    def __init__(self):
        pass
    
    def render_single_product(self, product: Dict[str, Any]) -> None:
        """단일 상품 카드 렌더링"""
        with st.container():
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col1:
                # 상품 이미지 (placeholder)
                if product.get("image_url"):
                    st.image(product["image_url"], width=100)
                else:
                    st.image("https://via.placeholder.com/100x100?text=No+Image", width=100)
            
            with col2:
                # 상품 정보
                st.subheader(product.get("name", "상품명 없음"))
                st.write(f"**가격:** {product.get('price', 'N/A')}")
                st.write(f"**쇼핑몰:** {product.get('store', 'N/A')}")
                
                if product.get("rating"):
                    st.write(f"**평점:** {'⭐' * int(product.get('rating', 0))} ({product.get('rating')})")
                
                if product.get("description"):
                    st.write(f"**설명:** {product['description'][:100]}...")
            
            with col3:
                # 액션 버튼
                if product.get("url"):
                    st.link_button("🛒 구매하기", product["url"])
                
                if st.button("❤️ 찜하기", key=f"like_{product.get('id', 'unknown')}"):
                    st.success("찜 목록에 추가되었습니다!")
    
    def render_product_grid(self, products: List[Dict[str, Any]]) -> None:
        """상품 그리드 렌더링"""
        if not products:
            st.info("검색된 상품이 없습니다.")
            return
        
        st.subheader(f"🛍️ 검색 결과 ({len(products)}개)")
        
        # 2열 그리드로 상품 표시
        for i in range(0, len(products), 2):
            col1, col2 = st.columns(2)
            
            with col1:
                if i < len(products):
                    self.render_single_product(products[i])
            
            with col2:
                if i + 1 < len(products):
                    self.render_single_product(products[i + 1])
            
            st.divider()
    
    def render_price_comparison(self, products: List[Dict[str, Any]]) -> None:
        """가격 비교 테이블 렌더링"""
        if not products:
            return
        
        st.subheader("💰 가격 비교")
        
        # 가격순 정렬
        sorted_products = sorted(
            products, 
            key=lambda x: float(x.get('price', '0').replace(',', '').replace('원', '')) if x.get('price') else 0
        )
        
        # 테이블 데이터 준비
        table_data = []
        for i, product in enumerate(sorted_products[:5]):  # 상위 5개만 표시
            rank = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else f"{i+1}위"
            table_data.append({
                "순위": rank,
                "상품명": product.get("name", "N/A")[:30] + "..." if len(product.get("name", "")) > 30 else product.get("name", "N/A"),
                "가격": product.get("price", "N/A"),
                "쇼핑몰": product.get("store", "N/A"),
                "평점": product.get("rating", "N/A")
            })
        
        # 테이블 표시
        st.dataframe(table_data, use_container_width=True)
    
    def render_product_summary(self, products: List[Dict[str, Any]]) -> None:
        """상품 요약 정보 렌더링"""
        if not products:
            return
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("총 상품 수", len(products))
        
        with col2:
            prices = [
                float(p.get('price', '0').replace(',', '').replace('원', '')) 
                for p in products if p.get('price')
            ]
            if prices:
                avg_price = sum(prices) / len(prices)
                st.metric("평균 가격", f"{avg_price:,.0f}원")
        
        with col3:
            if prices:
                min_price = min(prices)
                st.metric("최저 가격", f"{min_price:,.0f}원")
        
        with col4:
            if prices:
                max_price = max(prices)
                st.metric("최고 가격", f"{max_price:,.0f}원") 