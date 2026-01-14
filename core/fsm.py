# core/fsm.py
from core.emotion import Emotion

ALLOWED_TRANSITIONS = {
    Emotion.NEUTRAL: {
        Emotion.HAPPY,
        Emotion.TEASE,
        Emotion.CONCERN
    },

    Emotion.HAPPY: {
        Emotion.NEUTRAL,
        Emotion.CARE
    },

    Emotion.CARE: {
        Emotion.NEUTRAL
    },

    Emotion.TEASE: {
        Emotion.NEUTRAL
    },

    Emotion.CONCERN: {
        Emotion.NEUTRAL,
        Emotion.CARE
    },

    Emotion.SOFT_ANGRY: {
        Emotion.NEUTRAL
    }
}

def is_transition_allowed(current: Emotion, proposed: Emotion) -> bool:
    return proposed in ALLOWED_TRANSITIONS.get(current, set())
