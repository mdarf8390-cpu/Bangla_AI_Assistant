"""
================================================================
AYESHA AI
HOTWORD DETECTION MODULE

Version : 1.0.0

Purpose
-------
Wake word detection and assistant activation.

Features
--------
✓ Wake Word Detection
✓ Active / Sleep State
✓ Custom Wake Word
✓ Logging
✓ Error Handling
✓ Future Microphone Ready

================================================================
"""


from __future__ import annotations

import logging
from typing import List


logger = logging.getLogger(
    "AYESHA_CORE"
)


# ==========================================================
# HOTWORD DETECTOR
# ==========================================================

class HotwordDetector:


    def __init__(
        self,
        wake_word: str = "ayesha"
    ):


        self.wake_word = (
            wake_word.lower()
        )


        self.active = False


        logger.info(
            "Hotword Detector Initialized"
        )



    # ------------------------------------------------------
    # Check Wake Word
    # ------------------------------------------------------

    def detect(
        self,
        text: str
    ) -> bool:


        if not text:

            return False


        try:

            result = (
                self.wake_word
                in text.lower()
            )


            if result:

                logger.info(
                    "Wake Word Detected"
                )


            return result



        except Exception as error:


            logger.error(
                f"Hotword Detection Failed: {error}"
            )


            return False    # ------------------------------------------------------
    # Activate Assistant
    # ------------------------------------------------------

    def activate(
        self
    ) -> None:


        self.active = True


        logger.info(
            "AYESHA Activated"
        )



    # ------------------------------------------------------
    # Deactivate Assistant
    # ------------------------------------------------------

    def deactivate(
        self
    ) -> None:


        self.active = False


        logger.info(
            "AYESHA Sleeping"
        )



    # ------------------------------------------------------
    # State Check
    # ------------------------------------------------------

    def is_active(
        self
    ) -> bool:


        return self.active



    # ------------------------------------------------------
    # Process Input
    # ------------------------------------------------------

    def process(
        self,
        text: str
    ) -> dict:


        detected = self.detect(
            text
        )


        if detected:

            self.activate()



        return {

            "wake_word":
                self.wake_word,

            "detected":
                detected,

            "active":
                self.active,

            "input":
                text

        }    # ------------------------------------------------------
    # Change Wake Word
    # ------------------------------------------------------

    def set_wake_word(
        self,
        word: str
    ) -> bool:


        if not word:

            return False


        self.wake_word = (
            word.lower().strip()
        )


        logger.info(
            f"Wake Word Changed: {self.wake_word}"
        )


        return True



    # ------------------------------------------------------
    # Get Wake Word
    # ------------------------------------------------------

    def get_wake_word(
        self
    ) -> str:


        return self.wake_word



    # ------------------------------------------------------
    # Status
    # ------------------------------------------------------

    def status(
        self
    ) -> dict:


        return {

            "module":
                "HotwordDetector",

            "wake_word":
                self.wake_word,

            "active":
                self.active,

            "ready":
                True

        }



# ==========================================================
# GLOBAL INSTANCE
# ==========================================================

hotword = HotwordDetector()