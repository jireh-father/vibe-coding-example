# GitHub Actions 및 Discord 통합 설정 가이드

이 문서에서는 GitHub Actions를 사용하여 테스트 자동화 및 커버리지 리포트를 Discord로 전송하는 방법을 설명합니다.

## 1. Discord Webhook URL 설정

1. Discord 서버에서 채널 설정을 열고 "통합" 탭으로 이동합니다.
2. "웹후크 만들기" 버튼을 클릭합니다.
3. 웹후크의 이름과 아이콘을 설정하고 "웹후크 URL 복사" 버튼을 클릭합니다.

## 2. GitHub 저장소에 시크릿 추가

1. GitHub 저장소 페이지에서 "Settings" 탭으로 이동합니다.
2. 왼쪽 사이드바에서 "Secrets and variables" > "Actions"를 클릭합니다.
3. "New repository secret" 버튼을 클릭합니다.
4. 이름을 `DISCORD_WEBHOOK_URL`로 입력하고, 값으로 이전에 복사한 Discord 웹후크 URL을 붙여넣습니다.
5. "Add secret" 버튼을 클릭하여 저장합니다.

## 3. 워크플로우 동작 확인

GitHub Actions 워크플로우는 다음 이벤트에서 실행됩니다:

- **Push**: 모든 브랜치에 대한 Push 이벤트
- **Pull Request**: main 브랜치로의 Pull Request 이벤트

워크플로우가 실행되면 다음 작업을 수행합니다:

1. 테스트 실행 및 코드 커버리지 측정
2. 코드 커버리지 배지 생성
3. 결과를 Discord 채널로 전송

## 4. 워크플로우 결과 해석

Discord에 전송되는 메시지에는 다음 정보가 포함됩니다:

- **상태**: 테스트 성공/실패 여부
- **커버리지**: 코드 커버리지 비율 (%)
- **실행자**: 워크플로우를 트리거한 사용자
- **브랜치**: 이벤트가 발생한 브랜치
- **커밋**: 해당 커밋에 대한 링크

## 5. 문제 해결

워크플로우 실행 중 문제가 발생하면 다음을 확인하세요:

1. GitHub Actions 탭에서 워크플로우 실행 로그 확인
2. `DISCORD_WEBHOOK_URL` 시크릿이 올바르게 설정되었는지 확인
3. Discord 웹후크가 유효한지 확인 