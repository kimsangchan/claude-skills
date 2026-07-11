---
name: frontend-design-taste
description: |
  웹 UI를 설계·구현할 때 "AI 티 안 나는" 고급 프론트엔드 결과를 내기 위한 디자인 취향 하네스.
  React·Tailwind·Zustand 스택에 특화(다른 스택도 적용 가능). 대시보드·관제·SaaS 내부화면·랜딩 등
  화면을 만들거나 다시 디자인할 때, 색/그림자/타이포/레이아웃/모션을 정할 때, "디자인이 밋밋하다/
  AI스럽다"를 고칠 때 사용. 프로젝트별로 밀도·모션 "dial"을 정하고, 하드룰과 anti-slop을 강제한다.
  MengTo/Skills의 design-taste-frontend를 이식·일반화. service-prompt-workflow의 BUILD·REVIEW가 참조.
---

# Frontend Design Taste (프론트엔드 디자인 취향)

**목표: 어느 서비스든 "기본 템플릿 티" 안 나는, 의도된 고급 UI를 내는 것.**

한 벌의 dial + 프로파일 + 하드룰로, 대시보드부터 랜딩까지 일관된 취향을 강제한다.
구체 토큰(그림자·상태색·폰트·룩업맵)은 `references/tokens.md`에 있다.

## Use When (언제)

- 새 화면/컴포넌트를 만들거나 기존 UI를 다시 디자인할 때
- 색·그림자·타이포·간격·레이아웃·모션을 정해야 할 때
- "밋밋하다 / AI가 만든 것 같다 / 정보가 안 읽힌다"를 고칠 때
- `service-prompt-workflow`의 BUILD·REVIEW에서 프론트가 포함될 때 (자동 참조)

## 1. Dial 정하기 (프로젝트 시작 시 한 번)

세 축을 1~10으로 고정한다. **애매하면 사용자에게 한 번만 묻는다**(어떤 성격의 화면인가).

- **VISUAL_DENSITY** — 1 미술관(여백 최대) ↔ 10 조종석(데이터 최대 밀집)
- **MOTION_INTENSITY** — 1 정적 ↔ 10 시네마틱
- **DESIGN_VARIANCE** — 1 대칭·체계적 ↔ 10 파격·표현적

## 2. 프로파일 (프리셋 — 여기서 골라 시작)

| 프로파일 | DENSITY | MOTION | VARIANCE | 언제 |
|---|---|---|---|---|
| **관제/대시보드** (SCADA·텔레메트리·admin) | **8** | **2** | 3 | 실시간 데이터·모니터링·표·차트 위주 |
| **제품/앱 UI** (SaaS 내부 화면) | 5 | 4 | 4 | 폼·리스트·설정·업무 흐름 |
| **마케팅/랜딩** | 3 | 6 | 6 | 소개·전환 유도·스토리텔링 |

> NEUROS/SiWeb 같은 관제 화면 = **관제/대시보드 프로파일**이 기본. 아래 "Cockpit 모드" 규칙이 걸린다.

## 3. 하드룰 (위반 시 반려)

### 레이아웃
- `h-screen` 금지 → `min-h-[100dvh]`.
- flex 퍼센트 계산 금지 → **CSS Grid** (`grid grid-cols-1 md:grid-cols-3 gap-6`).
- 폭 컨테이너로 잡기 (`max-w-7xl mx-auto`). 반응형·모바일 접힘 보장.

### 타이포그래피
- **대시보드/소프트웨어 UI에 세리프 금지.** 고급 산세리프 페어링 사용(`Geist`+`Geist Mono`, `Satoshi`+`JetBrains Mono` 등 — `references/tokens.md`).
- **모든 숫자는 모노스페이스**(`font-mono`) — 정렬·판독성. 특히 관제.
- 거대 H1·`Inter` 남발 금지.

### Cockpit 모드 (VISUAL_DENSITY ≥ 8)
- 작은 패딩. **카드 박스 남발 금지** — `border-t`/`divide-y`/여백으로 논리 그룹화(z-index로 띄울 실제 이유가 있을 때만 카드).
- 데이터는 촘촘히, 1px 선으로 구분. 지표는 박스에 가두지 말고 숨 쉬게.

### 색 & 테마
- 순수 `#000000` 금지 → 근접 무채색(Zinc-950 계열).
- 네온 글로우·과한 그라디언트 금지.
- **테마 토큰을 쓴다.** 프로젝트에 CSS 변수 테마가 있으면 하드코드 색 대신 그 토큰(예: NEUROS는 `var(--color-*)` + `data-theme` 다크/라이트).
- 상태색(정상/경고/위험/정보)은 `references/tokens.md`의 의미쌍을 사용.

### 상태 관리 (Zustand/React)
- 격리된 UI 상태는 로컬 `useState`/`useReducer`. **전역 상태는 깊은 prop-drilling 회피용으로만** — 아무 데나 전역 금지.
- Pre-Flight: "전역 상태가 임의로 쓰였나, 아니면 prop-drilling 회피 목적인가?" 확인.

### 의존성 & Tailwind 버전 [필수]
- 라이브러리(`framer-motion`·`lucide-react`·`zustand` 등) import 전 **`package.json`에 실제 존재하는지 확인.** 있다고 가정 금지.
- **Tailwind 버전 잠금**: `package.json` 먼저 확인. v3 프로젝트에 v4 문법 쓰지 말 것. v4면 `postcss.config.js`에 `tailwindcss` 플러그인 말고 `@tailwindcss/postcss`(또는 Vite 플러그인) 사용.

### 모션 & 성능
- 애니메이션은 `transform`/`opacity`만. `top/left/width/height` 애니 금지.
- grain/noise는 `fixed … pointer-events-none` 레이어에만.
- `z-50` 남발 금지. 스크롤 감지는 `IntersectionObserver`(스크롤 리스너 금지). `useEffect` 정리(cleanup) 필수.

## 4. Avoid — AI 티(slop) 금지 목록

- 가짜 데이터 금지: "John Doe"/"Acme"/`99.99%` → 유기적 값(`47.2%`, `18 of 43`).
- 필러 카피 금지: "Elevate/Seamless/Unleash", "직관적인", "간편한".
- **동적 클래스명 금지**: `"text-" + color` (퍼지 시 사라짐) → **룩업맵**(`references/tokens.md`).
- 상태 누락 금지: **빈 / 로딩 / 에러 / (실시간이면) stale** 상태를 모두 구현. 관제 데이터는 끊긴다.

> 정성 표현("토스처럼", "고급스럽게")이 요구사항에 있으면 **측정 가능 기준으로 변환**한 뒤 진행.

## 5. Pre-Flight Check (완료 선언 전)

- [ ] 빈/로딩/에러(+실시간이면 stale) 상태가 모두 있나?
- [ ] 모바일에서 접히나(반응형 보장)?
- [ ] 숫자는 `font-mono`인가? 세리프를 안 썼나?
- [ ] 색이 테마 토큰(하드코드 아님)인가? 순수 #000·네온을 안 썼나?
- [ ] 동적 클래스명 대신 룩업맵인가(퍼지 안전)?
- [ ] `min-h-[100dvh]`·Grid를 썼나? `h-screen`·flex 퍼센트를 안 썼나?
- [ ] import한 라이브러리가 `package.json`에 실제 있나? Tailwind 버전이 맞나?
- [ ] 애니는 transform/opacity만인가? `useEffect` 정리를 했나?
- [ ] 전역 상태가 prop-drilling 회피 목적인가(남용 아님)?
- [ ] 가짜 데이터·필러 카피가 없나?

## 6. service-prompt-workflow와 통합

- **BUILD(5)**: 프론트 구현 시 이 스킬의 dial·프로파일·하드룰을 적용해 코드를 쓴다.
- **REVIEW(7)**: 이 스킬의 Pre-Flight + `service-prompt-workflow`의 `anti-patterns.md` C절을 리뷰 루브릭으로 함께 적용.
- 두 스킬은 겹치는 anti-slop을 공유하되, 이 스킬은 **적극적 "이렇게 만들라"**(dial·토큰), 저쪽은 **소극적 "하지 말라"** 담당.

## 참조
- `references/tokens.md` — 그림자 3종·의미 상태색쌍·룩업맵 패턴·폰트 페어링 (복붙). 프론트 구현/리뷰 시 읽는다.

출처: MengTo/Skills `design-taste-frontend`·`tailwindcss`·`beautiful-shadows`·`minimalist-ui` 이식·일반화.
현재 버전: v0.1.0
