# petfocus-inventory — 펫포커스 도구 모음

한우 강아지간식 제조·통신판매(펫포커스)에서 쓰는 사내 도구 모음.
서버 없이 정적 HTML로만 구성되며 **GitHub Pages**로 배포한다.

🔗 **라이브 주소:** https://16612743sky1-web.github.io/petfocus-inventory/

| 도구 | 주소 | 설명 |
|---|---|---|
| 펫포커스 현장재고 | https://16612743sky1-web.github.io/petfocus-inventory/ | Firestore 기반. 재고·입출고·이력·원가 (2인 현장용) |
| 재고/원가 관리 | https://16612743sky1-web.github.io/petfocus-inventory/stock-cost/ | RTDB 기반. 생산배치 원가·수율·판매 마진 |
| 상세페이지 생성기 | https://16612743sky1-web.github.io/petfocus-inventory/detail/ | 상세페이지용 AI 프롬프트 6단계 자동 생성 |

> ⚠️ **재고앱이 두 개**입니다. `현장재고`(루트)는 클라우드가 실제로 연결돼 지금 쓰는 앱이고,
> `재고/원가`(stock-cost)는 기능이 더 많지만 클라우드 미설정 버전입니다.
> 지금은 **둘 다 보관** 중이며, 하나로 합치거나 정리하는 건 천천히 결정합니다.

---

## 🚀 배포하는 법 (제일 자주 잊어버리는 것)

이 저장소는 **`main` 브랜치를 GitHub Pages가 자동으로 배포**한다.
→ **핵심 한 줄: 작업 내용을 `main`에 합치면(merge) 자동으로 배포된다.**

작업이 다른 브랜치(예: `claude/...`)에 있으면 **아직 라이브가 아니다.**

### 순서
1. GitHub 저장소 화면 → **`Contribute`** → **`Open pull request`**
2. **`Create pull request`** → **`Merge pull request`** (= `main`에 합쳐짐)
3. **1~2분 기다린 뒤** 라이브 주소를 강력 새로고침(`Ctrl`+`F5` / `Cmd`+`Shift`+`R`)

### 배포됐는지 확인
- 저장소 **`Deployments` → `github-pages`** 에 ✅ 초록불 + 방금 시각이면 성공.

---

## 개발 메모

- **도구 1개 = 폴더(또는 루트) 1개 = HTML 파일 1개.** 빌드 도구·프레임워크·npm 없음.
- 데이터는 브라우저 `localStorage` + Firebase(현장재고 Firestore / 재고원가 RTDB)에 저장.
- 현장재고 `index.html`은 Firebase dynamic import 때문에 `file://`로 열지 말고
  `python3 -m http.server`로 확인한다.
- 각 도구 사용법은 폴더의 `GUIDELINES.md`, 개발 원칙은 [`CLAUDE.md`](./CLAUDE.md) 참고.
