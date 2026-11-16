# Results

Produced by running the commands in this repository on 2026-11-16 with Python 3.12.3. Re-run them to reproduce.

## Unit tests
`PYTHONPATH=src python -m unittest discover -s tests`

```
----------------------------------------------------------------------
Ran 5 tests in 0.001s

OK
```

## Retrieval evaluation (20 questions)
`PYTHONPATH=src python eval/run_eval.py`

```
Questions: 20
Top-1 topic accuracy: 19/20 = 95%
Top-3 topic accuracy: 20/20 = 100%
```

How to read this: each question has one expected topic, and a hit counts when the top-ranked (or any of the top 3) passages come from that topic. The questions and the notes were written by the same author, so these numbers are optimistic and serve as a smoke test, not a benchmark.

## Not done yet
- Interviews with real teachers and students (see docs/user_interview_guide.md)
- Teacher review of the notes
- Quality evaluation of the optional LLM mode
- Evaluation on questions collected from real users
