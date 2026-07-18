from services.window import WindowService
from services.keyboard import KeyboardService
from services.mouse import MouseService
from services.clipboard import ClipboardService


class BaseSkill:

    def __init__(self):

        self.window = WindowService()

        self.keyboard = KeyboardService()

        self.mouse = MouseService()

        self.clipboard = ClipboardService()


    # -------------------------
    # Window
    # -------------------------

    def activate(self, target):

        return self.window.activate(target)


    def close(self, target):

        return self.window.close(target)


    # -------------------------
    # Keyboard
    # -------------------------

    def type(self, text, target=None):

        return self.keyboard.type(
            text=text,
            target=target
        )


    def press(self, key):

        self.keyboard.press(key)


    def hotkey(self, *keys):

        self.keyboard.hotkey(*keys)


    # -------------------------
    # Clipboard
    # -------------------------

    def paste(self, text, target=None):

        return self.clipboard.paste_text(
            text=text,
            target=target
        )


    # -------------------------
    # Mouse
    # -------------------------

    def click(self, x=None, y=None):

        self.mouse.click(x, y)


    def double_click(self, x=None, y=None):

        self.mouse.double_click(x, y)


    def right_click(self, x=None, y=None):

        self.mouse.right_click(x, y)