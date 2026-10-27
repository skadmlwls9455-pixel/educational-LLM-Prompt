---
name: npc-review
description: "NPC 프롬프트 v2 전체 검토 — 작성자 수정, 안전 검토, QA 실행을 순서대로 돌리고 결과를 정리한다."
argument-hint: "[01 | 02 | 03 | all] [수정 요청 내용]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Agent, AskUserQuestion, Bash(python3 tests/*)
---

# NPC Review

인자: 대상 NPC 번호(기본 `all`)와, 있으면 수정 요청.

## 1단계: 현재 상태

`python3 tests/lint_prompts.py`를 돌려 결과를 보여준다. 실패가 있으면 그것부터 고칠지 사용자에게 묻는다.

## 2단계: 작성 (수정 요청이 있을 때만)

`npc-writer` 에이전트를 호출한다. 대상 파일 경로(`prompts/v2/ko/..`, `prompts/v2/en/..`)를 프롬프트에 명시한다.
수정 요약을 사용자에게 보여주고 승인받는다.

## 3단계: 안전 검토

`child-safety-reviewer` 에이전트를 호출한다. `문제` 항목이 있으면 선택지로 정리해 사용자에게 묻고,
고르면 2단계로 돌아가 반영한다. `확인 필요` 항목(예: 연락처 유효성)은 사용자에게 그대로 전달한다.

## 4단계: QA

`prompt-qa-tester` 에이전트를 호출한다.

## 5단계: 요약

린트 결과, 안전 검토 결과, 평가 결과(돌렸는지 여부 포함), 남은 할 일을 짧게 정리한다.
커밋은 사용자가 시킬 때만 한다.
