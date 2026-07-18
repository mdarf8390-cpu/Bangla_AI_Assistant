"""
================================================================
AYESHA AI - COMMAND HISTORY SYSTEM
Version : 1.0.0

Purpose:
Stores user command execution history.

Features:
- Async support
- Type hints
- Logging
- Error handling
- Future database integration
================================================================
"""

import logging
import uuid
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Optional


logger = logging.getLogger("AYESHA_CORE")


# ===============================================================
# Command Record
# ===============================================================

@dataclass
class CommandRecord:

    id: str
    command: str
    status: str
    result: Optional[str]
    timestamp: str



# ===============================================================
# Command History Manager
# ===============================================================

class CommandHistory:


    def __init__(self):

        self.history: List[CommandRecord] = []

        logger.info(
            "Command History Initialized"
        )



    # -----------------------------------------------------------
    # Add Command
    # -----------------------------------------------------------

    def add(
        self,
        command: str,
        status: str = "pending",
        result: Optional[str] = None
    ) -> CommandRecord:

        try:

            record = CommandRecord(

                id=str(uuid.uuid4()),

                command=command,

                status=status,

                result=result,

                timestamp=datetime.now()
                .strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            )


            self.history.append(
                record
            )


            logger.info(
                f"Command Added: {command}"
            )


            return record


        except Exception as error:

            logger.error(
                f"History Add Failed: {error}"
            )

            raise



    # -----------------------------------------------------------
    # Update Status
    # -----------------------------------------------------------

    def update_status(
        self,
        command_id: str,
        status: str,
        result: Optional[str] = None
    ):


        for item in self.history:

            if item.id == command_id:


                item.status = status

                item.result = result


                logger.info(
                    f"Command Updated: {status}"
                )

                return True



        logger.warning(
            "Command ID Not Found"
        )

        return False



    # -----------------------------------------------------------
    # Get All History
    # -----------------------------------------------------------

    def get_all(
        self
    ) -> List[dict]:


        return [
            asdict(item)
            for item in self.history
        ]



    # -----------------------------------------------------------
    # Last Command
    # -----------------------------------------------------------

    def last(
        self
    ) -> Optional[dict]:


        if not self.history:

            return None


        return asdict(
            self.history[-1]
        )



    # -----------------------------------------------------------
    # Clear History
    # -----------------------------------------------------------

    def clear(
        self
    ):

        self.history.clear()

        logger.info(
            "Command History Cleared"
        )



# ===============================================================
# Global Instance
# ===============================================================

command_history = CommandHistory()