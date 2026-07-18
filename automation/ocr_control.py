"""
================================================================
AYESHA AI
OCR CONTROL MODULE

Version : 3.0.0
Status  : Production

Author  : AYESHA Project

Purpose
-------
Screen OCR Engine

Features
--------
✓ Screenshot
✓ Region Screenshot
✓ OCR
✓ Text Search
✓ Position Detection
✓ Multi Language
✓ Logging
✓ Error Handling
✓ Vision Ready

================================================================
"""

from __future__ import annotations

import logging

from pathlib import Path

from typing import Optional
from typing import Tuple
from typing import Dict
from typing import Any

import pytesseract

from PIL import Image
from PIL import ImageGrab


logger = logging.getLogger(
    "AYESHA_CORE"
)


# ==============================================================
# TESSERACT CONFIGURATION
# ==============================================================

DEFAULT_TESSERACT_PATH = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


if Path(DEFAULT_TESSERACT_PATH).exists():

    pytesseract.pytesseract.tesseract_cmd = (
        DEFAULT_TESSERACT_PATH
    )

    logger.info(
        "Tesseract Loaded"
    )

else:

    logger.warning(
        "Tesseract Not Found"
    )


# ==============================================================
# OCR CONTROLLER
# ==============================================================

class OCRController:


    """
    Production OCR Engine
    """


    def __init__(self):

        self.default_language = "eng"

        logger.info(
            "OCR Controller Initialized"
        )    # ==========================================================
    # Screenshot
    # ==========================================================

    def screenshot(
        self,
        save_path: Optional[str] = None,
        region: Optional[
            Tuple[int, int, int, int]
        ] = None
    ) -> Optional[Image.Image]:

        """
        Capture Screenshot

        region:
        (left, top, right, bottom)
        """

        try:

            image = ImageGrab.grab(
                bbox=region
            )

            if save_path:

                save_file = Path(
                    save_path
                )

                save_file.parent.mkdir(
                    parents=True,
                    exist_ok=True
                )

                image.save(
                    save_file
                )

                logger.info(
                    f"Screenshot Saved : {save_file}"
                )

            else:

                logger.info(
                    "Screenshot Captured"
                )

            return image

        except Exception:

            logger.exception(
                "Screenshot Failed"
            )

            return None


    # ==========================================================
    # Save Screenshot
    # ==========================================================

    def save_screenshot(
        self,
        file_path: str
    ) -> bool:

        """
        Save Current Screen
        """

        image = self.screenshot()

        if image is None:

            return False

        try:

            path = Path(
                file_path
            )

            path.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            image.save(path)

            logger.info(
                f"Saved : {path}"
            )

            return True

        except Exception:

            logger.exception(
                "Save Screenshot Failed"
            )

            return False    # ==========================================================
    # Read Screen
    # ==========================================================

    def read_screen(
        self,
        language: Optional[str] = None,
        region: Optional[
            Tuple[int, int, int, int]
        ] = None
    ) -> str:

        """
        Read text from the current screen.
        """

        try:

            image = self.screenshot(
                region=region
            )

            if image is None:
                return ""

            lang = (
                language
                or self.default_language
            )

            text = pytesseract.image_to_string(
                image,
                lang=lang
            )

            logger.info(
                "Screen OCR Completed"
            )

            return text.strip()

        except Exception:

            logger.exception(
                "Screen OCR Failed"
            )

            return ""


    # ==========================================================
    # Read Image
    # ==========================================================

    def read_image(
        self,
        image_path: str,
        language: Optional[str] = None
    ) -> str:

        """
        Read text from an image file.
        """

        try:

            path = Path(image_path)

            if not path.exists():

                logger.warning(
                    f"Image Not Found : {image_path}"
                )

                return ""

            lang = (
                language
                or self.default_language
            )

            with Image.open(path) as image:

                text = pytesseract.image_to_string(
                    image,
                    lang=lang
                )

            logger.info(
                f"OCR Success : {image_path}"
            )

            return text.strip()

        except Exception:

            logger.exception(
                "Image OCR Failed"
            )

            return ""    # ==========================================================
    # Find Text
    # ==========================================================

    def find_text(
        self,
        keyword: str,
        language: Optional[str] = None
    ) -> bool:

        """
        Search keyword on screen.
        """

        screen_text = self.read_screen(
            language=language
        )

        if not screen_text:

            return False

        found = (
            keyword.lower()
            in screen_text.lower()
        )

        if found:

            logger.info(
                f"Text Found : {keyword}"
            )

        else:

            logger.info(
                f"Text Not Found : {keyword}"
            )

        return found


    # ==========================================================
    # Find Text Position
    # ==========================================================

    def find_text_position(
        self,
        keyword: str,
        language: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:

        """
        Return text position and confidence.
        """

        try:

            image = self.screenshot()

            if image is None:

                return None

            lang = (
                language
                or self.default_language
            )

            data = pytesseract.image_to_data(
                image,
                lang=lang,
                output_type=pytesseract.Output.DICT
            )

            total = len(
                data["text"]
            )

            for index in range(total):

                text = (
                    data["text"][index]
                    .strip()
                )

                if not text:

                    continue

                confidence = float(
                    data["conf"][index]
                )

                if (
                    text.lower()
                    == keyword.lower()
                    and confidence >= 40
                ):

                    return {

                        "text": text,

                        "confidence": confidence,

                        "left": data["left"][index],

                        "top": data["top"][index],

                        "width": data["width"][index],

                        "height": data["height"][index]

                    }

            logger.info(
                f"Position Not Found : {keyword}"
            )

            return None

        except Exception:

            logger.exception(
                "Find Text Position Failed"
            )

            return None    # ==========================================================
    # Set Language
    # ==========================================================

    def set_language(
        self,
        language: str
    ) -> None:
        """
        Change the default OCR language.
        """

        self.default_language = language

        logger.info(
            f"OCR Language Changed : {language}"
        )


    # ==========================================================
    # Get Version
    # ==========================================================

    def get_version(
        self
    ) -> str:
        """
        Return installed Tesseract version.
        """

        try:

            version = str(
                pytesseract.get_tesseract_version()
            )

            return version

        except Exception:

            logger.exception(
                "Unable to get Tesseract version"
            )

            return "Unknown"


    # ==========================================================
    # OCR Available
    # ==========================================================

    def is_available(
        self
    ) -> bool:
        """
        Check whether Tesseract is available.
        """

        try:

            pytesseract.get_tesseract_version()

            return True

        except Exception:

            return False


# ==============================================================
# Global Instance
# ==============================================================

ocr = OCRController()