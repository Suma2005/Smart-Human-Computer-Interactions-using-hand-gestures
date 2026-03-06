# gesture_engine.py

class GestureEngine:
    def __init__(self):
        self.current_gesture = None
        self.previous_gesture = None

    def detect_gesture(self, landmarks):
        """
        Takes hand landmarks
        Returns gesture name as string
        """
        # For now just return None
        return None