# Science Study Assistant

A small, testable study aid that answers secondary-school science questions **only from a vetted set of notes**, and says "I don't know" when the notes don't cover the question. Built as a product experiment: the code is simple on purpose, and the interesting part is the product thinking in [`docs/`](docs).

## Problem

Teachers who introduce hands-on or immersive science content (for example VR lab modules) get many follow-up questions after class. General chatbots answer confidently even when wrong, which is a poor fit for classrooms. This project tests a narrower idea: a tutor that is **grounded in teacher-approved notes** and **declines to guess**.

## What it does

- Splits topic notes in `data/kb/` into sections and ranks them against a question with TF-IDF (standard library only).
- **Extractive mode (default, no API key):** returns the best-matching passage with its source.
- **LLM mode (optional):** if `ANTHROPIC_API_KEY` is set, sends only the retrieved passages to the Messages API with an instruction to answer from them or say it doesn't know. Set `TUTOR_MODEL` to choose the model. Falls back to extractive mode on any error.
- Refuses off-topic questions using a minimum-relevance threshold.

Topics covered: plate tectonics, ocean floor, colligative properties, electroplating, protein synthesis.

## Run it

```bash
git clone https://github.com/SABARISH-R/science-study-assistant.git
cd science-study-assistant
PYTHONPATH=src python -m tutor.cli "How are ocean trenches formed?"
PYTHONPATH=src python -m tutor.cli          # interactive mode
```

## Test and evaluate

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
PYTHONPATH=src python eval/run_eval.py
```

`eval/questions.json` holds 20 questions with the topic each should retrieve. The baseline run measured **top-1 topic accuracy 19/20 and top-3 20/20**. Treat this as a smoke test, not a benchmark: the questions and notes were written by the same person, so scores are optimistic. Next step is evaluating with questions collected from real students and teachers.

## Product docs

| Doc | Purpose |
|---|---|
| [`docs/PRD.md`](docs/PRD.md) | Problem, users, goals, non-goals, metrics, risks, launch plan |
| [`docs/user_interview_guide.md`](docs/user_interview_guide.md) | Script and notes template for teacher and student interviews |

## Status and roadmap

- [x] Retriever, CLI, tests, baseline eval
- [ ] Run 5+ teacher interviews and record findings in `docs/interview_notes.md`
- [ ] Replace the 5 sample topics with notes reviewed by a teacher
- [ ] Compare TF-IDF against embedding-based retrieval on a larger question set
- [ ] Add a minimal web UI and collect real usage data

## Limitations

TF-IDF is keyword-based, so paraphrased questions can miss. The notes are short summaries and should be reviewed by a subject teacher before any classroom use. The LLM mode has not been evaluated for answer quality.

## License

MIT

## Results
See [RESULTS.md](RESULTS.md) for test output and the retrieval evaluation.
