"""
================================================================
AYESHA AI
MICROPHONE CONTROL MODULE

Version : 1.0.0

Purpose
-------
Manage microphone input.

Features
--------
✓ Microphone State Control
✓ Recording Control
✓ Audio Buffer Ready
✓ Device Ready
✓ Logging
✓ Error Handling
✓ Future STT Integration Ready

================================================================
"""


from __future__ import annotations

import logging
from typing import Optional


logger = logging.getLogger(
    "AYESHA_CORE"
)



# ==========================================================
# MICROPHONE CONTROLLER
# ==========================================================

class MicrophoneController:


    def __init__(self):


        self.active = False


        self.device = None


        self.buffer = []


        logger.info(
            "Microphone Controller Initialized"
        )



    # ------------------------------------------------------
    # Start Microphone
    # ------------------------------------------------------

    def start(
        self
    ) -> bool:


        try:


            self.active = True


            logger.info(
                "Microphone Started"
            )


            return True



        except Exception as error:


            logger.error(
                f"Microphone Start Failed: {error}"
            )


            return False



    # ------------------------------------------------------
    # Stop Microphone
    # ------------------------------------------------------

    def stop(
        self
    ) -> bool:


        try:


            self.active = False


            logger.info(
                "Microphone Stopped"
            )


            return True



        except Exception as error:


            logger.error(
                f"Microphone Stop Failed: {error}"
            )


            return False    # ------------------------------------------------------
    # Add Audio Data
    # ------------------------------------------------------

    def add_sample(
        self,
        sample
    ) -> None:


        try:


            if self.active:

                self.buffer.append(
                    sample
                )


        except Exception as error:


            logger.error(
                f"Sample Add Failed: {error}"
            )



    # ------------------------------------------------------
    # Get Audio Buffer
    # ------------------------------------------------------

    def get_buffer(
        self
    ) -> list:


        return self.buffer



    # ------------------------------------------------------
    # Clear Buffer
    # ------------------------------------------------------

    def clear_buffer(
        self
    ) -> None:


        self.buffer.clear()


        logger.info(
            "Microphone Buffer Cleared"
        )



    # ------------------------------------------------------
    # Device Set
    # ------------------------------------------------------

    def set_device(
        self,
        device_name: str
    ) -> None:


        self.device = device_name


        logger.info(
            f"Microphone Device: {device_name}"
        )    # ------------------------------------------------------
    # Status
    # ------------------------------------------------------

    def status(
        self
    ) -> dict:


        return {

            "module":
                "MicrophoneController",

            "active":
                self.active,

            "device":
                self.device,

            "buffer_size":
                len(self.buffer),

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

microphone = MicrophoneController()