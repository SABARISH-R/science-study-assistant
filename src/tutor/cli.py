"""Command-line interface: python -m tutor.cli "why do oceans have trenches?" """
from __future__ import annotations

import argparse
from pathlib import Path

from .answer import answer
from .retriever import Retriever, load_chunks

KB_DIR = Path(__file__).resolve().parents[2] / "data" / "kb"


def main() -> None:
    parser = argparse.ArgumentParser(description="Ask the science study assistant a question.")
    parser.add_argument("question", nargs="*", help="Your question (omit for interactive mode)")
    parser.add_argument("-k", type=int, default=3, help="Passages to retrieve")
    args = parser.parse_args()
    retriever = Retriever(load_chunks(KB_DIR))

    if args.question:
        q = " ".join(args.question)
        print(answer(q, retriever.search(q, args.k)))
        return
    print("Science Study Assistant. Type a question, or 'quit'.")
    while True:
        q = input("\n> ").strip()
        if q.lower() in {"quit", "exit", ""}:
            break
        print(answer(q, retriever.search(q, args.k)))


if __name__ == "__main__":
    main()
