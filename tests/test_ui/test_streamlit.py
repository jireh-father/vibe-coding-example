import pytest
import streamlit as st
from unittest.mock import patch, MagicMock
import importlib
import sys

def test_frontend_app_imports():
    """Frontend 앱 임포트 테스트"""
    try:
        import frontend.app
        assert True
    except ImportError:
        pytest.fail("Frontend 앱 임포트 실패")

def test_session_manager_import():
    """SessionManager 임포트 테스트"""
    try:
        from frontend.utils.session_manager import SessionManager
        session_manager = SessionManager()
        assert session_manager is not None
    except ImportError:
        pytest.fail("SessionManager 임포트 실패")

def test_chat_interface_import():
    """ChatInterface 임포트 테스트"""
    try:
        from frontend.components.chat_interface import ChatInterface
        from frontend.utils.session_manager import SessionManager
        
        session_manager = SessionManager()
        chat_interface = ChatInterface(session_manager)
        assert chat_interface is not None
    except ImportError:
        pytest.fail("ChatInterface 임포트 실패")

def test_product_card_import():
    """ProductCard 임포트 테스트"""
    try:
        from frontend.components.product_card import ProductCard
        product_card = ProductCard()
        assert product_card is not None
    except ImportError:
        pytest.fail("ProductCard 임포트 실패")

def test_api_client_import():
    """APIClient 임포트 테스트"""
    try:
        from frontend.utils.api_client import APIClient
        api_client = APIClient()
        assert api_client is not None
    except ImportError:
        pytest.fail("APIClient 임포트 실패")

@patch('streamlit.set_page_config')
def test_app_config(mock_config):
    """앱 설정 테스트"""
    try:
        # 이미 로드된 모듈을 제거하고 다시 로드
        if 'frontend.app' in sys.modules:
            del sys.modules['frontend.app']
        import frontend.app
        # 설정이 호출되었는지 확인
        mock_config.assert_called_once()
    except Exception as e:
        pytest.fail(f"앱 설정 테스트 실패: {str(e)}")

def test_config_settings():
    """설정 파일 테스트"""
    try:
        from frontend.config.settings import AppConfig, UIMessages, StyleConfig
        
        config = AppConfig()
        ui_messages = UIMessages()
        style_config = StyleConfig()
        
        assert config.PAGE_TITLE == "PriceFinder Agent"
        assert config.PAGE_ICON == "🛒"
        assert ui_messages.CHAT_INPUT_PLACEHOLDER is not None
        assert style_config.CHAT_CONTAINER_HEIGHT > 0
        
    except ImportError:
        pytest.fail("설정 파일 임포트 실패")

# 추가 테스트 - SessionManager 직접 테스트
def test_session_manager_methods():
    """SessionManager 메서드 테스트 (모킹 없이)"""
    from frontend.utils.session_manager import SessionManager
    from frontend.config.settings import AppConfig
    
    # 세션 매니저 인스턴스 생성
    manager = SessionManager()
    
    # initialize_session 메서드 검증
    assert hasattr(manager, 'initialize_session')
    assert callable(manager.initialize_session)
    
    # add_message 메서드 검증
    assert hasattr(manager, 'add_message')
    assert callable(manager.add_message)
    
    # get_messages 메서드 검증
    assert hasattr(manager, 'get_messages')
    assert callable(manager.get_messages)
    
    # add_search_history 메서드 검증
    assert hasattr(manager, 'add_search_history')
    assert callable(manager.add_search_history)
    
    # get_search_history 메서드 검증
    assert hasattr(manager, 'get_search_history')
    assert callable(manager.get_search_history)
    
    # set_current_products 메서드 검증
    assert hasattr(manager, 'set_current_products')
    assert callable(manager.set_current_products)
    
    # get_current_products 메서드 검증
    assert hasattr(manager, 'get_current_products')
    assert callable(manager.get_current_products)
    
    # clear_session 메서드 검증
    assert hasattr(manager, 'clear_session')
    assert callable(manager.clear_session)

# ProductCard 메서드 단위 테스트
def test_product_card_methods():
    """ProductCard 메서드 테스트 (Streamlit 모킹 없이)"""
    from frontend.components.product_card import ProductCard
    
    card = ProductCard()
    
    # 메서드 존재 확인
    assert hasattr(card, 'render_single_product')
    assert callable(card.render_single_product)
    
    assert hasattr(card, 'render_product_grid')
    assert callable(card.render_product_grid)
    
    assert hasattr(card, 'render_price_comparison')
    assert callable(card.render_price_comparison)
    
    assert hasattr(card, 'render_product_summary')
    assert callable(card.render_product_summary)

# API 클라이언트 테스트
@pytest.mark.asyncio
async def test_api_client_methods():
    """API 클라이언트 메서드 테스트"""
    from frontend.utils.api_client import APIClient
    import httpx
    
    # httpx 요청 모킹
    with patch("httpx.AsyncClient") as mock_client:
        # 모의 응답 설정
        mock_response = MagicMock()
        mock_response.json.return_value = {"status": "ok"}
        mock_response.raise_for_status.return_value = None
        
        # AsyncClient 인스턴스 설정
        mock_async_client = MagicMock()
        mock_async_client.__aenter__.return_value.get.return_value = mock_response
        mock_async_client.__aenter__.return_value.post.return_value = mock_response
        mock_client.return_value = mock_async_client
        
        client = APIClient()
        
        # 헬스 체크 테스트
        result = await client.health_check()
        assert result == {"status": "ok"}
        
        # 메시지 전송 테스트
        chat_result = await client.send_message("안녕하세요", "session123")
        assert chat_result == {"status": "ok"}
        
        # 상품 검색 테스트
        search_result = await client.search_products("아이폰")
        assert search_result == {"status": "ok"}

# API 클라이언트 예외 처리 테스트
@pytest.mark.asyncio
async def test_api_client_error_handling():
    """API 클라이언트 에러 처리 테스트"""
    from frontend.utils.api_client import APIClient
    import httpx
    
    # 타임아웃 예외 테스트
    with patch("httpx.AsyncClient") as mock_client:
        mock_async_client = MagicMock()
        mock_async_client.__aenter__.return_value.get.side_effect = httpx.TimeoutException("타임아웃")
        mock_client.return_value = mock_async_client
        
        client = APIClient()
        result = await client.health_check()
        assert "error" in result
        assert "시간이 초과" in result["error"]
    
    # HTTP 오류 테스트
    with patch("httpx.AsyncClient") as mock_client:
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "404 에러", request=MagicMock(), response=MagicMock()
        )
        mock_response.response.status_code = 404
        
        mock_async_client = MagicMock()
        mock_async_client.__aenter__.return_value.get.return_value = mock_response
        mock_client.return_value = mock_async_client
        
        client = APIClient()
        result = await client.health_check()
        assert "error" in result
        assert "HTTP 오류" in result["error"]

# 동기 API 래퍼 함수 테스트
@patch('frontend.utils.api_client.APIClient.health_check')
@patch('asyncio.run')
def test_sync_api_functions(mock_run, mock_health_check):
    """동기 API 래퍼 함수 테스트"""
    from frontend.utils.api_client import sync_health_check, sync_send_message, sync_search_products
    
    # 모의 응답 설정
    mock_response = {"status": "ok"}
    mock_run.return_value = mock_response
    
    # 헬스 체크 테스트
    result = sync_health_check()
    assert result == mock_response
    assert mock_run.called
    
    # API 호출 파라미터 테스트
    sync_send_message("테스트 메시지", "session123")
    sync_search_products("아이폰")
    assert mock_run.call_count == 3

# ChatInterface 메서드 테스트
def test_chat_interface_methods():
    """ChatInterface 메서드 테스트 (모킹 없이)"""
    from frontend.components.chat_interface import ChatInterface
    
    # 세션 매니저 모킹
    session_manager = MagicMock()
    
    # 인스턴스 생성
    chat_interface = ChatInterface(session_manager)
    
    # 메서드 검증
    assert hasattr(chat_interface, 'render_messages')
    assert callable(chat_interface.render_messages)
    
    assert hasattr(chat_interface, 'render_input')
    assert callable(chat_interface.render_input)
    
    assert hasattr(chat_interface, '_handle_bot_response')
    assert callable(chat_interface._handle_bot_response)
    
    assert hasattr(chat_interface, 'render_sidebar_history')
    assert callable(chat_interface.render_sidebar_history)
    
    assert hasattr(chat_interface, 'render')
    assert callable(chat_interface.render)

# ChatPage 메서드 테스트
def test_chat_page_methods():
    """ChatPage 메서드 테스트 (모킹 없이)"""
    from frontend.pages.chat_page import ChatPage
    
    # 인스턴스 생성
    chat_page = ChatPage()
    
    # 메서드 검증
    assert hasattr(chat_page, 'render_header')
    assert callable(chat_page.render_header)
    
    assert hasattr(chat_page, 'render_quick_actions')
    assert callable(chat_page.render_quick_actions)
    
    assert hasattr(chat_page, 'render_status_info')
    assert callable(chat_page.render_status_info)
    
    assert hasattr(chat_page, 'render_products_section')
    assert callable(chat_page.render_products_section)
    
    assert hasattr(chat_page, 'render')
    assert callable(chat_page.render) 