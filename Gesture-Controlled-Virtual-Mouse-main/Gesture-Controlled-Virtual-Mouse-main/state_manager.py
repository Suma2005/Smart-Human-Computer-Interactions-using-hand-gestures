# state_manager.py
import time
from config import COOLDOWN_TIME

class StateManager:
    def __init__(self):
        self.last_trigger_time = 0

    def can_trigger(self):
        current_time = time.time()
        if current_time - self.last_trigger_time > COOLDOWN_TIME:
            self.last_trigger_time = current_time
            return True
        return False