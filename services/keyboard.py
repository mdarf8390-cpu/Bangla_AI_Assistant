import pyautogui
import time
import logging

from services.window import WindowService

logger = logging.getLogger(__name__)


class KeyboardService:

    def __init__(self):

        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.02

        self.window = WindowService()


    # -----------------------------
    # Smart Typing
    # -----------------------------

    def type(self, text, target=None, interval=0.01):

        if not isinstance(text, str):
            logger.error(f"Text must be string, got {type(text)}")
            return False

        if target:

            ok = self.window.activate(target)

            if not ok:
                logger.warning(f"Failed to activate window: {target}")
                return False

            time.sleep(0.2)

        try:
            pyautogui.write(
                text,
                interval=interval
            )
            return True
        except Exception as e:
            logger.error(f"Failed to type text: {str(e)}")
            return False


    # -----------------------------
    # Basic Keys
    # -----------------------------

    def press(self, key):

        if not key:
            logger.error("Key cannot be empty")
            return False
        
        try:
            pyautogui.press(key)
            return True
        except Exception as e:
            logger.error(f"Failed to press key '{key}': {str(e)}")
            return False


    def hotkey(self, *keys):

        if not keys:
            logger.error("At least one key is required")
            return False
        
        try:
            pyautogui.hotkey(*keys)
            return True
        except Exception as e:
            logger.error(f"Failed to execute hotkey {keys}: {str(e)}")
            return False


    def hold(self, key):

        if not key:
            logger.error("Key cannot be empty")
            return False
        
        try:
            pyautogui.keyDown(key)
            return True
        except Exception as e:
            logger.error(f"Failed to hold key '{key}': {str(e)}")
            return False


    def release(self, key):

        if not key:
            logger.error("Key cannot be empty")
            return False
        
        try:
            pyautogui.keyUp(key)
            return True
        except Exception as e:
            logger.error(f"Failed to release key '{key}': {str(e)}")
            return False


    # -----------------------------
    # Common Actions
    # -----------------------------

    def enter(self):

        return self.press("enter")


    def tab(self):

        return self.press("tab")


    def escape(self):

        return self.press("esc")


    def space(self):

        return self.press("space")


    def backspace(self):

        return self.press("backspace")


    def delete(self):

        return self.press("delete")


    # -----------------------------
    # Editing
    # -----------------------------

    def select_all(self):

        return self.hotkey("ctrl", "a")


    def copy(self):

        return self.hotkey("ctrl", "c")


    def paste(self):

        return self.hotkey("ctrl", "v")


    def cut(self):

        return self.hotkey("ctrl", "x")


    def undo(self):

        return self.hotkey("ctrl", "z")


    def redo(self):

        return self.hotkey("ctrl", "y")


    def save(self):

        return self.hotkey("ctrl", "s")
