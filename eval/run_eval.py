"""Measure retrieval quality: does the top-k hit come from the expected topic?

Run from the repo root:  PYTHONPATH=src python eval/run_eval.py
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tutor.retriever import Retriever, load_chunks  # noqa: E402


def main() -> None:
    retriever = Retriever(load_chunks(ROOT / "data" / "kb"))
    questions = json.loads((ROOT / "eval" / "questions.json").read_text())
    hit1 = hit3 = 0
    misses = []
    for item in questions:
        hits = retriever.search(item["question"], k=3)
        topics = [h.chunk.topic for h in hits]
        if topics[:1] == [item["expected_topic"]]:
            hit1 += 1
        if item["expected_topic"] in topics:
            hit3 += 1
        else:
            misses.append(item["question"])
    n = len(questions)
    print(f"Questions: {n}")
    print(f"Top-1 topic accuracy: {hit1}/{n} = {hit1 / n:.0%}")
    print(f"Top-3 topic accuracy: {hit3}/{n} = {hit3 / n:.0%}")
    for m in misses:
        print(f"MISS: {m}")


if __name__ == "__main__":
    main()
