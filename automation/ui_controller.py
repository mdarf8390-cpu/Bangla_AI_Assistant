"""
================================================================
AYESHA AI - UI CONTROLLER MODULE
Version : 1.0.0

Purpose:
Controls mouse and keyboard actions.

Features:
- Mouse control
- Keyboard control
- Hotkeys
- Screen information
- Logging
- Error handling
================================================================
"""

import logging
import time
from typing import Tuple


import pyautogui


logger = logging.getLogger("AYESHA_CORE")


# Safety pause between actions

pyautogui.PAUSE = 0.2



# ===============================================================
# UI Controller
# ===============================================================

class UIController:


    def __init__(self):

        logger.info(
            "UI Controller Initialized"
        )



    # -----------------------------------------------------------
    # Screen Size
    # -----------------------------------------------------------

    def screen_size(
        self
    ) -> Tuple[int, int]:

        try:

            size = pyautogui.size()

            return (
                size.width,
                size.height
            )


        except Exception as error:

            logger.error(
                f"Screen Size Failed: {error}"
            )

            return (
                0,
                0
            )



    # -----------------------------------------------------------
    # Move Mouse
    # -----------------------------------------------------------

    def move_mouse(
        self,
        x: int,
        y: int
    ) -> bool:


        try:

            pyautogui.moveTo(
                x,
                y
            )


            logger.info(
                f"Mouse moved: {x},{y}"
            )


            return True


        except Exception as error:

            logger.error(
                f"Mouse Move Failed: {error}"
            )

            return False



    # -----------------------------------------------------------
    # Left Click
    # -----------------------------------------------------------

    def click(
        self,
        x: int = None,
        y: int = None
    ) -> bool:


        try:

            if x is not None and y is not None:

                pyautogui.click(
                    x,
                    y
                )

            else:

                pyautogui.click()


            logger.info(
                "Mouse Click"
            )


            return True


        except Exception as error:

            logger.error(
                f"Click Failed: {error}"
            )

            return False



    # -----------------------------------------------------------
    # Double Click
    # -----------------------------------------------------------

    def double_click(
        self
    ) -> bool:


        try:

            pyautogui.doubleClick()

            return True


        except Exception as error:

            logger.error(
                f"Double Click Failed: {error}"
            )

            return False



    # -----------------------------------------------------------
    # Right Click
    # -----------------------------------------------------------

    def right_click(
        self
    ) -> bool:


        try:

            pyautogui.rightClick()

            return True


        except Exception as error:

            logger.error(
                f"Right Click Failed: {error}"
            )

            return False



    # -----------------------------------------------------------
    # Type Text
    # -----------------------------------------------------------

    def type_text(
        self,
        text: str
    ) -> bool:


        try:

            pyautogui.write(
                text,
                interval=0.03
            )


            logger.info(
                "Text Typed"
            )


            return True


        except Exception as error:

            logger.error(
                f"Typing Failed: {error}"
            )

            return False



    # -----------------------------------------------------------
    # Press Key
    # -----------------------------------------------------------

    def press(
        self,
        key: str
    ) -> bool:


        try:

            pyautogui.press(
                key
            )


            return True


        except Exception as error:

            logger.error(
                f"Key Press Failed: {error}"
            )

            return False



    # -----------------------------------------------------------
    # Hotkey
    # -----------------------------------------------------------

    def hotkey(
        self,
        *keys
    ) -> bool:


        try:

            pyautogui.hotkey(
                *keys
            )


            return True


        except Exception as error:

            logger.error(
                f"Hotkey Failed: {error}"
            )

            return False



# ===============================================================
# Global Instance
# ===============================================================

ui_controller = UIController()