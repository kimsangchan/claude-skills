# 단계별 산출물 템플릿 (A0~GATE)

각 단계 진입 시 해당 블록을 읽고 그 구조대로 산출물을 생성한다. 섹션 구성은 전부 실측 출처가
있다 — PRD·설계는 MetaGPT ActionNode + spec-kit spec-template, 아키텍처 문서 골격은 Google
디자인 독, 위협모델은 Threat Modeling Manifesto 4질문 + OWASP STRIDE, API 계약은 Zalando
가이드라인 + RFC 9457 + Stripe, 테스트는 Cucumber Gherkin + Fowler 테스트 피라미드,
운영은 Google SRE Book. 매핑 상세는 `evidence.md`.

---

## A0. SEED — `00-seed.md`

```
# Seed — {{서비스 가칭}}
- 원문: {{사용자 입력 그대로}}
- 서비스 유형: {{IoT·엣지 / 웹 SaaS / 관제 / 모바일 / AI·LLM / 데이터 파이프라인 / 복합(목록)}}
- 주 도메인 / 인접 도메인: {{…}} / {{…}}
- 감지된 제약: {{입력에서 읽히는 것만 — 없으면 "없음"}}
- 로드할 블라인드스팟 프로파일: {{P1~P6 중 해당}}
- 강도: {{lite|full}} — 사유: {{SKILL.md 강도 신호 표의 어느 항목이 걸렸나 / 하나도 없음}}
- 기존 시스템: {{없음 / 저장소·시스템 경로 — 있으면 A1에 "현재 시스템 감사" 절을 추가}}
```
되묻지 않는다. 부족한 정보는 A1~A2가 채운다.

---

## A1. RECON — `01-recon.md`

`references/evidence-map.md`의 소스 매핑을 따라 조사한다. 최소 섹션:

```
## 도메인 업무 흐름 — 이 산업이 실제로 어떻게 돌아가는가 (출처)
## 이해관계자 — 누가 쓰고, 누가 돈을 내는가 (출처)
## 규제·표준 — 반드시 준수해야 하는 것 (출처; 해당 없음도 확인 근거)
## 유사 솔루션 3~5개 — 오픈소스+상용, 실제 기능 범위 (출처)
## 스택 후보 — 후보별 근거·트레이드오프 (스타 수는 근거의 하나일 뿐, fit은 사용자 제약 매칭)
## 현재 시스템 감사 (기존 시스템이 있을 때만) — 실제 코드·스키마·설정에서 읽은 제약을 file:line으로 (추측 금지, Explore 서브에이전트 위임 가능)
```
전 항목 출처 URL 필수. 웹 검색으로 현재 시점 데이터 확인.

---

## A2. INTERROGATE — `02-blindspot-register.md`

`references/blindspot-checklists.md`를 읽고 3패스 실행. register 형식:

```
# 블라인드스팟 레지스터 — {{서비스}}
스캔: 공통 10축 + STRIDE 6범주 + 프로파일 {{P#}} ({{N}}항목)

| 축/항목 | 상태 | 처리 | 근거·출처 |
|---|---|---|---|
| 1. 기능 범위 | Clear | — | seed에서 확정 |
| P1. SD카드 마모 | Missing | **Asked → Q1** | Impact: 현장 출동 / Uncertainty: 설치 환경 미상 |
| P1. watchdog | Missing | Assumed: HW watchdog 활성(15초 이내) | mender.io Pi 체크리스트 |
| …전 축 전 항목… |

## 질문 배치 (최대 5) — {{제시 일시}}
### Q1. {{심문 질문}}
| 옵션 | 내용 | 근거·트레이드오프 |
|---|---|---|
| A (추천) | {{…}} | {{추천 이유}} |
| B | {{…}} | {{…}} |
→ 답: {{A/B/… 또는 "무응답 → 추천안 Assumed 채택"}}

## 반영 기록
Q1 답 → {{영향받은 산출물·결정}} (decision-log #{{n}})
```

질문 승격은 Impact × Uncertainty 상위 5개까지. 배치 1회 제시 후 즉시 register·decision-log에
반영하고 저장(원자적). 무응답 항목은 추천안을 `Assumed(무응답)`로.

---

## A3. PRD — `03-prd.md`

구성 출처: MetaGPT write_prd(목표≤3·스토리 3~5·P0/P1/P2 풀) + spec-kit spec-template
(P1-only-MVP 원칙, Given/When/Then 엣지케이스, 측정 가능 SC) + `quality-decomposition.md`.

```
# PRD — {{서비스명}}
버전: v1.0 — 개정하면 올리고, 04~07 머리의 `기준 03 v` 를 같은 턴에 갱신 (SKILL.md 규칙 9)
## 배경 (RECON 요약 3~5줄 + 링크)
## 제품 목표 — 최대 3개, 서로 직교
## 유저 스토리 — 3~5개, 우선순위 P1/P2/P3
   각: "As a {{역할}}, I want {{행동}}, so that {{가치}}" + 독립 테스트 가능
   **P1만 구현해도 성립하는 MVP가 되도록** 쪼갠다 (spec-kit 원칙)
## 요구사항 풀 — FR-001… 표: | ID | 요구사항 | 우선순위 P0/P1/P2 | 출처(스토리/규제) |
## 엣지케이스 — 핵심 흐름당 최소 3개, Given/When/Then으로 기대 동작까지
## 성공 기준 — SC-001… 전부 측정 가능·기술중립·pass/fail (질적 표현은 quality-decomposition으로 변환)
## UI 방향 (화면 있으면) — ux-principles-kr.md 적용, frontend-design-taste dial 지정
## 범위 밖 (non-goals) — "합리적으로 목표일 수 있었지만 명시적으로 제외한 것" (Google 디자인독 정의)
## 가정 목록 — register의 Assumed 전부 요약 링크
## 상수 표 (단일 출처) — | 이름 | 값 | 단위 | 근거 | — 상한·기간·임계·용량은 여기에만. 04~07은 이름으로 참조하고 값을 다시 쓰지 않는다 (규칙 9)
## 화면 스케치 (화면 있으면, 1장) — 핵심 화면 1개를 ASCII 또는 mermaid로, 빈/로딩/에러 상태를 표기 (실행가능성 — 2026-09 스모크 S1 패인)
## 미결정 — **게이트 통과 조건: 0건** (남으면 A2로 회귀; `scripts/check_package.py`가 "미정·TBD·추후" 표기를 스캔한다)
```

---

## A4. ARCHITECT — `04-architecture.md`

골격은 Google 디자인 독(트레이드오프 중심, "형식 정의 전문 복붙 금지, 스케치만"),
다이어그램은 MetaGPT design_api(classDiagram + sequenceDiagram), 위협모델은 Manifesto 4질문 + STRIDE.

```
# 아키텍처 — {{서비스명}}
버전: v1.0 · 기준 03 v{{03의 현재 버전}}
## Context & Scope — 시스템이 놓이는 환경 (기존 시스템·제약 포함, 간결하게)
## Goals / Non-goals
## 설계 (트레이드오프를 드러내는 게 핵심)
### 시스템 컨텍스트 다이어그램 — mermaid (전체 지형에서 신규 시스템의 위치)
### 구현 접근 — 난점 분석 + 선택 프레임워크/컴포넌트 (MetaGPT Implementation approach)
### 컴포넌트 구조 — mermaid classDiagram 또는 컴포넌트 다이어그램
### 데이터 흐름 — mermaid sequenceDiagram (핵심 시나리오 2~3개, 위에서 정의한 컴포넌트 이름만 사용)
### 데이터 저장 — 설계 결정에 관련된 부분만 (전체 스키마는 A5)
## 검토한 대안 — 대안별 트레이드오프 + 왜 최종안인가 (Google 디자인독 필수 섹션)
## 위협모델 (Cross-cutting: 보안)
### ① 무엇을 만드는가 — DFD + trust boundary 표시 (mermaid)
### ② 무엇이 잘못될 수 있는가 — STRIDE 표:
   | 자산/경계 | S | T | R | I | D | E | — 각 셀: 유효한 위협 or "해당없음(근거)"
### ③ 무엇을 할 것인가 — 위협별: Mitigate/Eliminate/Transfer/Accept(사유) + 대책
### ④ 충분한가 — 상위 리스크 3개 재검토 + 잔여 리스크 명시
## Cross-cutting: 관측성·프라이버시 — 한 단락씩이라도 강제 기술 (상세는 A7)
```
게이트: STRIDE 6범주가 모든 trust boundary에서 검토됨(해당없음도 근거).

---

## A5. CONTRACT — `05-api-contract.md`

체크 항목 출처: Zalando RESTful API Guidelines(규칙 번호), RFC 9457, Stripe.

```
# API 계약 & 데이터 스키마 — {{서비스명}}
버전: v1.0 · 기준 03 v{{03의 현재 버전}}
## 규약 (전 엔드포인트 공통)
- 에러 포맷: RFC 9457 Problem JSON (type/title/status/detail/instance), 스택트레이스 노출 금지 (Zalando #176·#177)
- 버저닝: 미디어타입 또는 헤더. **URL 버저닝 회피** (Zalando #115). 스펙 파일은 semver
- 페이지네이션: 커서 기반 선호, offset 회피 (Zalando #160)
- 멱등성: 부작용 있는 POST는 Idempotency-Key 헤더 — 클라 생성 키, 서버 ≥24h 보관,
  재시도 시 최초 응답 그대로 재생 (Stripe 방식)
- 네이밍·권한: 경로 kebab-case, 권한 스코프 `<모듈>:<자원>:<행위>` (Zalando #225와 동형)
## 엔드포인트 표
| ID | 메서드 경로 | 요청(핵심 필드) | 응답 | 주요 에러(RFC 9457 type) | 권한 스코프 |
## OpenAPI 스케치 — 핵심 리소스 2~3개만 YAML (전문은 구현 단계에서; Google 디자인독 "스케치만" 원칙)
## ERD — mermaid erDiagram (엔티티·관계·핵심 컬럼·소프트삭제 여부)
## 데이터 규칙 — 금액=정수(원)/Decimal, 시각=UTC ISO8601, 식별자 정책, 보존 기간
## 커버리지 매핑 — | FR-ID | 담당 엔드포인트/이벤트 | — P0·P1 요구사항 매핑 0건 = 결함 (spec-kit /analyze)
```

---

## A6. TEST-DESIGN — `06-test-design.md`

출처: Cucumber Gherkin 공식 정의, Fowler 테스트 피라미드.

```
# 테스트 설계 — {{서비스명}}
버전: v1.0 · 기준 03 v{{03의 현재 버전}}
## 원칙
- AC는 개발 시작 전에 존재한다. 각 시나리오는 처음엔 반드시 실패해야 한다 (TDD 게이트)
- 피라미드: unit 다수 → integration → contract(API 계약 대상) → E2E 최소 (~70/20/10)
- "가능한 한 아래층으로" — 하위에서 검증된 것을 상위에서 반복 금지 (Fowler)
## 수용 기준 → 시나리오 변환표
| SC/FR ID | Gherkin 시나리오 (Given/When/Then) | 레이어 | 데이터/목킹 |
— PRD의 SC·P0/P1 FR **전부**가 최소 1개 시나리오를 갖는다 (누락 0 게이트)
— 정상 경로 + 경계값 + 실패 경로(엣지케이스 표에서) 포함
## 계약 테스트 — A5 엔드포인트 표 기준: 스키마 검증·에러 포맷·멱등성 재시도
## E2E 후보 — 돈·안전·법이 걸린 핵심 여정만 2~3개
## 리스크 기반 커버리지 목표 — 위협모델 상위 리스크·P0 경로는 상향
```

---

## A7. OPS-DESIGN — `07-ops-design.md`

출처: Google SRE Book(SLI/SLO·골든 시그널·알람 철학), 런북 실무 템플릿, IoT는 P1 프로파일 기본값.

```
# 배포·운영 설계 — {{서비스명}}
버전: v1.0 · 기준 03 v{{03의 현재 버전}}
## 배포
- 런타임·형상: {{서버/컨테이너/엣지}} + Dockerfile/compose 스케치 (엣지면 A/B 파티션·서명 검증)
- CI/CD 단계: lint → test(A6 스위트) → build → (contract test) → deploy → smoke
- 설정·비밀: 환경변수 외부화, 비밀 저장 위치, 폐쇄망이면 오프라인 설치 경로
## 관측성
- SLI 선택 (서비스 유형 표준: 사용자 대면=가용성·지연·처리량 / 저장소=+내구성 / 파이프라인=처리량·E2E 지연 / 공통=정확성)
- SLO — **가능한 한 적게**, 100% 금지, 현재 성능이 아니라 사용자 기대 기준 (SRE 규칙)
- 4 골든 시그널 계측 계획: Latency(성공/실패 구분)·Traffic·Errors·Saturation
- 로깅 전략: 무엇을(이벤트 목록)·어디에(로컬/중앙, **엣지면 SD 마모 대책 필수**)·얼마나(보존·로테이션)·개인정보 마스킹
## 알림
- "모든 알람은 조치 가능해야 한다"(SRE) — 알람 표: | 조건 | 심각도 | 수신자 | 연결 런북 |
- 알람:런북 = 1:1. 증상 기반(사용자 체감)으로 울리고, 원인 지표는 대시보드로
## 장애·복구
- 시나리오 표 (상위 3~5): | 장애 | 감지 방법 | 영향 | 복구 절차(복붙 명령 수준) | RTO/RPO |
- 백업: 무엇을·주기·보관처·**복원 리허설 주기**
- 런북 골격: 메타(알람 연결) → 트리거·영향 → 진단(명령) → 해결 → 에스컬레이션 → 검증 → 롤백
## 착수 자산 (실행가능성 — 2026-09 스모크 S1 패인)
- 디렉터리 구조 스케치: 최상위 2단계까지, 디렉터리마다 역할 한 줄
- `.env.example`: 키 이름과 설명만. **값은 어떤 산출물에도 쓰지 않는다**
- 첫 작업 3개 = 워킹 스켈레톤: 핵심 여정 하나를 입력→저장→조회까지 얇게 끝까지 뚫는 작업. Impact×Uncertainty가 큰 것부터
```
게이트: 로그·백업·복구 각각 "어디에·얼마나·어떻게"가 답변됨.

---

## GATE — `08-readiness-report.md` (fresh context 서브에이전트, `model=opus` 이상 — `model-routing.md`)

적대적 검토 프롬프트 (BMAD adversarial review + spec-kit /analyze 이식):

```
<role>적대적 검토관. 이 문서들을 만든 사람이 아니다. "괜찮아 보인다" 금지 —
문제를 반드시 찾아라. 단 지적마다 심각도와 근거를 붙여라.</role>
<inputs>00~07 산출물 전부 + `python scripts/check_package.py autopilot/{{slug}}` 출력 (먼저 실행한다. CRITICAL이 있으면 고친 뒤 GATE)</inputs>
<check>
- 커버리지 공백: FR→엔드포인트, SC→테스트 시나리오 매핑 0건 항목 (CRITICAL)
- 모호성: 측정 불가 표현, 미결정 사항 잔존 (HIGH)
- 불일치: 문서 간 용어 드리프트, 스택 충돌, 다이어그램↔계약 불일치 (HIGH)
- 절대규칙 위반: 근거 없는 추천, register 미마킹 축 (CRITICAL)
- 중복·과잉: 같은 결정의 상충 기술, YAGNI 위반 (MEDIUM)
</check>
<output>발견 목록(심각도순, 문서:섹션 지목) + 판정 PASS / CONCERNS(사유) / FAIL(재실행 대상 단계)</output>
```

- 지적은 **반영 전에 타당성 필터링** — 적대 모드는 거짓 양성을 정기적으로 낸다 (BMAD 문서의 경고).
  재검토는 최대 1회 (예산 규칙 — SKILL.md 실행 절차 4). 두 번째도 FAIL이면 CONCERNS로 마감한다.
- **lite 강도**: 서브에이전트 없이 메인이 `check_package.py` 출력 + 위 <check> 항목을 자기 점검하고 08에 기록한다.
- 리포트 말미에 **핸드오프 블록**을 생성한다:

```
## 구현 핸드오프 (service-prompt-workflow SPEC 입력)
/service-prompt-workflow 로 다음을 실행:
<inputs>autopilot/{{slug}}/03-prd.md (요구사항·상수 표), 05-api-contract.md, 08-readiness-report.md (착수 조건·첫 작업 3개)</inputs>
<references>04-architecture.md, 06-test-design.md, 07-ops-design.md — 필요할 때만 읽는다</references>
<first_task>SPEC.md 작성 — 위 문서를 진실원으로, 낯선 구현자 실행 가능 수준(≥7/10)</first_task>
<then>superpowers 설치 시 `superpowers:writing-plans` → 첫 작업 3개(워킹 스켈레톤)부터. brainstorming은 생략 — 이 프롬프트를 붙여 넣은 것이 설계 승인이다.</then>
{{UI 있으면}} BUILD·REVIEW에서 frontend-design-taste dial={{…}} 적용
<model_hints>
opus: {{판단 집약 — INV 불변식·동시성·인증·마이그레이션에 걸린 FR}}
sonnet: {{패턴 반복 — CRUD·화면·RED 테스트 작성·설정 파일}}
haiku: {{기계적 — 문구·리네임·포맷}}
</model_hints>  (분류 기준: references/model-routing.md 하단 표)
```
