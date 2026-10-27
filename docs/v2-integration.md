# v2 프롬프트 게임 연동 가이드

v2 프롬프트(`prompts/v2/`)는 게임 쪽 코드가 아래 네 가지를 해줘야 제대로 동작한다.
Unity 프로젝트는 이 레포에 없으므로, 여기에는 연동 규칙만 적는다.

## 1. 학생 답변을 태그로 감싸서 보내기

시스템 프롬프트는 파일 내용 그대로, 학생 답변은 user 메시지로 보낸다.
학생 답변은 반드시 `<student_answer>` 태그로 감싸고, **감싸기 전에 학생 글 안의
`<student_answer>` / `</student_answer>` 문자열을 지운다.** 지우지 않으면 학생이
태그를 닫고 지시를 끼워 넣을 수 있다 (평가 세트 `inj-leak` 케이스).

```csharp
// C# (Unity) 예시
using System.Text.RegularExpressions;

static string WrapStudentAnswer(string answer)
{
    string cleaned = Regex.Replace(answer, @"</?\s*student_answer\s*>", "", RegexOptions.IgnoreCase);
    return "<student_answer>\n" + cleaned + "\n</student_answer>";
}
```

`tests/run_eval.py`의 `wrap_student_answer`가 같은 규칙의 Python 버전이다.

## 2. `[SAFETY_FLAG]` 처리

모델이 위기 신호(자해, 학대, 진행 중인 협박 등)를 보면 답변 맨 앞에 `[SAFETY_FLAG]`를 붙인다.
게임은 다음을 해야 한다.

1. 말풍선에 띄우기 전에 `[SAFETY_FLAG]` 문자열을 지운다.
2. Google Sheets에 저장할 때 `flagged` 열을 `TRUE`로 기록한다 (Google Form에 항목 하나 추가).
3. 교사용 시트는 `flagged`가 `TRUE`인 행을 맨 위에 보이도록 정렬하거나 조건부 서식으로 강조한다.

모델은 위기 신호를 놓칠 수 있다. 플래그는 교사의 확인을 돕는 보조 장치이고,
교사가 모든 답변을 읽는 절차를 대신하지 않는다.

## 3. 쓰기 전에 개인정보 안내 띄우기

학생 답변은 외부 AI 서비스(Mistral)로 전송되고 교사용 시트에 저장된다.
게시판 입력창 위나 입장 시 아래 문구를 보여준다.

> 여기에 쓴 글은 선생님이 볼 수 있도록 저장되고, AI 친구의 답장을 만들기 위해 외부 AI 서비스로 보내져.
> 이름, 학교, 전화번호, 주소, 계정 아이디는 쓰지 마. AI 친구의 답장은 틀릴 수도 있으니,
> 진짜 힘든 일은 꼭 선생님이나 부모님께 직접 말해줘.

## 4. 말풍선 길이

프롬프트는 3~5문장, 300자 정도로 답하라고 한다. 모델이 넘길 수 있으므로 말풍선은
스크롤되거나 넘치는 글을 잘라 "..."로 끝내되, `[SAFETY_FLAG]` 답변은 자르지 않는다.

## 연락처 확인

안전 블록의 연락처(1388, 109, 117, 112, ECRM, 스마트쉼센터 1599-0075)는 2026년 10월 기준으로 적었다.
수업 전에 각 기관 공식 사이트에서 번호가 바뀌지 않았는지 다시 확인하고,
바뀌었다면 `_safety_block.md`, 세 프롬프트, `tests/lint_prompts.py`의 `VERIFIED_NUMBERS`를 함께 고친다.
