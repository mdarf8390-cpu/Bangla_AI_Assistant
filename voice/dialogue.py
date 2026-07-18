"""
================================================================
AYESHA AI
DIALOGUE MODULE

Version : 1.0.0
Status  : Production

Purpose
-------
Conversation Manager

Features
--------
✓ Chat History
✓ Session Management
✓ Context Memory
✓ Response Queue
✓ Bangla + English
✓ Future LLM Ready
✓ Future TTS Ready
✓ EventBus Ready

================================================================
"""

from __future__ import annotations

import logging
import uuid
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime
from typing import Deque
from typing import Dict
from typing import List
from typing import Optional


logger = logging.getLogger(
    "AYESHA_CORE"
)


# ==========================================================
# MESSAGE
# ==========================================================

@dataclass(slots=True)
class DialogueMessage:

    role: str

    content: str

    timestamp: datetime = field(
        default_factory=datetime.now
    )


# ==========================================================
# SESSION
# ==========================================================

class DialogueSession:

    def __init__(self):

        self.session_id = str(
            uuid.uuid4()
        )

        self.created_at = datetime.now()

        self.messages: List[
            DialogueMessage
        ] = []

        logger.info(
            "Dialogue Session Created"
        )# ==========================================================
# CONVERSATION MANAGER
# ==========================================================

class ConversationManager:

    def __init__(self):

        self.session = DialogueSession()

        self.response_queue: Deque[str] = deque()

        self.context: Dict[
            str,
            str
        ] = {}

        logger.info(
            "Conversation Manager Initialized"
        )


    # ------------------------------------------------------
    # Add Message
    # ------------------------------------------------------

    def add_message(
        self,
        role: str,
        content: str
    ) -> None:

        message = DialogueMessage(
            role=role,
            content=content
        )

        self.session.messages.append(
            message
        )

        logger.info(
            f"{role} Message Added"
        )


    # ------------------------------------------------------
    # History
    # ------------------------------------------------------

    def get_history(
        self
    ) -> List[DialogueMessage]:

        return list(
            self.session.messages
        )


    # ------------------------------------------------------
    # Clear History
    # ------------------------------------------------------

    def clear_history(
        self
    ) -> None:

        self.session.messages.clear()

        logger.info(
            "Conversation History Cleared"
        )


    # ------------------------------------------------------
    # Count
    # ------------------------------------------------------

    def message_count(
        self
    ) -> int:

        return len(
            self.session.messages
        )    # ------------------------------------------------------
    # Context
    # ------------------------------------------------------

    def set_context(
        self,
        key: str,
        value: str
    ) -> None:

        self.context[key] = value

        logger.info(
            f"Context Updated : {key}"
        )


    def get_context(
        self,
        key: str,
        default: Optional[str] = None
    ) -> Optional[str]:

        return self.context.get(
            key,
            default
        )


    def clear_context(
        self
    ) -> None:

        self.context.clear()

        logger.info(
            "Context Cleared"
        )


    # ------------------------------------------------------
    # Response Queue
    # ------------------------------------------------------

    def queue_response(
        self,
        response: str
    ) -> None:

        self.response_queue.append(
            response
        )


    def next_response(
        self
    ) -> Optional[str]:

        if not self.response_queue:

            return None

        return self.response_queue.popleft()


    def queue_size(
        self
    ) -> int:

        return len(
            self.response_queue
        )


    # ------------------------------------------------------
    # Last Messages
    # ------------------------------------------------------

    def last_message(
        self
    ) -> Optional[DialogueMessage]:

        if not self.session.messages:

            return None

        return self.session.messages[-1]


    def last_user_message(
        self
    ) -> Optional[DialogueMessage]:

        for message in reversed(
            self.session.messages
        ):

            if message.role == "user":

                return message

        return None


    def last_assistant_message(
        self
    ) -> Optional[DialogueMessage]:

        for message in reversed(
            self.session.messages
        ):

            if message.role == "assistant":

                return message

        return None    # ------------------------------------------------------
    # Remove Last Message
    # ------------------------------------------------------

    def remove_last_message(
        self
    ) -> Optional[DialogueMessage]:

        if not self.session.messages:

            return None

        message = self.session.messages.pop()

        logger.info(
            "Last Message Removed"
        )

        return message


    # ------------------------------------------------------
    # Session Information
    # ------------------------------------------------------

    def session_id(
        self
    ) -> str:

        return self.session.session_id


    def created_time(
        self
    ):

        return self.session.created_at


    # ------------------------------------------------------
    # Export Conversation
    # ------------------------------------------------------

    def export_history(
        self
    ) -> List[dict]:

        history = []

        for message in self.session.messages:

            history.append(

                {
                    "role": message.role,
                    "content": message.content,
                    "timestamp": (
                        message.timestamp.isoformat()
                    )
                }

            )

        return history


    # ------------------------------------------------------
    # Reset Session
    # ------------------------------------------------------

    def reset_session(
        self
    ) -> None:

        self.session = DialogueSession()

        self.response_queue.clear()

        self.context.clear()

        logger.info(
            "Dialogue Session Reset"
        )


    # ------------------------------------------------------
    # Status
    # ------------------------------------------------------

    def is_empty(
        self
    ) -> bool:

        return len(
            self.session.messages
        ) == 0    # ------------------------------------------------------
    # Recent Messages
    # ------------------------------------------------------

    def recent_messages(
        self,
        limit: int = 5
    ) -> List[DialogueMessage]:

        if limit <= 0:

            return []

        return self.session.messages[-limit:]


    # ------------------------------------------------------
    # Statistics
    # ------------------------------------------------------

    def statistics(
        self
    ) -> dict:

        return {

            "session_id":
                self.session.session_id,

            "messages":
                len(self.session.messages),

            "context_items":
                len(self.context),

            "queue_size":
                len(self.response_queue),

            "created":
                self.session.created_at.isoformat()

        }


    # ------------------------------------------------------
    # Magic Methods
    # ------------------------------------------------------

    def __len__(
        self
    ) -> int:

        return len(
            self.session.messages
        )


    def __iter__(
        self
    ):

        return iter(
            self.session.messages
        )


# ==========================================================
# GLOBAL DIALOGUE INSTANCE
# ==========================================================

dialogue = ConversationManager()