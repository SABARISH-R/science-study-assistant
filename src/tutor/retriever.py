"""Dependency-free TF-IDF retriever over markdown knowledge-base files.

Each "## " section of a file in data/kb/ becomes one searchable chunk.
"""
from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

STOPWORDS = frozenset(
    "a an and are as at be by do does for from how in is it of on or that the this "
    "to what when where which why with i you your can we they them their into than".split()
)
TOKEN_RE = re.compile(r"[a-z0-9]+")


def tokenize(text: str) -> list[str]:
    return [t for t in TOKEN_RE.findall(text.lower()) if t not in STOPWORDS]


@dataclass(frozen=True)
class Chunk:
    topic: str      # file name without extension, e.g. "plate_tectonics"
    heading: str    # the "## " heading text
    text: str       # the section body


@dataclass(frozen=True)
class Hit:
    chunk: Chunk
    score: float


def load_chunks(kb_dir: str | Path) -> list[Chunk]:
    chunks: list[Chunk] = []
    for path in sorted(Path(kb_dir).glob("*.md")):
        topic = path.stem
        heading, buf = None, []
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.startswith("## "):
                if heading and buf:
                    chunks.append(Chunk(topic, heading, " ".join(buf).strip()))
                heading, buf = line[3:].strip(), []
            elif heading is not None and line.strip():
                buf.append(line.strip())
        if heading and buf:
            chunks.append(Chunk(topic, heading, " ".join(buf).strip()))
    return chunks


class Retriever:
    def __init__(self, chunks: list[Chunk]):
        if not chunks:
            raise ValueError("No chunks loaded; check the knowledge-base directory.")
        self.chunks = chunks
        docs = [tokenize(f"{c.heading} {c.heading} {c.text}") for c in chunks]
        n = len(docs)
        df = Counter(t for d in docs for t in set(d))
        self.idf = {t: math.log((1 + n) / (1 + f)) + 1.0 for t, f in df.items()}
        self.vectors = [self._vector(d) for d in docs]

    def _vector(self, tokens: list[str]) -> dict[str, float]:
        tf = Counter(tokens)
        vec = {t: (1 + math.log(c)) * self.idf.get(t, 0.0) for t, c in tf.items()}
        norm = math.sqrt(sum(v * v for v in vec.values())) or 1.0
        return {t: v / norm for t, v in vec.items()}

    def search(self, query: str, k: int = 3) -> list[Hit]:
        q = self._vector(tokenize(query))
        scored = []
        for chunk, vec in zip(self.chunks, self.vectors):
            score = sum(w * vec.get(t, 0.0) for t, w in q.items())
            if score > 0:
                scored.append(Hit(chunk, score))
        scored.sort(key=lambda h: h.score, reverse=True)
        return scored[:k]
