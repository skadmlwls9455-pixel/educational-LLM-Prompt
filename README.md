# Cyber Ethics NPC Prompts

**The system prompts behind the LLM feedback NPCs in a metaverse cyber-ethics
lesson for middle-school students, plus what I would change about them now.**

These prompts come from a capstone project that was later published:

> H. Kim, **U. Nahm**, J. Cho, "Cyber Ethics Education Program Based on
> Metaverse," *Proceedings of the KIICE Spring Conference 2025*, pp. 516–518.
> Outstanding Paper Award, KIICE Spring Conference 2025
> ([certificate](docs/kiice-2025-outstanding-paper-award.png), in Korean, May 23, 2025).

The program is a multiplayer Unity world where students walk through
scenarios on cyber violence and smartphone overuse and then post what they
would do on an in-game board. Each answer is saved to Google Sheets for the
teacher and also sent to an LLM (Mistral). The LLM replies in character as a
friendly NPC, and the reply appears in-game as a speech bubble.

This repo contains the three NPC system prompts I wrote for that feedback
step, in the original Korean and in English translation.

The prompts were first drafted in Google Docs in November 2024 and were added
to this repository later, so the repository's commit dates are more recent
than the prompts themselves. A screenshot of the original document's version
history (Korean, November 27–29, 2024) is in
[docs/prompt-draft-version-history-2024-11.png](docs/prompt-draft-version-history-2024-11.png).

## The three NPCs

| Topic | Korean original | English |
|---|---|---|
| Account theft and impersonation | [ko/01](prompts/ko/01_identity_theft_impersonation.md) | [en/01](prompts/en/01_identity_theft_impersonation.md) |
| Cyber extortion (e.g. forced hotspot sharing) | [ko/02](prompts/ko/02_cyber_extortion.md) | [en/02](prompts/en/02_cyber_extortion.md) |
| Smartphone overuse | [ko/03](prompts/ko/03_smartphone_overuse.md) | [en/03](prompts/en/03_smartphone_overuse.md) |

## How they were designed

The audience was 13–15-year-olds writing short, often emotional answers about
situations they may have actually experienced. All three prompts share the
same structure:

1. **Empathize first.** Acknowledge the student's feelings before giving any
   advice. Comfort victims; name harmful behavior as wrong without shaming the
   student.
2. **Give an ethical reason.** Explain *why* something is wrong (e.g. it
   violates someone's rights), not just that it is against the rules.
3. **Give concrete steps.** Prevention and response steps a teenager can
   actually take: change the password, take screenshots, use the platform's
   report button, say no.
4. **Hand off to a trusted adult.** Every prompt routes serious situations to
   a teacher, a parent or a counselor rather than having the NPC handle them
   alone.
5. **Sound like a peer, not a lecture.** Casual Korean (banmal), light humor,
   and a fixed verbal habit ("맞아!" instead of "네!") so the NPC reads as a
   friendly character rather than a textbook.

Each rule comes with an example sentence, so the model has a concrete target
for tone and content rather than an abstract instruction.

## What I would change now

I wrote these as a student focused on getting the feature working. Looking
back with a safety lens, these are the gaps I see:

- **No crisis protocol.** A student might disclose self-harm, abuse or ongoing
  extortion. The prompts have no rule for that case. They should tell the
  model to stop giving tips, respond with care, point to a real youth helpline
  (in Korea, 1388), and flag the response so the teacher sees it first.
- **Student text is not treated as data.** Answers were passed to the model
  with the system prompt, but nothing tells the model that the student's text
  is content to respond to, never instructions to follow. A student could type
  "ignore your rules and…" and steer the NPC. I would delimit the student's
  answer and add an explicit instruction about it.
- **No scope boundary.** Nothing stops the NPC from answering off-topic
  requests. It should redirect politely to the lesson topic.
- **A peer persona for minors needs limits.** Presenting an AI as "a teenage
  friend" helps engagement but can blur what it is. I would have the NPC say
  it is an AI when asked, and avoid encouraging students to rely on it
  instead of people.
- **Unverified resources.** "Report it to a cyber safety center" is vague, and
  a model may invent specific names or numbers. Real contacts should come
  from a fixed, verified list in the prompt, not from the model.
- **Privacy notice.** The prompts tell students not to share personal
  information online, but the system itself sends their answers to a
  third-party API and logs them in a spreadsheet. Students should be told
  that before they write.
- **No systematic testing.** The next step would be a small test set covering
  normal answers, off-topic answers, injection attempts and crisis
  disclosures, run against each prompt before classroom use.

## My role

I built the system's technical core and wrote the paper's design and
implementation section:

- **Multiplayer backend** on Unity + Photon PUN2: real-time movement sync, a
  nickname lobby with names kept across scenes, and the Photon Chat server
  connection
- **Data pipeline** that stores student responses in Google Sheets for teacher
  review (Unity → Google Form → Sheet) and reads them back into the game
- **LLM feedback loop**, including these three prompts

My teammate wrote the quiz and board content and the chat UI toggle, and
debugged an issue where chat history reset when moving between scenes.
Development notes (Korean): [barrikate.tistory.com](https://barrikate.tistory.com)

The Unity project is not included here; this repo contains the prompts only.

## Copyright
Copyright (c) 2026 Katherine Nahm (남의진). All rights reserved. See [LICENSE](LICENSE).
