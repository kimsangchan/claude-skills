---
name: service-prompt-workflow
description: |
  어떤 서비스·기능이든 AI 코딩 에이전트에게 "효율적인 프롬프트"로 명령하는 9단계 실행 워크플로우.
  무엇을 만들지 아는 상태에서 착수할 때 사용 — 서비스/기능 제작 시작, "이거 어떻게 시작하지",
  프롬프트를 어떻게 써야 할지 막힐 때, SPEC·PLAN·구현·리뷰·배포 명령이 필요할 때, 스택 선정 후
  실제 빌드로 넘어갈 때. 기획 자체가 막연하거나 도메인을 모르면 먼저 service-autopilot을 쓴다.
  gstack 스프린트 모델 + Anthropic/OpenAI/GitHub spec-kit 검증 기법을 종합한 근거 기반 하네스.
argument-hint: "[요청 한 문장 또는 단계명]"
metadata:
  version: "0.3.0"
  updated: "2026-09-04"
---

# Service Prompt Workflow (서비스 프롬프트 워크플로우)

**"뭘 만들지 아는" 순간부터 배포까지, 각 단계를 효율적 프롬프트로 명령하는 실행 하네스.**

이 스킬은 기획이 아니라 **제작**을 다룬다. 서비스를 어떻게 프롬프트로 지시해야 낭비 없이
정확히 만들어지는지를 9단계 파이프라인 + 단계별 복붙 프롬프트 템플릿으로 표준화한다.

## service-autopilot과의 관계 (역할 분담)

```
[뭘 만들지 모를 때 / 설계가 필요할 때]        [설계 패키지가 있을 때]
service-autopilot                    →     service-prompt-workflow (이 스킬)
SEED→RECON→INTERROGATE→PRD→ARCHITECT       Frame→Explore→Spec→Plan→Build→Verify→Review→Ship→Reflect
→CONTRACT→TEST-DESIGN→OPS-DESIGN→GATE
산출: 03-prd / 04-architecture(+위협모델) / 05-api-contract(+ERD) / 06-test-design / 07-ops-design
                    └────────── 이 산출물이 아래 SPEC 단계의 입력이 된다 ──────────┘
```

- 도메인·범위·스택이 불확실하면 **service-autopilot을 먼저** 돌려 설계 패키지를 만든다.
- 설계 패키지(또는 이미 아는 요구사항)가 있으면 **이 워크플로우로 실행**한다.
- 둘은 경쟁이 아니라 앞뒤로 물린다. `03~07` 산출물은 그대로 `SPEC` 입력으로 쓴다.
- (구) solution-planner는 deprecated. 그 blueprint(05/06/07)를 입력으로 쓴 기존 문서도 여전히 유효하다.

## 절대 규칙 (ETHOS — 모든 단계에 주입)

출처가 여럿에서 수렴하는 원칙만 규칙으로 승격한다. 근거는 `references/evidence.md`.

1. **명시적으로 지시한다.** 원하는 출력·형식·제약을 구체적으로 쓴다. "알아서 잘"은 금지.
   에이전트는 "똑똑하지만 우리 관례를 모르는 신입"이다 — 맥락이 없으면 헤맨다. *(Anthropic·OpenAI)*
2. **이유(why)를 준다.** 규칙엔 근거를 붙인다. 이유를 알면 에이전트가 일반화한다. *(Anthropic)*
3. **탐색·계획과 구현을 분리한다.** 사소한 한 줄 수정이 아니면 코드부터 짜지 않는다. 먼저 읽고, 계획하고, 명세한 뒤 구현한다. *(Claude Code explore→plan→code, spec-kit, Harper Reed)*
4. **명세와 계획을 파일로 남긴다.** SPEC.md → tasks.md는 진실원(source of truth)이다. 구현은 깨끗한 새 컨텍스트에서 명세를 보고 시작한다. *(spec-kit, gstack /spec)*
5. **작게 쪼개 각 단계를 개별 검증한다.** 큰 덩어리 한 번에 금지. 작은 증분 + 검증. *(spec-kit /implement, prompt chaining)*
6. **루프를 닫는다.** 에이전트에게 스스로 검증할 수단(테스트·빌드·린트·스크린샷)을 준다. "된 것 같다"가 아니라 **증거**(실행 결과)를 요구한다. 오류는 억누르지 말고 근본 원인을 고친다. *(Claude Code)*
7. **테스트 우선.** 실패하는 테스트/수용 기준을 먼저 쓰고 통과시킨다. *(Claude Code, spec-kit Article III)*
8. **사용자 주권.** AI는 추천하고 사용자가 결정한다. 두 모델이 동의해도 "신호일 뿐 증명이 아니다." 방향 전환은 반드시 묻는다 — **한 번에 하나씩**. *(gstack User Sovereignty)*
9. **컨텍스트 위생.** 무관한 작업 사이엔 `/clear`. 같은 지시를 2번 고쳐도 안 되면 세션을 비우고 프롬프트를 다시 쓴다. 조사·리뷰는 서브에이전트에 위임해 메인 컨텍스트를 아낀다. *(Claude Code, Context engineering)*
10. **단순함 우선.** 가장 단순한 해법부터. 복잡도는 효과가 증명될 때만 추가한다. BUILD에서는 ponytail 결정 사다리(필요한가→이미 있나→표준 라이브러리→네이티브→설치된 의존성→한 줄→최소 코드)로 강제한다. *(Building effective agents, spec-kit anti-abstraction, ponytail)*

## 파이프라인 (9단계)

각 단계는 **목적 · 하드 게이트(통과 조건) · 산출물**을 갖는다. 게이트를 못 넘으면 다음 단계로 가지 않는다.
각 단계의 **복붙 프롬프트 블록**은 `references/prompt-templates.md`에, 단계별로 호출할 전문 스킬은 `references/skill-routing.md`에 있다.

| # | 단계 | 목적 | 하드 게이트 (넘어야 다음 단계) | 산출물 |
|---|---|---|---|---|
| 0 | **BASE** | 저장소 상시 지침 | CLAUDE.md/AGENTS.md 존재·최신 | 저장소 지침 파일 |
| 1 | **FRAME** | 무엇을·왜 | 사용자·문제·성공기준·범위경계 확정 (모르면 solution-planner) | frame 메모 |
| 2 | **EXPLORE** | 코드·패턴 먼저 읽기 | 관련 파일 최소 1곳을 실제로 읽고 인용 (plan mode, 수정 금지) | 탐색 노트(file:line) |
| 3 | **SPEC** | 자기완결 명세 | "낯선 구현자가 실행 가능" 점수 ≥ 7/10, 모호성 0 | `SPEC.md` |
| 4 | **PLAN** | 순서 있는 작업 | 각 작업에 검증 가능한 완료기준 + 테스트 우선 표기 | `tasks.md` |
| 5 | **BUILD** | 구현 | 작은 증분마다 테스트 통과 · 기존 패턴 모방 | 코드 + 테스트 |
| 6 | **VERIFY** | 실행 검증 | 실행 결과(테스트/빌드/스크린샷) **증거** 첨부 | 검증 로그 |
| 7 | **REVIEW** | 적대적 검토 | 새 컨텍스트 리뷰어가 diff+기준만 보고 통과 | 리뷰 결과 |
| 8 | **SHIP** | 배포 | 증분 커밋 + 설명형 메시지(한글) + PR | 커밋·PR |
| 9 | **REFLECT** | 회고·학습 | 배운 것 → CLAUDE.md/decision-log 반영 | 학습 기록 |

### 라우터 (요청 → 단계 매핑)

사용자 한 문장을 받아 어느 단계에서 진입할지 판단한다. 의심스러우면 앞 단계로 내려간다
(잘못된 조기 착수보다 한 단계 되돌아가는 게 싸다 — gstack 라우터 원칙).

- "새 서비스/기능 만들자", "어떻게 시작하지" → **1 FRAME** (도메인 모르면 service-autopilot)
- "이 코드 어디를 고쳐야 해?", "구조부터 보자" → **2 EXPLORE**
- "명세 써줘", "PRD/스펙 만들자", blueprint 있음 → **3 SPEC**
- "작업 쪼개줘", "할 일 목록" → **4 PLAN**
- "구현해", "이 스펙대로 만들어" → **5 BUILD**
- "이거 진짜 되는지 확인", "테스트 돌려" → **6 VERIFY**
- "리뷰해줘", "버그 없나 봐줘" → **7 REVIEW**
- "커밋/PR 만들어" → **8 SHIP**
- "회고", "뭘 배웠지", "CLAUDE.md 갱신" → **9 REFLECT**

## 실행 절차

1. 라우터로 진입 단계를 정한다. 필요하면 사용자에게 **한 번에 하나** 확인한다.
2. `references/skill-routing.md`에서 그 단계의 행을 읽어 설치된 스킬을 호출한다(없으면 대체 열). 사용 기록은 decision-log 한 줄.
   서브에이전트에 위임하는 작업은 `references/model-routing.md`의 작업 클래스로 `model`을 고른다
   (PLAN에서 tasks.md에 `model:` 태그 → BUILD 위임 시 그대로, REVIEW 정확성은 `opus` fresh). 기록 줄에 모델을 병기한다.
3. 해당 단계의 프롬프트 블록을 `references/prompt-templates.md`에서 가져와 빈칸(`{{...}}`)을 채운다.
4. 하드 게이트를 확인한다. 못 넘으면 그 단계에 머문다.
5. 산출물을 파일로 남긴다 (대화에만 두지 않는다).
6. 다음 단계로. 완료 상태는 `DONE / DONE_WITH_CONCERNS / NEEDS_CONTEXT` 중 하나로 명시한다.

코드를 쓰는 단계(BUILD)와 보는 단계(REVIEW)는 ponytail을 함께 적용한다 — BUILD 진입 시 `ponytail:ponytail`
(미설치면 `references/skill-routing.md`의 내장 사다리), REVIEW에서 `/code-review` 뒤 `ponytail:ponytail-review`.
정확성 리뷰 1회 + 복잡도 리뷰 1회를 넘기지 않는다.

프론트엔드가 포함된 단계(SPEC·BUILD·REVIEW)는 두 가지를 함께 적용한다:
- **적극적 지침** — `frontend-design-taste` 스킬(있으면)의 dial·프로파일·하드룰·토큰으로 "이렇게 만들라".
- **소극적 금지** — `references/anti-patterns.md`의 slop 체크리스트를 리뷰 루브릭으로.

## 참조 파일

- `references/prompt-templates.md` — 단계별 XML 구조 복붙 프롬프트 블록. 각 단계 진입 시 읽는다.
- `references/skill-routing.md` — 단계별 스킬 라우팅 표 + ponytail 배선 + 충돌 우선순위. 각 단계 진입 시 해당 행을 읽는다.
- `references/model-routing.md` — 작업 클래스(판단 집약/패턴 반복/기계적/검증/리뷰) → 모델 등급(opus/sonnet/haiku) 표 + 승급 규칙. PLAN과 서브에이전트 위임 전에 읽는다.
- `references/anti-patterns.md` — AI slop/거짓 진척 체크리스트 · anti-sycophancy · 리뷰 루브릭. REVIEW와 프론트 작업 시 읽는다.
- `references/evidence.md` — 각 규칙·단계의 출처 매핑(gstack·Anthropic·OpenAI·spec-kit·Harper Reed·MengTo). 규칙을 바꿀 때 읽는다.

버전·갱신일은 프론트매터 `metadata`. 라우팅·ponytail 배선 변경 시 `eval/` 대리 A/B로 확인.
