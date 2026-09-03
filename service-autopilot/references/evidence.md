# 근거 매핑 — 무엇을 어디서 이식했고, 무엇을 왜 바꿨나

조사일: 2026-07-09 (웹 실측 — 스타 수는 GitHub API, 프로토콜은 원본 명령 프롬프트 파일 확인).
규칙: 여러 권위 출처가 수렴하거나 1차 출처(원문)가 확인된 것만 채택.

## 프레임워크 실측 (2026-07-09 기준, 2026-09-03 GitHub API 재확인 → 화살표 뒤 값)

| 프레임워크 | 스타 | 활성 | 이 스킬이 가져온 것 |
|---|---|---|---|
| [github/spec-kit](https://github.com/github/spec-kit) | 118.9k → 133.1k | 매우 활발 | /clarify 질문 프로토콜(5문항 상한·Impact×Uncertainty·객관식+추천), 9카테고리 택소노미, /analyze 교차검사(커버리지 0건 탐지), P1-only-MVP 스토리 원칙, "체크리스트는 요구사항의 유닛테스트" |
| [geekan/MetaGPT](https://github.com/geekan/MetaGPT) | 69.3k → 70.2k | 정체 (마지막 push 2026-01-21) | PRD 노드(목표≤3 직교·스토리 3~5·P0/P1/P2 풀), 시스템설계 노드(구현접근·classDiagram·sequenceDiagram), 태스크의 OpenAPI 산출, "Anything UNCLEAR" 필드 개념 |
| [bmad-code-org/BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD) | 50.3k → 52.6k | 매우 활발(v6) | fresh-context 적대적 리뷰("문제를 반드시 찾아라" + 거짓양성 필터 + 2회 수확체감), PASS/CONCERNS/FAIL 준비도 게이트, "각 문서가 다음 페이즈의 컨텍스트" |
| [buildermethods/agent-os](https://github.com/buildermethods/agent-os) | 5.0k | 보통 | 표준(컨벤션)을 스펙에 주입하는 3층 컨텍스트 관점 (→ 핸드오프 시 CLAUDE.md/BASE와 연결) |
| [ruvnet/claude-flow](https://github.com/ruvnet/claude-flow) | 63.6k | 매우 활발 | (채택 없음 — 메타 오케스트레이션이라 스코프 밖. SPARC 5단계는 spec-kit과 중복) |

**5개 전부 위협모델링·IaC·관측성 전용 단계 부재** → A4 위협모델·A7 OPS-DESIGN이 이 스킬의
고유 확장. 근거는 프레임워크가 아니라 실무 표준(아래)에서 직접 가져왔다.

## 실무 표준 이식

| 스킬 요소 | 출처 (원문 확인) |
|---|---|
| A4 문서 골격(Context/Goals·Non-goals/설계=트레이드오프/검토한 대안/Cross-cutting) | [Design Docs at Google](https://www.industrialempathy.com/posts/design-docs-at-google/) |
| A4 위협모델 4질문 프레임 | [Threat Modeling Manifesto](https://www.threatmodelingmanifesto.org/) |
| A4 STRIDE 6범주·대응 4택(Mitigate/Eliminate/Transfer/Accept)·trust boundary 절차 | [OWASP Threat Modeling Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html) |
| A5 에러 포맷 Problem JSON·스택트레이스 금지·URL 버저닝 회피·커서 페이지네이션·스코프 규약 | [Zalando RESTful API Guidelines](https://opensource.zalando.com/restful-api-guidelines/) (#176/#177/#115/#160/#225) + [RFC 9457](https://www.rfc-editor.org/rfc/rfc9457) |
| A5 멱등성(클라 생성 키·≥24h 보관·최초 응답 재생) | [Stripe Idempotent Requests](https://docs.stripe.com/api/idempotent_requests) |
| A6 Given/When/Then 정의·AC는 개발 전 존재 | [Cucumber Gherkin Reference](https://cucumber.io/docs/gherkin/reference) |
| A6 피라미드·"가능한 한 아래층으로"·contract test 레이어 | [Fowler — Practical Test Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html) |
| A7 SLI 유형별 표준·SLO 규칙(적게·100% 금지)·4 골든 시그널·"모든 알람은 조치 가능" | [Google SRE Book — SLO](https://sre.google/sre-book/service-level-objectives/) · [Monitoring](https://sre.google/sre-book/monitoring-distributed-systems/) |
| 블라인드스팟 P1(IoT) — SD 마모·전원·watchdog 15초 함정·OTA A/B·RTC 부재·X.509 신원 | [Mender — Pi in production](https://mender.io/blog/raspberry-pi-in-production) · [dzombak SD wear](https://www.dzombak.com/blog/2021/11/reducing-sd-card-wear-on-a-raspberry-pi-or-armbian-device/) · [AWS IoT Lens](https://docs.aws.amazon.com/wellarchitected/latest/iot-lens/) (IOTSEC 1·2, OTA·프로비저닝 원문) |
| 도메인 Lens 개념(도메인별 체크리스트가 공식 패턴이라는 근거) | [AWS Well-Architected Lenses](https://docs.aws.amazon.com/wellarchitected/latest/userguide/lenses.html) (IoT·SaaS·Serverless·ML 등 실존 + Custom Lens 공식 지원) |
| eval/ 전체(pairwise+스왑·binary 6차원·시드 10·해석 임계) | eval/PROTOCOL.md의 출처 절 참조 (MT-Bench·Anthropic·Hamel·ISO 29148) |

## 스킬 라우팅·형식 정렬 근거 (2026-09-03 추가)

| 출처 | 실측 (2026-09-03, GitHub API) | 이 스킬이 가져온 것 |
|---|---|---|
| [Anthropic — Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) · [anthropics/skills](https://github.com/anthropics/skills) skill-creator · [agentskills.io 스펙](https://agentskills.io/specification) | 173.3k★ | `metadata`(version/updated)·`argument-hint` 프론트매터, 본문에서 시간 민감 수치 제거(근거 파일로 이동), 참조 1단계 깊이, `evals/evals.json` 형식, description에 사용 시점 포함 |
| [Claude Code — Skills](https://code.claude.com/docs/en/skills) | 2.1.259 문서 | `when_to_use`·`context: fork`·`paths` 등 확장 필드 확인. `context: fork`는 미채택(아래 의도적 변경 6) |
| [affaan-m/everything-claude-code](https://github.com/affaan-m/everything-claude-code) (ecc) | 246.4k★, 설치 v1.10.0 (2026-04-09) | `references/skill-routing.md`의 1순위 스킬 대부분 (research-ops·product-lens·api-design·tdd-workflow·deployment-patterns·santa-method 등). 설치본이 5개월 구버전이므로 갱신 시 라우팅 재검사 |
| [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) | 121.6k★, MIT, v4.9.0, 마지막 push 2026-08-07 | 구현 단계(service-prompt-workflow BUILD·REVIEW)의 결정 사다리. 자체 벤치마크: 12개 기능 과제·n=4·Haiku 4.5에서 LOC −54%, 토큰 −22%, 비용 −20%, 시간 −27%, 안전 100% (`benchmarks/results/2026-06-18-agentic.md`) |
| [obra/superpowers](https://github.com/obra/superpowers) | 280.8k★, 미설치 (공식 마켓 `superpowers`) | 채택 없음 — 흡수 후보. README "외부 스킬 흡수 기준" 참조 |

## 의도적 변경 (출처와 다르게 한 것 — 이유 명시)

1. **질문 배치 1회** vs spec-kit의 "한 번에 정확히 1문항씩 순차": spec-kit은 대화형 CLI라 순차가
   자연스럽지만, 이 스킬의 1순위 요구는 **개입 최소화**(사용자 결정)다. 총량 5문항 상한·객관식·
   추천 기본값·즉시 반영은 그대로 유지하고 제시만 배치로 바꿨다. 트레이드오프: 앞 답변이 뒤 질문을
   바꾸는 연쇄는 포기 — 대신 충돌 시 GATE가 잡는다.
2. **MetaGPT 경쟁 분석(5~7개)·쿼드런트 차트 미채택**: RECON의 유사 솔루션 3~5개로 충분하고,
   쿼드런트는 장식성 높음(범위 절제 차원과 충돌). 필요 시 RECON에서 선택 적용.
3. **BMAD advanced elicitation(사용자가 렌즈 지정) 미채택**: 개입을 늘리는 방향이라 목적과 반대.
   같은 효과(다각 검토)는 GATE의 적대적 검토가 자동으로 수행.
5. **라우팅은 정적 표 + 스캔 스크립트, 동적 스캔 아님**: 매 단계 200개 넘는 description을 훑으면 토큰 비용과
   선택 흔들림이 크다. 표는 사람이 근거를 달아 유지하고, `_tools/skill_catalog.py`가 설치 여부·미배정만 기계적으로 검사한다.
6. **`context: fork` 미채택**: GATE·REVIEW의 fresh-context 검토는 Agent 도구 서브에이전트로 이미 구현돼 있고,
   파이프라인 내부 단계를 별도 스킬로 쪼개야만 `context: fork`를 쓸 수 있어 파일 수만 는다.
4. **OpenAPI 전문 생성 안 함**: MetaGPT는 태스크 단계에서 Full OpenAPI 3.0을 뽑지만, Google
   디자인독 원칙("형식 정의 전문 복붙 금지, 스케치만")과 충돌. 설계 단계는 스케치, 전문은 구현
   단계(service-prompt-workflow BUILD)로 미룸.

## 이 파일의 용도

스킬 규칙·템플릿을 바꾸려면: ① 바꿀 항목의 출처를 여기서 확인 ② 새 근거(수렴 출처)를 확보
③ eval/ 동결 시드로 회귀 평가 ④ 이 표와 버전을 갱신. 근거 없는 변경 금지.
