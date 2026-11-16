"""Regenerate docs/images/retrieval_accuracy_by_topic.png. Run from the repo root:
   PYTHONPATH=src python scripts/make_figures.py   (needs matplotlib)
"""
import json
import sys
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from tutor.retriever import Retriever, load_chunks  # noqa: E402

retriever = Retriever(load_chunks(ROOT / "data" / "kb"))
questions = json.loads((ROOT / "eval" / "questions.json").read_text())
stats = defaultdict(lambda: [0, 0, 0])  # n, top1, top3
for q in questions:
    topics = [h.chunk.topic for h in retriever.search(q["question"], k=3)]
    s = stats[q["expected_topic"]]
    s[0] += 1
    s[1] += topics[:1] == [q["expected_topic"]]
    s[2] += q["expected_topic"] in topics

names = sorted(stats)
labels = [n.replace("_", " ") for n in names]
top1 = [stats[n][1] / stats[n][0] * 100 for n in names]
top3 = [stats[n][2] / stats[n][0] * 100 for n in names]
x = range(len(names))
fig, ax = plt.subplots(figsize=(7, 3.8))
ax.bar([i - 0.2 for i in x], top1, 0.4, label="Top-1", color="#1F3A5F")
ax.bar([i + 0.2 for i in x], top3, 0.4, label="Top-3", color="#7FA7D9")
ax.set_xticks(list(x))
ax.set_xticklabels(labels, fontsize=8)
ax.set_ylabel("Questions answered from the right topic (%)")
ax.set_ylim(0, 110)
ax.set_title("Retrieval accuracy by topic (20 internal questions)")
ax.legend(frameon=False, fontsize=8)
fig.tight_layout()
out = ROOT / "docs" / "images"
out.mkdir(parents=True, exist_ok=True)
fig.savefig(out / "retrieval_accuracy_by_topic.png", dpi=160)
print("Saved", out / "retrieval_accuracy_by_topic.png")
