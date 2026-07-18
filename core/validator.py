"""
================================================================
AYESHA AI - INPUT VALIDATOR SYSTEM
Version : 1.0.0

Purpose:
Validates user commands before execution.

Features:
- Input validation
- Command length check
- Dangerous input filtering
- Type hints
- Logging
- Error handling
- Future security integration
================================================================
"""

import logging
from typing import Tuple, List


logger = logging.getLogger("AYESHA_CORE")


# ===============================================================
# Validator
# ===============================================================

class Validator:


    def __init__(self):

        self.blocked_words: List[str] = [

            "delete system32",
            "format disk",
            "shutdown -s"

        ]


        logger.info(
            "Validator Initialized"
        )



    # -----------------------------------------------------------
    # Validate Command
    # -----------------------------------------------------------

    def validate(
        self,
        command: str
    ) -> Tuple[bool, str]:


        try:

            # Empty check

            if not command:

                return (
                    False,
                    "Command is empty"
                )



            command = command.strip()



            # Length check

            if len(command) < 2:

                return (
                    False,
                    "Command too short"
                )



            if len(command) > 500:

                return (
                    False,
                    "Command too long"
                )



            # Security check

            lowered = command.lower()


            for word in self.blocked_words:


                if word in lowered:

                    logger.warning(
                        f"Blocked command: {command}"
                    )


                    return (
                        False,
                        "Unsafe command blocked"
                    )



            return (
                True,
                "Command valid"
            )



        except Exception as error:


            logger.error(
                f"Validation Error: {error}"
            )


            return (
                False,
                "Validator error"
            )



    # -----------------------------------------------------------
    # Add Blocked Word
    # -----------------------------------------------------------

    def add_block(
        self,
        word: str
    ):

        if word not in self.blocked_words:

            self.blocked_words.append(
                word
            )


            logger.info(
                f"Added blocked rule: {word}"
            )



    # -----------------------------------------------------------
    # Remove Block
    # -----------------------------------------------------------

    def remove_block(
        self,
        word: str
    ):


        if word in self.blocked_words:

            self.blocked_words.remove(
                word
            )


            logger.info(
                f"Removed blocked rule: {word}"
            )



# ===============================================================
# Global Instance
# ===============================================================

validator = Validator()