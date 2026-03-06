import cv2
import mediapipe as mp
import pyautogui
import math
import time
from enum import Enum
from action_controller import ActionController

pyautogui.FAILSAFE = False

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands


# ---------------- GESTURES ---------------- #

class Gest(Enum):
    NONE = 0
    INDEX = 1
    PINCH = 2
    FIST = 3
    TWO = 4
    THREE = 5
    FOUR = 6
    CALL = 7   # Thumb + Little finger


# ---------------- HAND RECOGNITION ---------------- #

class HandRecog:

    def __init__(self):
        self.prev = Gest.NONE
        self.count = 0
        self.stable = Gest.NONE

    def get(self, hand):

        lm = hand.landmark

        index = lm[8].y < lm[6].y
        middle = lm[12].y < lm[10].y
        ring = lm[16].y < lm[14].y
        pinky = lm[20].y < lm[18].y

        thumb_open = abs(lm[4].x - lm[2].x) > 0.15

        palm_size = math.hypot(lm[0].x - lm[9].x,
                               lm[0].y - lm[9].y)

        pinch_dist = math.hypot(lm[8].x - lm[4].x,
                                lm[8].y - lm[4].y)

        pinch = pinch_dist < palm_size * 0.25

        detected = Gest.NONE

        # Exit Gesture (Thumb + Pinky only)
        if thumb_open and pinky and not index and not middle and not ring:
            detected = Gest.CALL

        elif pinch:
            detected = Gest.PINCH

        elif index and not middle and not ring and not pinky:
            detected = Gest.INDEX

        elif index and middle and not ring and not pinky:
            detected = Gest.TWO

        elif index and middle and ring and not pinky:
            detected = Gest.THREE

        elif index and middle and ring and pinky:
            detected = Gest.FOUR

        elif not index and not middle and not ring and not pinky:
            detected = Gest.FIST

        # Stability filter
        if detected == self.prev:
            self.count += 1
        else:
            self.count = 0

        self.prev = detected

        if self.count > 5:
            self.stable = detected

        return self.stable


# ---------------- MAIN CONTROLLER ---------------- #

class GestureController:

    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.hand = HandRecog()
        self.controller = ActionController()

        self.prev_x = None
        self.prev_y = None
        self.hold_start = None
        self.hold_gesture = None

    def start(self):

        with mp_hands.Hands(
                max_num_hands=1,
                min_detection_confidence=0.85,
                min_tracking_confidence=0.85) as hands:

            while self.cap.isOpened():

                success, frame = self.cap.read()
                if not success:
                    break

                frame = cv2.flip(frame, 1)
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = hands.process(rgb)

                if results.multi_hand_landmarks:

                    hand = results.multi_hand_landmarks[0]
                    gesture = self.hand.get(hand)

                    sw, sh = pyautogui.size()
                    x = int(hand.landmark[9].x * sw)
                    y = int(hand.landmark[9].y * sh)

                    cur_x = hand.landmark[9].x
                    cur_y = hand.landmark[9].y

                    if self.prev_x is None:
                        self.prev_x = cur_x
                        self.prev_y = cur_y

                    delta_x = cur_x - self.prev_x
                    delta_y = cur_y - self.prev_y

                    # -------- EXIT (CALL Gesture Hold 2 sec) -------- #
                    if gesture == Gest.CALL:

                        if self.hold_gesture != Gest.CALL:
                            self.hold_start = time.time()
                            self.hold_gesture = Gest.CALL

                        elif time.time() - self.hold_start > 2:
                            break

                    # -------- MOVE -------- #
                    elif gesture == Gest.INDEX:
                        self.controller.move_mouse(x, y)

                    # -------- DRAG -------- #
                    elif gesture == Gest.PINCH:
                        self.controller.drag_mouse(x, y)

                    # -------- RELEASE -------- #
                    elif gesture == Gest.FIST:
                        self.controller.release_mouse()

                    # -------- TWO (Tabs + Copy) -------- #
                    elif gesture == Gest.TWO:

                        if delta_x > 0.12:
                            self.controller.next_tab()
                        elif delta_x < -0.12:
                            self.controller.prev_tab()

                        if self.hold_gesture != Gest.TWO:
                            self.hold_start = time.time()
                            self.hold_gesture = Gest.TWO
                        elif time.time() - self.hold_start > 2:
                            self.controller.copy()
                            self.hold_gesture = None

                    # -------- THREE (Click + Paste) -------- #
                    elif gesture == Gest.THREE:

                        if self.hold_gesture != Gest.THREE:
                            self.hold_start = time.time()
                            self.hold_gesture = Gest.THREE
                            self.controller.left_click()

                        elif time.time() - self.hold_start > 2:
                            self.controller.paste()
                            self.hold_gesture = None

                    # -------- FOUR (Scroll) -------- #
                    elif gesture == Gest.FOUR:
                        if abs(delta_y) > 0.03:
                            self.controller.scroll(delta_y)

                    else:
                        self.hold_gesture = None

                    self.prev_x = cur_x
                    self.prev_y = cur_y

                    mp_drawing.draw_landmarks(
                        frame, hand, mp_hands.HAND_CONNECTIONS)

                cv2.imshow("Gesture Controller", frame)

                # ESC backup exit
                if cv2.waitKey(1) & 0xFF == 27:
                    break

        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    GestureController().start()