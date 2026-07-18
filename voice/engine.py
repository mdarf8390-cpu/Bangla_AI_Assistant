"""
================================================================
AYESHA AI
VOICE ENGINE MODULE

Version : 1.0.0

Purpose
-------
Main controller for voice processing pipeline.

Features
--------
✓ Voice Module Integration
✓ Hotword Connection
✓ Language Connection
✓ Noise Analysis
✓ Logging
✓ Error Handling
✓ Future Speech Recognition Ready

================================================================
"""


from __future__ import annotations

import logging
from typing import Optional, List


from voice.noise import noise
from voice.language import language
from voice.hotword import hotword


logger = logging.getLogger(
    "AYESHA_CORE"
)



# ==========================================================
# VOICE ENGINE
# ==========================================================

class VoiceEngine:


    def __init__(self):


        self.running = False


        self.last_text = ""


        logger.info(
            "Voice Engine Initialized"
        )



    # ------------------------------------------------------
    # Start Engine
    # ------------------------------------------------------

    def start(
        self
    ) -> None:


        self.running = True


        logger.info(
            "Voice Engine Started"
        )



    # ------------------------------------------------------
    # Stop Engine
    # ------------------------------------------------------

    def stop(
        self
    ) -> None:


        self.running = False


        hotword.deactivate()


        logger.info(
            "Voice Engine Stopped"
        )



    # ------------------------------------------------------
    # Running Status
    # ------------------------------------------------------

    def is_running(
        self
    ) -> bool:


        return self.running    # ------------------------------------------------------
    # Analyze Audio
    # ------------------------------------------------------

    def analyze_audio(
        self,
        samples: List[float]
    ) -> dict:


        try:

            result = noise.analyze(
                samples
            )


            logger.info(
                "Audio Analysis Complete"
            )


            return result



        except Exception as error:


            logger.error(
                f"Audio Analysis Failed: {error}"
            )


            return {}



    # ------------------------------------------------------
    # Process Text Input
    # ------------------------------------------------------

    def process_text(
        self,
        text: str
    ) -> dict:


        try:

            self.last_text = text



            wake = hotword.process(
                text
            )


            lang = language.analyze(
                text
            )


            result = {

                "hotword":
                    wake,

                "language":
                    lang,

                "text":
                    text

            }


            logger.info(
                "Voice Text Processed"
            )


            return result



        except Exception as error:


            logger.error(
                f"Text Processing Failed: {error}"
            )


            return {}    # ------------------------------------------------------
    # Reset Engine
    # ------------------------------------------------------

    def reset(
        self
    ) -> None:


        self.last_text = ""


        hotword.deactivate()


        logger.info(
            "Voice Engine Reset"
        )



    # ------------------------------------------------------
    # Last Input
    # ------------------------------------------------------

    def get_last_text(
        self
    ) -> str:


        return self.last_text



    # ------------------------------------------------------
    # Status
    # ------------------------------------------------------

    def status(
        self
    ) -> dict:


        return {

            "module":
                "VoiceEngine",

            "running":
                self.running,

            "hotword":
                hotword.status(),

            "language":
                language.status(),

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

engine = VoiceEngine()