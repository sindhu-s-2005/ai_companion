# core/emotion_resolver.py
from core.emotion import Emotion
from core.context_analyzer import Context


class EmotionResolver:

    def resolve(self, context: Context) -> Emotion | None:
        """
        Returns a proposed Emotion or None if no change is suggested.
        FSM + StateManager decide what actually happens.
        """

        # Hard safety overrides
        if "DEPENDENCY_RISK" in context.flags:
            return Emotion.NEUTRAL

        if "SELF_NEGATIVE" in context.flags:
            return Emotion.CONCERN

        # High emotional pressure
        if context.emotional_pressure >= 3:
            return Emotion.CONCERN

        # Medium pressure
        if context.emotional_pressure == 2:
            return Emotion.CARE

        # Intent-based light emotions
        if context.intent == "GREETING":
            return Emotion.HAPPY

        if context.intent == "SHORT_CHAT":
            return Emotion.TEASE

        # Default: no suggestion
        return None
