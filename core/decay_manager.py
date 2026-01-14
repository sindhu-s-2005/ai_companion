# core/decay_manager.py
import time
from core.state_manager import StateManager
from core.memory_store import MemoryStore


class DecayManager:
    def __init__(self, state_manager: StateManager, memory_store: MemoryStore):
        self.state_manager = state_manager
        self.memory_store = memory_store
        self.last_check = time.time()

    def tick(self):
        now = time.time()

        # Run every 10 seconds
        if now - self.last_check < 10:
            return

        self.last_check = now

        # Emotion decay
        self.state_manager.decay_if_needed()

        # Memory decay
        self.memory_store.delete_expired()
