import pyautogui
import time

pyautogui.FAILSAFE = False


class ActionController:

    def __init__(self):
        self.drag = False
        self.last_action = 0
        self.cooldown = 0.3

    def ready(self):
        now = time.time()
        if now - self.last_action < self.cooldown:
            return False
        self.last_action = now
        return True

    # -------- Mouse -------- #

    def move_mouse(self, x, y):
        pyautogui.moveTo(x, y, duration=0.05)

    def drag_mouse(self, x, y):
        if not self.drag:
            pyautogui.mouseDown()
            self.drag = True
        pyautogui.moveTo(x, y, duration=0.05)

    def release_mouse(self):
        if self.drag:
            pyautogui.mouseUp()
            self.drag = False

    def left_click(self):
        if self.ready():
            pyautogui.click()

    # -------- Scroll -------- #

    def scroll(self, delta):
        if delta > 0:
            pyautogui.scroll(-200)
        else:
            pyautogui.scroll(200)

    # -------- Copy / Paste -------- #

    def copy(self):
        if self.ready():
            pyautogui.hotkey("ctrl", "c")

    def paste(self):
        if self.ready():
            pyautogui.hotkey("ctrl", "v")

    # -------- Tabs -------- #

    def next_tab(self):
        if self.ready():
            pyautogui.hotkey("ctrl", "tab")

    def prev_tab(self):
        if self.ready():
            pyautogui.hotkey("ctrl", "shift", "tab")