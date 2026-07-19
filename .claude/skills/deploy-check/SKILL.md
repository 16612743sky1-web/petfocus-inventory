---
name: deploy-check
description: petfocus-inventory의 정적 HTML 도구(현장재고 index.html, stock-cost, detail)를 수정한 뒤 GitHub Pages에 올리기 전 점검하는 체크리스트. "배포", "올려줘", "커밋", "확인해줘", HTML 수정 마무리 시점에 사용.
---

# 배포 전 점검 (deploy-check)

petfocus-inventory는 서버 없이 정적 HTML만으로 GitHub Pages에 배포된다.
빌드 과정이 없어서 문법 실수나 깨진 화면이 그대로 라이브로 나간다.
그래서 커밋/푸시 전에 아래를 반드시 확인한다.

## 이 저장소의 도구

| 파일 | 도구 | 라이브 주소 |
|---|---|---|
| `index.html` | 펫포커스 현장재고 (Firestore, 입출고/이력) | `.../petfocus-inventory/` |
| `stock-cost/index.html` | 재고/원가 관리 (RTDB, 생산배치 원가·수율) | `.../petfocus-inventory/stock-cost/` |
| `detail/index.html` | 상세페이지 프롬프트 생성기 | `.../petfocus-inventory/detail/` |

## 1. 무엇을 고쳤는지 먼저 확인
- `git status` 와 `git diff` 로 실제 바뀐 파일과 내용을 본다.
- 의도한 파일만 바뀌었는지 확인한다. (실수로 다른 도구 파일을 건드리지 않았는지)

## 2. 브라우저로 실제 열어서 확인 (가장 중요)
자동 테스트가 없으므로 눈으로 확인하는 것이 유일한 안전장치다.
Playwright로 파일을 직접 열어 콘솔 오류와 핵심 흐름을 점검한다.
(executablePath: '/opt/pw-browsers/chromium')
※ `index.html`(현장재고)는 Firebase dynamic import 때문에 `file://`가 아니라
`python3 -m http.server` 로 띄워서 확인한다.

- **콘솔에 빨간 오류(Error)가 없는지** — 있으면 배포 금지. (익명 인증 미설정 `console.warn`은 허용)
- 수정한 도구의 **핵심 흐름이 실제로 동작하는지**:
  - `index.html` (현장재고): 입고 1건 저장 → 재고 탭 증가 → 이력에서 삭제 → 재고 원복
  - `stock-cost/index.html` (재고/원가): 매입 → 생산 → 판매 → 재고 반영 → 새로고침 후 값 유지
  - `detail/index.html` (상세페이지 생성기): 상품 입력 → 6단계 프롬프트 생성 → 새로고침 유지
- 모바일 폭(390px)에서 레이아웃이 깨지지 않는지.

## 3. 데이터 저장 규칙을 깼는지 확인
고친 도구의 CLAUDE.md/GUIDELINES 핵심 원칙을 위반하지 않았는지 본다.
- **현장재고(index.html)**: 재고 증감은 batch+increment(하드룰), Firestore/로컬 두 분기 모두 구현,
  `esc()` 없는 innerHTML 삽입 금지, `FIREBASE_CONFIG` 블록 건드리지 않기.
- **재고/원가(stock-cost)**: 재고는 records에서 매번 재계산(`computeStock()`), 삭제는 soft delete
  (`deleted:true`), 스키마 변경 시 `petfocus_v1` 키 버전업 + `load()` 마이그레이션.
- 공통: 고객 개인정보(주소·전화)를 데이터 모델에 추가하지 않는다 (공개 URL 동기화 전제).

## 4. 원가 검산 (stock-cost 또는 원가 계산 로직을 건드렸을 때만)
기준값: 우피10kg·식초2L·스틱50·포장50·건조12h·인시4
→ 배치 총원가 **231,000원**, 50개 생산 시 개당 **4,620원**.
이 값이 나오지 않으면 계산 로직이 틀린 것이다.

## 5. 커밋 & 배포
위가 모두 통과하면:
- 명확한 한글 커밋 메시지로 커밋한다. (무엇을 왜 바꿨는지)
- 푸시하면 GitHub Pages가 자동 반영한다. 1~2분 뒤 실제 URL에서 다시 확인한다.

## 하지 말 것
- 확인 없이 "될 거예요" 하고 푸시하지 않는다.
- 콘솔 오류가 남아있는 채로 배포하지 않는다.
- 여러 도구를 한 커밋에 섞지 않는다. (한 커밋 = 한 가지 변경)
