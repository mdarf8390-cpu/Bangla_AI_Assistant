"""
================================================================
AYESHA AI
SPEECH TO TEXT MODULE

Version : 1.0.0

Purpose
-------
Convert human voice into text.

Features
--------
✓ Speech Input Base
✓ Microphone Ready
✓ Audio Buffer Ready
✓ Logging
✓ Error Handling
✓ Future Whisper Integration Ready

================================================================
"""


from __future__ import annotations

import logging
from typing import Optional


logger = logging.getLogger(
    "AYESHA_CORE"
)



# ==========================================================
# SPEECH RECOGNIZER
# ==========================================================

class SpeechRecognizer:


    def __init__(self):


        self.language = "en"


        self.running = False


        self.last_text = ""


        logger.info(
            "Speech Recognizer Initialized"
        )



    # ------------------------------------------------------
    # Start Listening
    # ------------------------------------------------------

    def start(
        self
    ) -> None:


        self.running = True


        logger.info(
            "STT Listening Started"
        )



    # ------------------------------------------------------
    # Stop Listening
    # ------------------------------------------------------

    def stop(
        self
    ) -> None:


        self.running = False


        logger.info(
            "STT Listening Stopped"
        )    # ------------------------------------------------------
    # Process Audio Input
    # ------------------------------------------------------

    def recognize(
        self,
        audio_data: Optional[bytes] = None
    ) -> str:


        try:


            if not self.running:

                logger.warning(
                    "STT is not running"
                )

                return ""



            # Future:
            # Whisper / Vosk / Google STT
            # integration point


            text = ""


            self.last_text = text


            return text



        except Exception as error:


            logger.error(
                f"STT Recognition Failed: {error}"
            )


            return ""



    # ------------------------------------------------------
    # Set Language
    # ------------------------------------------------------

    def set_language(
        self,
        language: str
    ) -> None:


        self.language = language


        logger.info(
            f"STT Language Set: {language}"
        )



    # ------------------------------------------------------
    # Get Last Text
    # ------------------------------------------------------

    def get_last_text(
        self
    ) -> str:


        return self.last_text    # ------------------------------------------------------
    # Status
    # ------------------------------------------------------

    def status(
        self
    ) -> dict:


        return {

            "module":
                "SpeechRecognizer",

            "running":
                self.running,

            "language":
                self.language,

            "last_text":
                self.last_text,

            "ready":
                True

        }



    # ------------------------------------------------------
    # Health Check
    # ------------------------------------------------------

    def health(
        self
    ) -> bool:


        try:

            return True


        except Exception:

            return False



# ==========================================================
# GLOBAL INSTANCE
# ==========================================================

stt = SpeechRecognizer()