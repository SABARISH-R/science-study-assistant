# PRD: Science Study Assistant

Status: Draft v0.1 | Owner: Sabarish R

## 1. Problem
Students ask follow-up questions after science lessons, and teachers cannot answer all of them in class. Students turn to general chatbots, which can answer incorrectly and with high confidence. Teachers have no way to control what their students are told.

## 2. Users
- **Primary: secondary-school students (grades 8-12)** who need quick, correct answers while revising.
- **Secondary: science teachers** who want students to get answers consistent with the curriculum they teach.

## 3. Goals
1. Answers come only from teacher-approved notes, with the source shown.
2. The tool says "I don't know" rather than guess.
3. A teacher can add or edit a topic by editing a markdown file, with no code.

## 4. Non-goals (v1)
Quizzes, grading, student accounts, voice input, languages other than English, topics outside the pilot set.

## 5. Success metrics
| Metric | How measured | Target (to be set after interviews) |
|---|---|---|
| Retrieval accuracy | `eval/run_eval.py` on a held-out question set from real users | TBD |
| Correct refusal rate | Share of out-of-scope questions answered with "I don't know" | TBD |
| Helpfulness | Thumbs up/down after each answer | TBD |
| Teacher trust | Share of interviewed teachers who would let students use it | TBD |

Counter-metric: wrong-but-confident answers (reviewed by a teacher on a sample of logged questions).

## 6. Requirements
- **P0:** retrieve from notes, show source, decline off-topic questions, run offline.
- **P1:** optional LLM-written answer grounded in retrieved passages.
- **P2:** web UI, usage logging with consent, teacher dashboard of unanswered questions.

## 7. Key trade-offs
- **Extractive vs generated answers:** extractive is safer and cheaper but reads less naturally. v1 defaults to extractive, with generation optional.
- **TF-IDF vs embeddings:** TF-IDF needs no dependencies or network and is easy to explain; embeddings handle paraphrase better. Decision deferred until the eval set is large enough to compare them.
- **Refuse vs best-effort:** a false refusal frustrates a student, but a wrong answer misleads one. v1 favours refusing.

## 8. Risks
- Notes contain errors, so every topic needs teacher review.
- Threshold tuning: too high refuses valid questions, too low answers off-topic ones.
- Student data privacy if logging is added (collect only with consent, minimise data).

## 9. Launch plan
1. Interview 5+ teachers and 5+ students (see the interview guide).
2. Teacher-review the notes for the pilot topics.
3. Pilot with one class for two weeks and review logged questions weekly.
4. Decide go/no-go on the metrics above.

## 10. Open questions
Which topics do students ask about most? Do teachers prefer short or detailed answers? Is a refusal acceptable if it suggests where to look next?
