"""Answer generation.

Default mode is extractive and needs no API key: it returns the best-matching
passages with their sources. If ANTHROPIC_API_KEY is set, the retrieved passages
are sent to the Messages API and the model is told to answer ONLY from them.
"""
from __future__ import annotations

import json
import os
import urllib.request

from .retriever import Hit

NO_ANSWER = (
    "I couldn't find that in my notes. Try rephrasing, or ask about one of: "
    "plate tectonics, the ocean floor, colligative properties, electroplating, "
    "or protein synthesis."
)
MIN_SCORE = 0.15  # below this we say we don't know instead of guessing


def extractive_answer(hits: list[Hit]) -> str:
    hits = [h for h in hits if h.score >= MIN_SCORE]
    if not hits:
        return NO_ANSWER
    best = hits[0].chunk
    lines = [f"{best.text}", "", "Sources:"]
    for h in hits:
        lines.append(f"- {h.chunk.topic} > {h.chunk.heading} (score {h.score:.2f})")
    return "\n".join(lines)


def llm_answer(question: str, hits: list[Hit]) -> str:
    hits = [h for h in hits if h.score >= MIN_SCORE]
    if not hits:
        return NO_ANSWER
    context = "\n\n".join(f"[{h.chunk.topic} > {h.chunk.heading}]\n{h.chunk.text}" for h in hits)
    prompt = (
        "You are a patient science tutor for secondary-school students. Answer the "
        "question using ONLY the notes below. If the notes do not contain the answer, "
        "say you don't know. Keep it under 120 words and cite the note titles in brackets.\n\n"
        f"NOTES:\n{context}\n\nQUESTION: {question}"
    )
    body = json.dumps({
        "model": os.environ.get("TUTOR_MODEL", "claude-sonnet-5-5"),
        "max_tokens": 400,
        "messages": [{"role": "user", "content": prompt}],
    }).encode()
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=body,
        headers={
            "content-type": "application/json",
            "x-api-key": os.environ["ANTHROPIC_API_KEY"],
            "anthropic-version": "2023-06-01",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.load(resp)
    return "".join(b.get("text", "") for b in data.get("content", []))


def answer(question: str, hits: list[Hit]) -> str:
    if os.environ.get("ANTHROPIC_API_KEY"):
        try:
            return llm_answer(question, hits)
        except Exception as exc:  # fall back rather than fail the student
            return extractive_answer(hits) + f"\n\n(LLM unavailable: {exc})"
    return extractive_answer(hits)
