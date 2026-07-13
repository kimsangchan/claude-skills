# 개인 Claude Code 스킬 모음

`~/.claude/skills/`에 두고 쓰는 **개인 제작 스킬 저장소**다. 어느 PC에서든 이 저장소를
`~/.claude/skills`로 clone하면 Claude Code가 세션 시작 시 자동으로 인식한다.

스킬은 이름을 몰라도 된다 — 각 스킬의 `description`을 보고 Claude가 상황에 맞게 자동 적용한다.
직접 부르고 싶으면 `/스킬이름 인자` 형태로 호출한다.

## 스킬 간 관계 (큰 그림)

```
[아이디어만 있고 뭘 만들지 막연함]          [뭘 만들지 정해짐]              [화면이 포함됨]
service-autopilot                →   service-prompt-workflow   →   frontend-design-taste
"기획·설계 자동 생성"                  "구현을 단계별로 명령"           "AI 티 안 나는 UI 강제"
산출: PRD·아키텍처·API계약·테스트설계      SPEC→PLAN→BUILD→VERIFY→SHIP      BUILD·REVIEW 단계에서 자동 참조
```

비유하면: **autopilot이 건축 설계도를 그리고, prompt-workflow가 시공 순서를 지휘하고,
design-taste가 인테리어 품질 기준을 잡는다.**

---

## 1. service-autopilot — 기획·설계 오토파일럿

**한 줄 아이디어를 "구현 착수 가능한 설계 패키지"로 바꾼다.** 사용자가 빈칸을 채우는 게 아니라
AI가 스스로 조사하고, 사각지대를 찾아 덮고, 가정으로 못 덮는 위험한 결정만 객관식 최대 5문항으로
**딱 1번** 묻는다.

- **언제 쓰나**: 신규 서비스/기능 기획, PRD 필요, 기술스택 추천, MVP 범위 결정, 도메인을 모르는
  상태의 착수, 위협모델·API 설계·배포/모니터링 설계.
- **파이프라인**: A0 SEED(아이디어 정규화) → A1 RECON(도메인 조사) → A2 INTERROGATE(사각지대 심문,
  질문 배치 1회) → A3 PRD → A4 아키텍처+위협모델(STRIDE) → A5 API계약+ERD → A6 테스트설계 →
  A7 배포/관측성 → GATE(새 컨텍스트 적대적 자기검토).
- **산출물**: `00-seed.md` ~ `08-readiness-report.md` + `decision-log.md` (9개 파일, 생성 즉시 저장).
- **근거**: spec-kit·MetaGPT·BMAD 등 검증된 프레임워크와 ISO 29148·STRIDE·AWS Well-Architected의
  실측 이식 (`references/evidence.md`).

**사용 예시:**

```
> 회의실 예약 서비스 만들고 싶어
```

이 한 줄이면 자동 발동한다. 조사 → (필요하면 객관식 질문 1회) → 설계 문서 9개가 폴더에 생성되고,
마지막에 "다음 명령"(service-prompt-workflow로 넘기는 핸드오프 프롬프트)까지 알려준다.
실제 산출 예시는 `service-autopilot/eval/runs/run-20260709-smoke/meeting-room-booking/`에 있다
(회의실 예약 서비스를 실제로 돌린 결과물 전체).

명시 호출: `/service-autopilot 라즈베리파이로 IP 카메라 모니터링 서비스`

---

## 2. service-prompt-workflow — 구현 실행 워크플로우

**"뭘 만들지 아는" 순간부터 배포까지, AI 코딩 에이전트에게 낭비 없이 명령하는 9단계 실행 하네스.**
기획이 아니라 **제작**을 다룬다. 각 단계에 하드 게이트(통과 조건)가 있어서 게이트를 못 넘으면
다음 단계로 안 간다.

- **언제 쓰나**: 서비스/기능 제작 시작, "이거 어떻게 시작하지", 프롬프트를 어떻게 써야 할지 막힐 때,
  SPEC·PLAN·구현·리뷰·배포 명령이 필요할 때. (기획이 막연하면 먼저 service-autopilot.)
- **파이프라인**: 0 BASE(저장소 지침) → 1 FRAME(무엇을·왜) → 2 EXPLORE(코드 먼저 읽기) →
  3 SPEC(자기완결 명세) → 4 PLAN(작업 쪼개기) → 5 BUILD(작은 증분+테스트) → 6 VERIFY(실행 증거) →
  7 REVIEW(새 컨텍스트 적대적 리뷰) → 8 SHIP(커밋·PR) → 9 REFLECT(회고→지침 반영).
- **라우터 내장**: 사용자 한 문장을 보고 어느 단계에서 진입할지 스스로 판단한다.
  ("구현해" → BUILD, "리뷰해줘" → REVIEW, "커밋해" → SHIP)
- **핵심 규칙 10개(ETHOS)**: 명시적 지시, 이유 제공, 탐색·구현 분리, 명세 파일화, 작게 쪼개 검증,
  검증 루프 닫기(증거 요구), 테스트 우선, 사용자 주권, 컨텍스트 위생, 단순함 우선.
- **복붙 프롬프트 템플릿**: 단계별 명령 문구가 `references/prompt-templates.md`에 있다.

**사용 예시:**

```
> /service-prompt-workflow 사용해서 하위 모델에서 구현할 기획까지만 세우고 푸시해
```

(실제로 LOD 프로젝트의 네이버 카페 수집기를 이렇게 만들었다 — SPEC과 tasks.md를 만들어
하위 모델이 이어받게 한 사례.)

```
> 이 스펙대로 구현해            ← 라우터가 BUILD 단계로 진입
> 이거 진짜 되는지 확인해       ← VERIFY 단계로 진입
```

---

## 3. frontend-design-taste — 프론트엔드 디자인 취향

**웹 UI에서 "AI가 만든 티(slop)"를 없애고 의도된 고급 결과를 강제하는 취향 하네스.**
React·Tailwind·Zustand에 특화(다른 스택도 적용 가능). MengTo/Skills의 design-taste-frontend를
이식·일반화한 것.

- **언제 쓰나**: 새 화면/컴포넌트 제작, 기존 UI 리디자인, 색/그림자/타이포/레이아웃/모션 결정,
  "밋밋하다 / AI스럽다 / 정보가 안 읽힌다"를 고칠 때. service-prompt-workflow의 BUILD·REVIEW에
  프론트가 포함되면 자동 참조된다.
- **작동 방식**: 프로젝트 시작 시 3개 dial(밀도·모션·파격)을 1~10으로 고정하고, 프로파일
  (관제/대시보드=밀도8, 제품 UI=밀도5, 랜딩=밀도3)을 골라 시작한다. 이후 하드룰 위반은 반려.
- **하드룰 예시**: 대시보드에 세리프 금지, 모든 숫자는 모노스페이스, 순수 검정(#000) 금지,
  `h-screen` 금지, 카드 박스 남발 금지(관제 모드), 라이브러리 import 전 package.json 실존 확인.
- **anti-slop 목록**: "John Doe"/"Acme"/99.99% 같은 가짜 데이터 금지 → 유기적 값(47.2%, 18 of 43) 사용 등.
- **구체 토큰**(그림자·상태색·폰트 페어링)은 `references/tokens.md`.

**사용 예시:**

```
> 텔레메트리 대시보드 화면 만들어줘
```

→ 자동으로 관제/대시보드 프로파일(밀도 8, 모션 2)이 걸리고, 숫자 모노스페이스·1px 구분선·
카드 최소화 같은 규칙이 강제된다.

```
> 이 랜딩 페이지 너무 AI스러워, 고쳐줘
```

→ anti-slop 목록과 대조해 가짜 데이터·네온 그라디언트·거대 H1 남발 등을 걷어낸다.

---

## 4. catch-up — 세션 이어받기 부트스트랩

**새 세션·다른 AI 툴이 이전 작업 맥락을 토큰 낭비 없이 "바로 따라잡게(catch up)" 프로젝트 구조를
1회로 세팅한다.** 핵심 원칙은 Progressive Disclosure(Anthropic) — 항상 읽히는 층은 얇게, 상세는 필요할 때만.

- **언제 쓰나**: 프로젝트 시작/정리 시, "세션마다 맥락 다시 설명하기 귀찮다", "새 세션이 이전 걸
  기억 못 한다", "CLAUDE.md가 너무 커졌다", "Antigravity·Cursor에서도 지시 없이 프로젝트를 이해시키고 싶다".
- **세팅하는 구조**: 얇은 `CLAUDE.md`(행동규칙 + `@AGENTS.md`) · `AGENTS.md`(크로스툴 단일 원본 —
  Claude Code·Antigravity v1.20.3+·Cursor 공유) · `NEXT.md`(다음-할일) + SessionStart 훅(그 블록만 주입) ·
  폴더별 `CLAUDE.md`(그 폴더 만질 때만 로드) · `WORKLOG.md`(히스토리 분리).
- **5 페이즈**: SCAN(현황) → CLASSIFY(스코프·이관계획) → PROPOSE(diff 제시) → APPLY(승인 후 clean-tree
  git 체크포인트) → VERIFY(자동 점검). **비파괴·가역**(`git revert` 한 번).
- **근거**: Anthropic Progressive Disclosure/Just-in-time, Claude Code 중첩 CLAUDE.md 온디맨드 로딩,
  AGENTS.md 오픈표준, Memory Bank 패턴 (`catch-up/references/PRINCIPLES.md`).

**사용 예시:**

```
> /catch-up
```

→ 현재 프로젝트를 스캔해 "이렇게 바꾸겠다"는 diff를 **먼저 보여주고**, 승인하면 얇은 컨텍스트 구조를
세팅한다. 부작용이 있어 **사용자 호출 전용**(모델이 알아서 실행하지 않음).
다른 툴 어댑터까지: `/catch-up --tools antigravity,cursor`

---

## 5. solution-planner — ⚠ 폐기됨 (2026-07-09)

service-autopilot으로 대체됐다. **새 기획 요청에는 쓰지 않는다.**
과거 산출물(`solution-planning/` 디렉토리, ICT inspection-run-ux 등)을 해석할 때만 참조용으로 남겨둔다.

---

## learned/ — 자동 학습 스킬 자리

세션에서 추출된 학습 스킬이 쌓이는 폴더 (현재 비어 있음).

---

## 다른 PC에서 쓰는 법

```bash
# 새 PC에서 1회 (기존 ~/.claude/skills가 비어있거나 없을 때)
git clone https://github.com/kimsangchan/claude-skills "$HOME/.claude/skills"
```

Windows PowerShell:

```powershell
git clone https://github.com/kimsangchan/claude-skills "$env:USERPROFILE\.claude\skills"
```

## 평소 동기화 루틴

- 스킬을 **고친 PC에서**: `git add . && git commit -m "무엇을 왜" && git push`
- **다른 PC에서** 세션 시작 전: `git pull`
- 원칙: 원본은 GitHub 하나. 두 PC에서 동시에 같은 스킬을 고치지 않는다(충돌 방지).
