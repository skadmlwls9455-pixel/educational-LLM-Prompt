"""NPC 프롬프트 v2 정적 검사. API 키 없이 돈다.

검사 항목:
  - 세 프롬프트의 안전 블록이 _safety_block.md와 글자 하나까지 같은지
  - 각 프롬프트에 페르소나, 수업 주제, 답변 원칙, 안전 규칙이 있는지
  - 프롬프트에 나오는 전화번호가 모두 검증된 연락처 목록 안에 있는지
  - ko/en 프롬프트 파일 구성이 같은지

사용법: python3 tests/lint_prompts.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
V2 = ROOT / "prompts" / "v2"

# 안전 블록의 연락처 목록과 맞춰 둘 것. 번호를 추가하면 여기도 고친다.
VERIFIED_NUMBERS = {"1388", "#1388", "109", "117", "#0117", "112", "1599-0075"}
# 연락처가 아닌 숫자: 비밀번호 예시, 말풍선 글자 수 제한.
NOT_CONTACTS = {"12345", "300"}

SAFETY_HEADING = {"ko": "## 안전 규칙", "en": "## Safety rules"}
REQUIRED = {
    "ko": ["맞아!", "수업 주제:", "## 답변 원칙", "<student_answer>", "[SAFETY_FLAG]", "AI"],
    "en": ["맞아!", "Lesson topic:", "## Response principles", "<student_answer>", "[SAFETY_FLAG]", "AI"],
}
PHONE_RE = re.compile(r"#?\d[\d-]+\d")


def strip_comment(text):
    return re.sub(r"<!--.*?-->\n?", "", text, flags=re.S)


def phone_numbers(text):
    # 목록 번호("1.")나 "3~5" 같은 한두 자리 숫자는 정규식에서 이미 빠진다.
    return {m.group(0) for m in PHONE_RE.finditer(text)} - NOT_CONTACTS


def lint():
    errors = []
    names = {}
    for lang in ("ko", "en"):
        folder = V2 / lang
        block = strip_comment((folder / "_safety_block.md").read_text(encoding="utf-8")).strip()
        prompts = sorted(p for p in folder.glob("[0-9]*.md"))
        names[lang] = [p.name for p in prompts]
        if len(prompts) != 3:
            errors.append(f"{lang}: 프롬프트가 3개가 아님 ({len(prompts)})")
        for p in prompts:
            text = p.read_text(encoding="utf-8")
            rel = p.relative_to(ROOT)
            idx = text.find(SAFETY_HEADING[lang])
            if idx < 0:
                errors.append(f"{rel}: '{SAFETY_HEADING[lang]}' 구간 없음")
            elif text[idx:].strip() != block:
                errors.append(f"{rel}: 안전 블록이 _safety_block.md와 다름")
            for needle in REQUIRED[lang]:
                if needle not in text:
                    errors.append(f"{rel}: '{needle}' 없음")
            for num in phone_numbers(text) - VERIFIED_NUMBERS:
                errors.append(f"{rel}: 검증 목록에 없는 번호 '{num}'")
    if names.get("ko") != names.get("en"):
        errors.append(f"ko/en 파일 구성이 다름: {names}")
    return errors


if __name__ == "__main__":
    errs = lint()
    for e in errs:
        print("FAIL", e)
    print("OK" if not errs else f"{len(errs)} problem(s)")
    sys.exit(1 if errs else 0)
