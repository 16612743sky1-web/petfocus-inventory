---
description: 배포 전 점검(deploy-check)을 한 뒤 커밋하고 GitHub에 올린다
---

deploy-check 스킬의 체크리스트대로 방금 수정한 내용을 점검해줘.

점검 순서:
1. `git status`와 `git diff`로 무엇이 바뀌었는지 보여준다.
2. 브라우저(Playwright, executablePath: '/opt/pw-browsers/chromium')로 수정한 도구를 직접 열어 콘솔 오류가 없는지, 핵심 흐름이 동작하는지 확인한다. (현장재고 index.html은 `python3 -m http.server`로 띄운다)
3. 데이터 규칙을 확인한다:
   - 현장재고(index.html): batch+increment, Firestore/로컬 두 분기, `esc()`, `FIREBASE_CONFIG` 불변
   - 재고/원가(stock-cost): records 재계산·soft delete·스키마 버전, 원가 검산(231,000원 / 개당 4,620원)

점검을 통과하면:
- 무엇을 왜 바꿨는지 한 줄로 한글 커밋 메시지를 만들어 커밋한다.
- 지정된 작업 브랜치에 푸시한다.

점검에서 콘솔 오류나 문제가 발견되면 **올리지 말고** 무엇이 문제인지 먼저 알려준다.
