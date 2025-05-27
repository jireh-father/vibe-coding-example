"""채팅 관련 데이터 스키마 정의"""
from typing import List, Optional, Literal
from pydantic import BaseModel, Field


class Product(BaseModel):
    """상품 정보 스키마"""
    name: str = Field(..., description="상품명")
    price: int = Field(..., description="가격(원)")
    store: str = Field(..., description="판매처")
    url: str = Field(..., description="상품 URL")
    image_url: Optional[str] = Field(None, description="상품 이미지 URL")


class ChatRequest(BaseModel):
    """채팅 요청 스키마"""
    message: str = Field(..., description="사용자 메시지")
    session_id: str = Field(..., description="세션 ID")
    image_url: Optional[str] = Field(None, description="이미지 URL (이미지 검색 시)")


class ChatResponse(BaseModel):
    """채팅 응답 스키마"""
    message: str = Field(..., description="AI 응답 메시지")
    session_id: str = Field(..., description="세션 ID")
    products: List[Product] = Field(default=[], description="검색된 상품 목록")


class StreamingEvent(BaseModel):
    """스트리밍 이벤트 스키마"""
    event_type: Literal["message", "products", "error", "thinking", "search"] = Field(
        ..., description="이벤트 타입"
    )
    data: str = Field(..., description="이벤트 데이터")
    session_id: str = Field(..., description="세션 ID") 