"""
================================================================
AYESHA AI
LANGUAGE DETECTION MODULE

Version : 1.0.0

Purpose
-------
Detect and manage user language.

Features
--------
✓ Bangla Detection
✓ English Detection
✓ Mixed Language Support
✓ Language Preference
✓ Logging
✓ Future STT Ready

================================================================
"""


from __future__ import annotations

import logging
from typing import Dict


logger = logging.getLogger(
    "AYESHA_CORE"
)


# ==========================================================
# LANGUAGE TYPES
# ==========================================================

SUPPORTED_LANGUAGES = {

    "bangla": "bn",

    "english": "en",

    "mixed": "mix"

}


# ==========================================================
# LANGUAGE MANAGER
# ==========================================================

class LanguageManager:


    def __init__(self):

        self.default_language = (
            "english"
        )

        self.user_language = (
            self.default_language
        )


        logger.info(
            "Language Manager Initialized"
        )



    # ------------------------------------------------------
    # Detect Bangla Characters
    # ------------------------------------------------------

    def contains_bangla(
        self,
        text: str
    ) -> bool:


        for char in text:

            if "\u0980" <= char <= "\u09FF":

                return True


        return False    # ------------------------------------------------------
    # Detect English Characters
    # ------------------------------------------------------

    def contains_english(
        self,
        text: str
    ) -> bool:


        for char in text:


            if char.isalpha() and char.isascii():

                return True


        return False



    # ------------------------------------------------------
    # Detect Language
    # ------------------------------------------------------

    def detect(
        self,
        text: str
    ) -> str:


        if not text:

            return self.default_language



        has_bn = self.contains_bangla(
            text
        )


        has_en = self.contains_english(
            text
        )



        if has_bn and has_en:

            return "mixed"



        if has_bn:

            return "bangla"



        if has_en:

            return "english"



        return self.default_language



    # ------------------------------------------------------
    # Language Code
    # ------------------------------------------------------

    def code(
        self,
        language: str
    ) -> str:


        return SUPPORTED_LANGUAGES.get(

            language,

            SUPPORTED_LANGUAGES[
                self.default_language
            ]

        )    # ------------------------------------------------------
    # Set User Language
    # ------------------------------------------------------

    def set_language(
        self,
        language: str
    ) -> bool:


        if language not in SUPPORTED_LANGUAGES:

            logger.warning(
                f"Unsupported Language: {language}"
            )

            return False


        self.user_language = language


        logger.info(
            f"User Language Set: {language}"
        )


        return True



    # ------------------------------------------------------
    # Get Current Language
    # ------------------------------------------------------

    def get_language(
        self
    ) -> str:


        return self.user_language



    # ------------------------------------------------------
    # Analyze Text
    # ------------------------------------------------------

    def analyze(
        self,
        text: str
    ) -> Dict[str, str]:


        detected = self.detect(
            text
        )


        return {

            "language":
                detected,

            "code":
                self.code(
                    detected
                ),

            "text":
                text

        }



    # ------------------------------------------------------
    # Status
    # ------------------------------------------------------

    def status(
        self
    ) -> dict:


        return {

            "module":
                "LanguageManager",

            "current":
                self.user_language,

            "supported":
                list(
                    SUPPORTED_LANGUAGES.keys()
                ),

            "ready":
                True

        }



# ==========================================================
# GLOBAL INSTANCE
# ==========================================================

language = LanguageManager()