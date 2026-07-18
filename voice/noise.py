"""
================================================================
AYESHA AI
NOISE CONTROL MODULE

Version : 1.0.0

Purpose
-------
Microphone noise analysis and
voice activity preparation.

Features
--------
✓ Noise Level Detection
✓ Silence Detection
✓ Audio Validation
✓ Logging
✓ Error Handling
✓ Future STT Ready

================================================================
"""


from __future__ import annotations

import logging
import math
from typing import List


logger = logging.getLogger(
    "AYESHA_CORE"
)


# ==========================================================
# NOISE ANALYZER
# ==========================================================

class NoiseAnalyzer:


    def __init__(
        self,
        silence_threshold: float = 0.02
    ):

        self.silence_threshold = (
            silence_threshold
        )

        logger.info(
            "Noise Analyzer Initialized"
        )


    # ------------------------------------------------------
    # Calculate Volume Level
    # ------------------------------------------------------

    def volume_level(
        self,
        samples: List[float]
    ) -> float:


        if not samples:

            return 0.0


        try:

            total = sum(
                sample * sample
                for sample in samples
            )


            rms = math.sqrt(
                total / len(samples)
            )


            return rms


        except Exception as error:


            logger.error(
                f"Volume Calculation Failed: {error}"
            )


            return 0.0    # ------------------------------------------------------
    # Detect Silence
    # ------------------------------------------------------

    def is_silent(
        self,
        samples: List[float]
    ) -> bool:

        level = self.volume_level(
            samples
        )


        silent = (
            level < self.silence_threshold
        )


        if silent:

            logger.debug(
                "Silence Detected"
            )

        else:

            logger.debug(
                "Voice Activity Detected"
            )


        return silent



    # ------------------------------------------------------
    # Noise Level
    # ------------------------------------------------------

    def noise_level(
        self,
        samples: List[float]
    ) -> str:


        level = self.volume_level(
            samples
        )


        if level == 0:

            return "silent"


        if level < 0.05:

            return "low"


        if level < 0.15:

            return "medium"


        return "high"



    # ------------------------------------------------------
    # Normalize Audio Samples
    # ------------------------------------------------------

    def normalize(
        self,
        samples: List[float]
    ) -> List[float]:


        if not samples:

            return []


        try:

            maximum = max(
                abs(x)
                for x in samples
            )


            if maximum == 0:

                return samples


            return [

                x / maximum

                for x in samples

            ]


        except Exception as error:


            logger.error(
                f"Normalization Failed: {error}"
            )


            return samples    # ------------------------------------------------------
    # Voice Activity Detection
    # ------------------------------------------------------

    def has_voice(
        self,
        samples: List[float]
    ) -> bool:

        return not self.is_silent(
            samples
        )


    # ------------------------------------------------------
    # Analyze Audio
    # ------------------------------------------------------

    def analyze(
        self,
        samples: List[float]
    ) -> dict:


        level = self.volume_level(
            samples
        )


        return {

            "volume":
                level,

            "silent":
                self.is_silent(samples),

            "noise":
                self.noise_level(samples),

            "samples":
                len(samples)

        }


    # ------------------------------------------------------
    # Update Threshold
    # ------------------------------------------------------

    def set_threshold(
        self,
        value: float
    ) -> None:


        if value < 0:

            value = 0


        self.silence_threshold = value


        logger.info(
            f"Silence Threshold Updated: {value}"
        )


    # ------------------------------------------------------
    # Status
    # ------------------------------------------------------

    def status(
        self
    ) -> dict:


        return {

            "module":
                "NoiseAnalyzer",

            "threshold":
                self.silence_threshold,

            "ready":
                True

        }



# ==========================================================
# GLOBAL INSTANCE
# ==========================================================

noise = NoiseAnalyzer()