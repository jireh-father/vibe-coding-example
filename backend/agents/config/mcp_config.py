"""
MCP 서버 설정
기존 MCP 서버들을 활용한 설정
"""
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 환경 변수에서 키 가져오기
SMITHERY_API_KEY = os.getenv("SMITHERY_API_KEY")

# 기본 MCP 서버 설정
MCP_SERVER_CONFIG = {
    "exa": {
        "transport": "streamable_http",
        "url": f"https://server.smithery.ai/exa/mcp?api_key={SMITHERY_API_KEY}"
    },
    # "browser": {
    #     "command": "npx", 
    #     "args": ["-y", "@modelcontextprotocol/server-puppeteer"],
    #     "transport": "stdio",
    # },
    # "filesystem": {
    #     "command": "npx",
    #     "args": ["-y", "@modelcontextprotocol/server-filesystem", "/tmp/shopping_data"],
    #     "transport": "stdio",
    # }
}

# 개발 환경별 설정
if os.getenv("ENVIRONMENT") == "development":
    # 개발 환경에서는 로컬 MCP 서버 사용 가능
    MCP_SERVER_CONFIG["filesystem"]["args"][-1] = "./tmp/shopping_data"
elif os.getenv("ENVIRONMENT") == "production":
    # 프로덕션 환경 최적화
    MCP_SERVER_CONFIG["filesystem"]["args"][-1] = "/var/tmp/shopping_data"

def get_mcp_config_with_api_keys(brave_api_key: str = None, **kwargs) -> dict:
    """
    API 키를 포함한 MCP 설정 반환
    
    Args:
        brave_api_key: Brave Search API 키
        **kwargs: 기타 API 키들
    
    Returns:
        dict: 완전한 MCP 서버 설정
    """
    config = MCP_SERVER_CONFIG.copy()
    
    # 웹 검색 서버에 API 키 추가
    if brave_api_key:
        config["web_search"]["env"] = {"BRAVE_API_KEY": brave_api_key}
    
    # 기타 환경 변수 추가
    for key, value in kwargs.items():
        if key.endswith("_API_KEY") and value:
            if "env" not in config["web_search"]:
                config["web_search"]["env"] = {}
            config["web_search"]["env"][key] = value
    
    return config
