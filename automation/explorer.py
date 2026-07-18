"""
================================================================
AYESHA AI - EXPLORER AUTOMATION MODULE
Version : 1.0.0

Purpose:
Controls Windows File Explorer.

Features:
- Open folders
- Open files
- Check path
- Create folders
- Logging
- Error handling
- Future Event Bus integration
================================================================
"""

import logging
import os
import subprocess
from pathlib import Path
from typing import Optional


logger = logging.getLogger("AYESHA_CORE")


# ===============================================================
# Explorer Controller
# ===============================================================

class ExplorerManager:


    def __init__(self):

        logger.info(
            "Explorer Manager Initialized"
        )



    # -----------------------------------------------------------
    # Open Folder
    # -----------------------------------------------------------

    def open_folder(
        self,
        path: str
    ) -> bool:


        try:

            folder = Path(path)


            if not folder.exists():

                logger.warning(
                    f"Folder not found: {path}"
                )

                return False



            os.startfile(
                str(folder)
            )


            logger.info(
                f"Folder Opened: {path}"
            )


            return True



        except Exception as error:


            logger.error(
                f"Open Folder Failed: {error}"
            )


            return False



    # -----------------------------------------------------------
    # Open File
    # -----------------------------------------------------------

    def open_file(
        self,
        path: str
    ) -> bool:


        try:

            file = Path(path)


            if not file.exists():

                logger.warning(
                    f"File not found: {path}"
                )

                return False



            os.startfile(
                str(file)
            )


            logger.info(
                f"File Opened: {path}"
            )


            return True



        except Exception as error:


            logger.error(
                f"Open File Failed: {error}"
            )


            return False



    # -----------------------------------------------------------
    # Open Explorer Home
    # -----------------------------------------------------------

    def open_explorer(
        self
    ) -> bool:


        try:

            subprocess.Popen(
                "explorer"
            )


            logger.info(
                "Explorer Started"
            )


            return True



        except Exception as error:


            logger.error(
                f"Explorer Start Failed: {error}"
            )


            return False



    # -----------------------------------------------------------
    # Check Path
    # -----------------------------------------------------------

    def exists(
        self,
        path: str
    ) -> bool:


        return Path(path).exists()



    # -----------------------------------------------------------
    # Create Folder
    # -----------------------------------------------------------

    def create_folder(
        self,
        path: str
    ) -> bool:


        try:

            Path(path).mkdir(
                parents=True,
                exist_ok=True
            )


            logger.info(
                f"Folder Created: {path}"
            )


            return True



        except Exception as error:


            logger.error(
                f"Create Folder Failed: {error}"
            )


            return False



# ===============================================================
# Global Instance
# ===============================================================

explorer = ExplorerManager()