"""
================================================================
AYESHA AI - PROCESS AUTOMATION MODULE
Version : 1.0.0

Purpose:
Controls Windows processes and applications.

Features:
- Launch applications
- Check running processes
- Get process list
- Terminate process
- Logging
- Error handling
================================================================
"""

import logging
import subprocess
from typing import List, Dict, Optional

import psutil


logger = logging.getLogger("AYESHA_CORE")



# ===============================================================
# Process Manager
# ===============================================================

class ProcessManager:


    def __init__(self):

        logger.info(
            "Process Manager Initialized"
        )



    # -----------------------------------------------------------
    # Launch Application
    # -----------------------------------------------------------

    def launch(
        self,
        app_path: str
    ) -> bool:


        try:

            subprocess.Popen(
                app_path
            )


            logger.info(
                f"Application Started: {app_path}"
            )


            return True



        except Exception as error:


            logger.error(
                f"Launch Failed: {error}"
            )


            return False



    # -----------------------------------------------------------
    # Check Process Running
    # -----------------------------------------------------------

    def is_running(
        self,
        process_name: str
    ) -> bool:


        try:

            for process in psutil.process_iter(
                ["name"]
            ):

                if process.info["name"]:


                    if process_name.lower() in process.info["name"].lower():

                        return True



            return False



        except Exception as error:


            logger.error(
                f"Process Check Failed: {error}"
            )


            return False



    # -----------------------------------------------------------
    # Get Process List
    # -----------------------------------------------------------

    def list_processes(
        self,
        limit: int = 20
    ) -> List[Dict]:


        processes = []


        try:

            for process in psutil.process_iter(
                [
                    "pid",
                    "name",
                    "memory_percent"
                ]
            ):


                processes.append(
                    process.info
                )


                if len(processes) >= limit:

                    break



            return processes



        except Exception as error:


            logger.error(
                f"Process List Failed: {error}"
            )


            return []



    # -----------------------------------------------------------
    # Kill Process
    # -----------------------------------------------------------

    def terminate(
        self,
        process_name: str
    ) -> bool:


        try:

            for process in psutil.process_iter(
                ["name"]
            ):


                if process.info["name"]:


                    if process_name.lower() in process.info["name"].lower():

                        process.terminate()


                        logger.info(
                            f"Process Closed: {process_name}"
                        )


                        return True



            return False



        except Exception as error:


            logger.error(
                f"Terminate Failed: {error}"
            )


            return False



    # -----------------------------------------------------------
    # System Resource Info
    # -----------------------------------------------------------

    def system_usage(
        self
    ) -> Dict:


        try:

            return {

                "cpu":
                psutil.cpu_percent(),

                "memory":
                psutil.virtual_memory()
                .percent

            }


        except Exception as error:


            logger.error(
                f"System Usage Failed: {error}"
            )


            return {}



# ===============================================================
# Global Instance
# ===============================================================

process_manager = ProcessManager()