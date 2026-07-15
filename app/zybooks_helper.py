from typing import List


class ZyBooksHelper:
    def summarize_text(self, text: str) -> str:
        paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
        if not paragraphs:
            return "No content available."

        summary_points = []
        for paragraph in paragraphs[:4]:
            words = paragraph.split()
            if len(words) > 20:
                summary_points.append(" ".join(words[:20]) + "...")
            else:
                summary_points.append(paragraph)

        return "\n".join(f"- {point}" for point in summary_points)

    def extract_key_concepts(self, text: str) -> List[str]:
        concepts = []
        seen = set()
        for line in text.splitlines():
            stripped = line.strip()
            if not stripped:
                continue
            if len(stripped) < 80 and stripped[0].isupper():
                if stripped not in seen:
                    concepts.append(stripped)
                    seen.add(stripped)
        if not concepts:
            for sentence in text.split("."):
                candidate = sentence.strip()
                if candidate and len(candidate) < 80:
                    if candidate not in seen:
                        concepts.append(candidate)
                        seen.add(candidate)
        return concepts[:8]

    def generate_quick_questions(self, topic: str) -> List[dict]:
        return [
            {
                "question": f"What is the main idea of {topic}?",
                "answer": "Core concept",
                "options": ["Core concept", "Key definition", "Real-world example"],
            },
            {
                "question": f"How would you apply {topic} to a simple example?",
                "answer": "Real-world example",
                "options": ["Core concept", "Key definition", "Real-world example"],
            },
        ]
