# GitHub Actions 및 Discord 통합 설정 가이드

이 프로젝트는 GitHub Actions를 사용하여 테스트 자동화 및 코드 커버리지 측정을 수행하고, 그 결과를 Discord로 전송합니다.

## 1. Discord 웹훅 설정하기

1. Discord 서버에서 알림을 받을 채널을 선택합니다.
2. 채널 설정 > 통합 > 웹훅 생성을 클릭합니다.
3. 웹훅의 이름과 아이콘을 설정합니다.
4. "웹훅 URL 복사" 버튼을 클릭하여 URL을 복사합니다.

## 2. GitHub 저장소에 시크릿 추가하기

1. GitHub 저장소 페이지에서 "Settings" 탭을 클릭합니다.
2. 왼쪽 사이드바에서 "Secrets and variables" > "Actions"를 선택합니다.
3. "New repository secret" 버튼을 클릭합니다.
4. 이름 필드에 `DISCORD_WEBHOOK_URL`을 입력합니다.
5. 값 필드에 앞서 복사한 Discord 웹훅 URL을 붙여넣습니다.
6. "Add secret" 버튼을 클릭하여 저장합니다.

## 3. GitHub Actions 워크플로우 동작 확인

워크플로우는 다음 상황에서 자동으로 실행됩니다:

- **모든 브랜치로의 Push**: 코드가 푸시될 때마다 테스트가 실행됩니다.
- **main 브랜치로의 PR**: main 브랜치로 PR이 생성되거나 업데이트될 때 테스트가 실행됩니다.

워크플로우가 실행되면 Discord 채널에 다음 정보가 포함된 메시지가 전송됩니다:
- 테스트 성공/실패 여부
- 코드 커버리지 비율 (%)
- 이벤트를 트리거한 사용자
- 브랜치 및 커밋 정보

## 4. 추가 설정 (선택 사항)

### Codecov 연동

이 워크플로우는 [Codecov](https://codecov.io/)에도 커버리지 리포트를 업로드합니다. Codecov 연동을 원하시면:

1. [Codecov](https://codecov.io/)에 GitHub 계정으로 로그인합니다.
2. 해당 저장소를 Codecov에 추가합니다.
3. 필요한 경우 Codecov 토큰을 GitHub 시크릿에 추가합니다 (`CODECOV_TOKEN`).

### 배지 추가

README.md 파일에 테스트 상태 및 커버리지 배지를 추가하려면:

```markdown
![Tests](https://github.com/[username]/[repository]/actions/workflows/test-and-report.yml/badge.svg)
![Coverage](https://img.shields.io/codecov/c/github/[username]/[repository])
``` 