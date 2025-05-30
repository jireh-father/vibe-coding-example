"""
Chat Service와 Shopping Agent 연결 테스트 (멀티턴 대화 지원)
"""
import asyncio
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

from backend.services.chat_service import ChatService
from backend.schemas.chat import ChatRequest

async def test_chat_integration():
    """Chat Service와 Shopping Agent 연결 테스트"""
    
    # API 키 확인
    google_api_key = os.getenv("GOOGLE_API_KEY")
    brave_api_key = os.getenv("BRAVE_API_KEY")
    
    print(f"Google API Key: {'설정됨' if google_api_key else '설정되지 않음'}")
    print(f"Brave API Key: {'설정됨' if brave_api_key else '설정되지 않음'}")
    
    if not google_api_key:
        print("❌ GOOGLE_API_KEY가 설정되지 않았습니다.")
        print("📝 .env 파일에 다음과 같이 설정해주세요:")
        print("GOOGLE_API_KEY=your_actual_google_api_key")
        print("BRAVE_API_KEY=your_actual_brave_api_key")
        return
    
    try:
        # ChatService 초기화
        print("\n🔧 ChatService 초기화 중...")
        chat_service = ChatService()
        print("✅ ChatService 초기화 성공!")
        
        # 테스트 세션 ID
        session_id = "test-session-multi-turn"
        
        # 첫 번째 메시지 테스트
        print(f"\n💬 첫 번째 메시지 테스트 (세션: {session_id})")
        request1 = ChatRequest(
            message="아이폰 15 최저가 알려줘",
            session_id=session_id
        )
        
        print("📤 요청 전송 중...")
        events1 = []
        async for event in chat_service.process_message(request1):
            print(f"📨 이벤트: {event.event_type} - {event.data[:100]}...")
            events1.append(event)
        
        print(f"✅ 첫 번째 응답 완료! (이벤트 수: {len(events1)})")
        
        # 두 번째 메시지 테스트 (멀티턴 - 같은 세션)
        print(f"\n💬 두 번째 메시지 테스트 (같은 세션: {session_id})")
        request2 = ChatRequest(
            message="256GB는 얼마야?",  # 이전 컨텍스트 참조
            session_id=session_id
        )
        
        print("📤 요청 전송 중...")
        events2 = []
        async for event in chat_service.process_message(request2):
            print(f"📨 이벤트: {event.event_type} - {event.data[:100]}...")
            events2.append(event)
        
        print(f"✅ 두 번째 응답 완료! (이벤트 수: {len(events2)})")
        
        # 다른 세션에서 테스트 (세션 격리 확인)
        print(f"\n💬 다른 세션 테스트")
        different_session_id = "test-session-different"
        request3 = ChatRequest(
            message="갤럭시 S24 가격 알려줘",
            session_id=different_session_id
        )
        
        print("📤 요청 전송 중...")
        events3 = []
        async for event in chat_service.process_message(request3):
            print(f"📨 이벤트: {event.event_type} - {event.data[:100]}...")
            events3.append(event)
        
        print(f"✅ 다른 세션 응답 완료! (이벤트 수: {len(events3)})")
        
        # 대화 기록 조회 테스트
        print(f"\n📋 대화 기록 조회 테스트")
        history1 = await chat_service.get_conversation_history(session_id)
        history2 = await chat_service.get_conversation_history(different_session_id)
        
        print(f"세션 1 상태: {history1}")
        print(f"세션 2 상태: {history2}")
        
        # 결과 요약
        print(f"\n🎉 멀티턴 대화 테스트 완료!")
        print(f"✅ 첫 번째 대화: {len(events1)}개 이벤트")
        print(f"✅ 두 번째 대화 (같은 세션): {len(events2)}개 이벤트")
        print(f"✅ 다른 세션 대화: {len(events3)}개 이벤트")
        print(f"✅ 메모리 기능: {history1.get('memory_enabled', False)}")
        
    except Exception as e:
        print(f"❌ 테스트 실패: {str(e)}")
        import traceback
        traceback.print_exc()

async def test_multi_turn_scenario():
    """실제 멀티턴 대화 시나리오 테스트"""
    
    print("\n🎭 멀티턴 대화 시나리오 테스트")
    print("=" * 50)
    
    try:
        chat_service = ChatService()
        session_id = "scenario-test-session"
        
        # 시나리오: 아이폰 구매 상담
        scenarios = [
            "아이폰 15 최저가 알려줘",
            "256GB 모델은 얼마야?",
            "아이폰 14와 비교해줘",
            "어떤 걸 추천해?",
            "128GB로 결정했어, 어디서 사는 게 좋을까?"
        ]
        
        for i, message in enumerate(scenarios, 1):
            print(f"\n👤 사용자 ({i}/5): {message}")
            
            request = ChatRequest(
                message=message,
                session_id=session_id
            )
            
            print("🤖 AI Assistant:")
            async for event in chat_service.process_message(request):
                if event.event_type == "message":
                    print(f"   {event.data}")
                elif event.event_type == "thinking":
                    print(f"   🤔 {event.data}")
                elif event.event_type == "search":
                    print(f"   🔍 {event.data}")
                elif event.event_type == "error":
                    print(f"   ❌ {event.data}")
            
            # 잠시 대기
            await asyncio.sleep(1)
        
        print(f"\n✅ 멀티턴 시나리오 테스트 완료!")
        
    except Exception as e:
        print(f"❌ 시나리오 테스트 실패: {str(e)}")

if __name__ == "__main__":
    print("🚀 멀티턴 대화 지원 Chat Integration 테스트 시작")
    
    # 기본 연결 테스트
    asyncio.run(test_chat_integration())
    
    # 멀티턴 시나리오 테스트
    asyncio.run(test_multi_turn_scenario()) 