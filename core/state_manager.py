# core/state_manager.py
import time
from core.emotion import Emotion
from core.fsm import is_transition_allowed

EMOTION_COOLDOWN = 10  # seconds
MAX_EMOTION_DURATION = 120  # seconds

class StateManager:
    def __init__(self):
        self.current_emotion = Emotion.NEUTRAL
        self.last_transition_time = time.time()

    def request_transition(self, proposed_emotion: Emotion) -> Emotion:
        now = time.time()

        # Cooldown enforcement
        if now - self.last_transition_time < EMOTION_COOLDOWN:
            return self.current_emotion

        # FSM enforcement
        if is_transition_allowed(self.current_emotion, proposed_emotion):
            self.current_emotion = proposed_emotion
            self.last_transition_time = now
            return self.current_emotion

        # Illegal transition → ignore
        return self.current_emotion

    def decay_if_needed(self) -> Emotion:
        now = time.time()

        if (
            self.current_emotion != Emotion.NEUTRAL
            and now - self.last_transition_time > MAX_EMOTION_DURATION
        ):
            self.current_emotion = Emotion.NEUTRAL
            self.last_transition_time = now

        return self.current_emotion