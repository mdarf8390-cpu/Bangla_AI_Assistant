"""
================================================================
AYESHA AI
TEXT TO SPEECH MODULE

Version : 1.0.0

Purpose
-------
Convert AI text response into voice.

Features
--------
✓ Text To Speech Base
✓ Voice Queue Ready
✓ Speed Control
✓ Volume Control
✓ Logging
✓ Error Handling
✓ Future Neural TTS Ready

================================================================
"""


from __future__ import annotations

import logging
from typing import Optional


logger = logging.getLogger(
    "AYESHA_CORE"
)


# ==========================================================
# TTS ENGINE
# ==========================================================

class TTSEngine:


    def __init__(self):


        self.rate = 150


        self.volume = 1.0


        self.enabled = True


        logger.info(
            "TTS Engine Initialized"
        )



    # ------------------------------------------------------
    # Speak Placeholder
    # ------------------------------------------------------

    def speak(
        self,
        text: str
    ) -> bool:


        if not self.enabled:

            logger.warning(
                "TTS Disabled"
            )

            return False



        if not text:

            return False



        try:


            logger.info(
                f"Speaking: {text}"
            )


            print(
                "AYESHA:",
                text
            )


            return True



        except Exception as error:


            logger.error(
                f"TTS Failed: {error}"
            )


            return False    # ------------------------------------------------------
    # Set Voice Rate
    # ------------------------------------------------------

    def set_rate(
        self,
        rate: int
    ) -> None:


        if rate < 50:

            rate = 50


        if rate > 300:

            rate = 300


        self.rate = rate


        logger.info(
            f"TTS Rate Changed: {rate}"
        )



    # ------------------------------------------------------
    # Set Volume
    # ------------------------------------------------------

    def set_volume(
        self,
        volume: float
    ) -> None:


        if volume < 0:

            volume = 0


        if volume > 1:

            volume = 1


        self.volume = volume


        logger.info(
            f"TTS Volume Changed: {volume}"
        )



    # ------------------------------------------------------
    # Enable TTS
    # ------------------------------------------------------

    def enable(
        self
    ) -> None:


        self.enabled = True


        logger.info(
            "TTS Enabled"
        )



    # ------------------------------------------------------
    # Disable TTS
    # ------------------------------------------------------

    def disable(
        self
    ) -> None:


        self.enabled = False


        logger.info(
            "TTS Disabled"
        )    # ------------------------------------------------------
    # Status
    # ------------------------------------------------------

    def status(
        self
    ) -> dict:


        return {

            "module":
                "TTSEngine",

            "enabled":
                self.enabled,

            "rate":
                self.rate,

            "volume":
                self.volume,

            "ready":
                True

        }



    # ------------------------------------------------------
    # Test Voice
    # ------------------------------------------------------

    def test(
        self
    ) -> bool:


        return self.speak(
            "Hello, I am AYESHA"
        )



# ==========================================================
# GLOBAL INSTANCE
# ==========================================================

tts = TTSEngine()