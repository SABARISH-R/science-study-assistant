import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tutor.answer import NO_ANSWER, extractive_answer  # noqa: E402
from tutor.retriever import Retriever, load_chunks, tokenize  # noqa: E402


class RetrieverTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.retriever = Retriever(load_chunks(ROOT / "data" / "kb"))

    def test_loads_all_topics(self):
        topics = {c.topic for c in self.retriever.chunks}
        self.assertEqual(len(topics), 5)

    def test_tokenize_drops_stopwords(self):
        self.assertEqual(tokenize("What is the cathode?"), ["cathode"])

    def test_finds_trench_answer(self):
        hit = self.retriever.search("how do ocean trenches form", k=1)[0]
        self.assertEqual(hit.chunk.topic, "ocean_floor")

    def test_finds_freezing_point_answer(self):
        hit = self.retriever.search("why does salt melt ice", k=1)[0]
        self.assertEqual(hit.chunk.topic, "colligative_properties")

    def test_off_topic_question_is_declined(self):
        hits = self.retriever.search("who won the football match yesterday", k=3)
        self.assertEqual(extractive_answer(hits), NO_ANSWER)


if __name__ == "__main__":
    unittest.main()
