"""
================================================================
AYESHA AI - CLIPBOARD AUTOMATION MODULE
Version : 1.0.0

Purpose:
Controls system clipboard.

Features:
- Read clipboard
- Write clipboard
- Clear clipboard
- Logging
- Error handling
- Future Event Bus integration
================================================================
"""

import logging
from typing import Optional

import pyperclip


logger = logging.getLogger("AYESHA_CORE")


# ===============================================================
# Clipboard Controller
# ===============================================================

class ClipboardManager:


    def __init__(self):

        logger.info(
            "Clipboard Manager Initialized"
        )



    # -----------------------------------------------------------
    # Copy Text
    # -----------------------------------------------------------

    def copy(
        self,
        text: str
    ) -> bool:


        try:

            pyperclip.copy(
                text
            )


            logger.info(
                "Text copied to clipboard"
            )


            return True



        except Exception as error:


            logger.error(
                f"Copy Failed: {error}"
            )


            return False



    # -----------------------------------------------------------
    # Paste / Read
    # -----------------------------------------------------------

    def paste(
        self
    ) -> Optional[str]:


        try:

            data = pyperclip.paste()


            logger.info(
                "Clipboard read successful"
            )


            return data



        except Exception as error:


            logger.error(
                f"Paste Failed: {error}"
            )


            return None



    # -----------------------------------------------------------
    # Clear Clipboard
    # -----------------------------------------------------------

    def clear(
        self
    ) -> bool:


        try:

            pyperclip.copy("")


            logger.info(
                "Clipboard cleared"
            )


            return True



        except Exception as error:


            logger.error(
                f"Clear Failed: {error}"
            )


            return False



# ===============================================================
# Global Instance
# ===============================================================

clipboard = ClipboardManager()