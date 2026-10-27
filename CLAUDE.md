# Cyber Ethics NPC Prompts — 작업 가이드

메타버스 사이버 윤리 수업(중학생 대상)의 LLM 피드백 NPC 프롬프트 레포.
구조와 작업 방식은 [Claude Code Game Studios](https://github.com/Donchitos/Claude-Code-Game-Studios)
(MIT)의 "역할별 에이전트 + 경로별 규칙 + 검증 게이트" 방식을 이 레포 규모에 맞게 줄여서 가져왔다.

## 구조

- `prompts/ko/`, `prompts/en/` — 2024년 11월 원본(v1)과 번역. **역사 기록이므로 고치지 않는다.**
- `prompts/v2/ko/`, `prompts/v2/en/` — 개선판. 실제로 고치는 곳.
  - `_safety_block.md` — 세 프롬프트가 공유하는 안전 규칙. 세 파일의 `## 안전 규칙` 구간과 글자까지 같아야 한다.
- `tests/` — `lint_prompts.py`(정적 검사), `npc_eval_cases.json`(평가 세트), `run_eval.py`(모델 평가)
- `docs/v2-integration.md` — 게임(Unity) 쪽에서 해야 하는 연동 규칙

## 에이전트

| 에이전트 | 맡는 일 |
|---|---|
| `npc-writer` | NPC 말투, 공감, 조언 내용. `prompts/v2/` 작성 |
| `child-safety-reviewer` | 위기 대응, 프롬프트 인젝션, 개인정보, 연락처 검증. 검토만 함 |
| `prompt-qa-tester` | 평가 세트 케이스 추가, 린트/평가 실행과 결과 정리 |

전체 검토는 `/npc-review` 스킬로 돌린다 (작성 → 안전 검토 → QA 순서).

## 작업 규칙

- 사용자 주도: 질문 → 선택지 → 결정 → 초안 → 승인. 파일을 쓰기 전에 무엇을 어디에 쓸지 먼저 보여준다.
- 사용자가 시키지 않으면 커밋하지 않는다.
- 프롬프트를 고친 뒤에는 항상 `python3 tests/lint_prompts.py`를 돌린다. 통과하지 않으면 끝난 게 아니다.
- 안전 블록은 `_safety_block.md`를 먼저 고치고, ko/en 세 프롬프트에 똑같이 반영한다. ko를 고치면 en도 고친다.
- 연락처(전화번호, 기관명)는 안전 블록 목록과 `tests/lint_prompts.py`의 `VERIFIED_NUMBERS`에 있는 것만 쓴다.
  새 연락처는 공식 출처를 사용자에게 확인받은 뒤에만 추가한다.
- 검사 스크립트는 관찰만 출력한다. 말투·공감의 질은 사람이 판정한다.
- 새 검사(게이트)를 추가하면, 일부러 틀린 입력으로 실패하는 것을 먼저 확인한다.

@.claude/rules/npc-prompts.md
