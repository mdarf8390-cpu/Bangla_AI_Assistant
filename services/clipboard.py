import pyperclip
import logging

from services.keyboard import KeyboardService

logger = logging.getLogger(__name__)


class ClipboardService:

    def __init__(self):

        self.keyboard = KeyboardService()


    # -----------------------------
    # Clipboard
    # -----------------------------

    def copy(self):

        try:
            return self.keyboard.copy()
        except Exception as e:
            logger.error(f"Failed to copy: {str(e)}")
            return False


    def cut(self):

        try:
            return self.keyboard.cut()
        except Exception as e:
            logger.error(f"Failed to cut: {str(e)}")
            return False


    def paste(self):

        try:
            return self.keyboard.paste()
        except Exception as e:
            logger.error(f"Failed to paste: {str(e)}")
            return False


    # -----------------------------
    # Text
    # -----------------------------

    def set_text(self, text):

        if not isinstance(text, str):
            logger.error(f"Text must be string, got {type(text).__name__}")
            return False

        try:
            pyperclip.copy(text)
            return True
        except Exception as e:
            logger.error(f"Failed to set clipboard text: {str(e)}")
            return False


    def get_text(self):

        try:
            text = pyperclip.paste()
            return text if text else ""
        except Exception as e:
            logger.error(f"Failed to get clipboard text: {str(e)}")
            return None


    # -----------------------------
    # Smart Paste
    # -----------------------------

    def paste_text(self, text, target=None):

        if not isinstance(text, str):
            logger.error(f"Text must be string, got {type(text).__name__}")
            return False

        try:
            if not self.set_text(text):
                logger.error("Failed to set clipboard text")
                return False

            if target:
                if not self.keyboard.window.activate(target):
                    logger.warning(f"Failed to activate target window: {target}")
                    return False

            if not self.keyboard.paste():
                logger.error("Failed to paste text")
                return False

            return True
        except Exception as e:
            logger.error(f"Failed in paste_text operation: {str(e)}")
            return False


    def clear(self):

        try:
            pyperclip.copy("")
            return True
        except Exception as e:
            logger.error(f"Failed to clear clipboard: {str(e)}")
            return False
