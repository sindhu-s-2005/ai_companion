# core/context_analyzer.py
from dataclasses import dataclass
from typing import Optional


@dataclass
class Context:
    intent: str
    emotional_pressure: int  # 0–3
    topic: Optional[str]
    flags: list[str]
# core/context_analyzer.py
import re
from core.context_analyzer import Context


class ContextAnalyzer:

    def analyze(self, user_input: str) -> Context:
        text = user_input.lower().strip()

        intent = self._detect_intent(text)
        pressure = self._detect_emotional_pressure(text)
        topic = self._detect_topic(text)
        flags = self._detect_flags(text)

        return Context(
            intent=intent,
            emotional_pressure=pressure,
            topic=topic,
            flags=flags
        )
    def _detect_intent(self, text: str) -> str:
        if any(word in text for word in ["remind", "schedule", "task"]):
            return "TASK"

        if any(word in text for word in ["help", "explain", "how", "why"]):
            return "INFORMATION"

        if any(word in text for word in ["hi", "hello", "hey"]):
            return "GREETING"

        if len(text.split()) < 4:
            return "SHORT_CHAT"

        return "GENERAL_CHAT"
    def _detect_emotional_pressure(self, text: str) -> int:
        score = 0

        if re.search(r"\b(sad|tired|angry|upset|lonely)\b", text):
            score += 1

        if "!" in text:
            score += 1

        if len(text.split()) > 20:
            score += 1

        return min(score, 3)
    def _detect_topic(self, text: str) -> str | None:
        if any(word in text for word in ["work", "job", "office"]):
            return "WORK"

        if any(word in text for word in ["study", "exam", "college"]):
            return "STUDY"

        if any(word in text for word in ["family", "home"]):
            return "FAMILY"

        return None
    def _detect_flags(self, text: str) -> list[str]:
        flags = []

        if any(word in text for word in ["only you", "need you", "don't leave"]):
            flags.append("DEPENDENCY_RISK")

        if any(word in text for word in ["hate myself", "worthless"]):
            flags.append("SELF_NEGATIVE")

        if any(word in text for word in ["always", "never"]):
            flags.append("ABSOLUTE_LANGUAGE")

        return flags
