"""
=========================================================
AYESHA AI
Context Manager
Version : 3.0
=========================================================
"""

from __future__ import annotations

import time
import threading
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Any, Optional

from core.memory import memory


# =========================================================
# Context
# =========================================================

@dataclass
class Context:

    current_goal: str = ""

    current_task: str = ""

    previous_task: str = ""

    user_input: str = ""

    ai_response: str = ""

    language: str = "auto"

    active_app: str = ""

    active_window: str = ""

    screen_text: str = ""

    current_url: str = ""

    timestamp: float = field(default_factory=time.time)

    metadata: Dict[str, Any] = field(default_factory=dict)


# =========================================================
# Context Manager
# =========================================================

class ContextManager:

    def __init__(self):

        self.lock = threading.RLock()

        self.current = Context()

        self.history: List[Context] = []

        self.max_history = 30

    # --------------------------------------------------

    def set_user_input(self, text: str):

        with self.lock:

            self.current.user_input = text

    # --------------------------------------------------

    def set_ai_response(self, text: str):

        with self.lock:

            self.current.ai_response = text

    # --------------------------------------------------

    def set_goal(self, goal: str):

        with self.lock:

            self.current.current_goal = goal

    # --------------------------------------------------

    def set_task(self, task: str):

        with self.lock:

            self.current.previous_task = self.current.current_task

            self.current.current_task = task

    # --------------------------------------------------

    def set_language(self, language: str):

        with self.lock:

            self.current.language = language

    # --------------------------------------------------

    def set_active_app(self, app: str):

        with self.lock:

            self.current.active_app = app

    # --------------------------------------------------

    def set_active_window(self, title: str):

        with self.lock:

            self.current.active_window = title

    # --------------------------------------------------

    def set_screen_text(self, text: str):

        with self.lock:

            self.current.screen_text = text

    # --------------------------------------------------

    def set_url(self, url: str):

        with self.lock:

            self.current.current_url = url

    # --------------------------------------------------

    def add_metadata(self,
                     key: str,
                     value: Any):

        with self.lock:

            self.current.metadata[key] = value

    # --------------------------------------------------

    def save(self):

        with self.lock:

            self.history.append(

                Context(

                    **asdict(self.current)

                )

            )

            if len(self.history) > self.max_history:

                self.history.pop(0)

            memory.add_conversation(

                "user",

                self.current.user_input

            )

            memory.add_conversation(

                "assistant",

                self.current.ai_response

            )    # --------------------------------------------------
    # Get Current Context
    # --------------------------------------------------

    def get_current(self):

        with self.lock:

            return Context(

                **asdict(self.current)

            )

    # --------------------------------------------------
    # Context History
    # --------------------------------------------------

    def get_history(self,
                    limit: int = 10):

        with self.lock:

            return self.history[-limit:]

    # --------------------------------------------------
    # Recent Conversation
    # --------------------------------------------------

    def recent_conversation(self,
                            limit: int = 10):

        return memory.get_conversation(limit)

    # --------------------------------------------------
    # Build AI Context
    # --------------------------------------------------

    def build_context(self):

        with self.lock:

            return {

                "goal":

                    self.current.current_goal,

                "task":

                    self.current.current_task,

                "previous_task":

                    self.current.previous_task,

                "user_input":

                    self.current.user_input,

                "language":

                    self.current.language,

                "active_app":

                    self.current.active_app,

                "active_window":

                    self.current.active_window,

                "screen_text":

                    self.current.screen_text,

                "current_url":

                    self.current.current_url,

                "conversation":

                    [

                        asdict(x)

                        for x in

                        memory.get_conversation(10)

                    ],

                "memory":

                    memory.statistics(),

                "metadata":

                    self.current.metadata

            }

    # --------------------------------------------------
    # AI Prompt Context
    # --------------------------------------------------

    def prompt_context(self):

        ctx = self.build_context()

        prompt = f"""

Goal:
{ctx['goal']}

Current Task:
{ctx['task']}

Previous Task:
{ctx['previous_task']}

User:
{ctx['user_input']}

Language:
{ctx['language']}

Active App:
{ctx['active_app']}

Window:
{ctx['active_window']}

URL:
{ctx['current_url']}

Screen:
{ctx['screen_text']}

"""

        return prompt.strip()

    # --------------------------------------------------
    # Reset
    # --------------------------------------------------

    def clear(self):

        with self.lock:

            self.current = Context()

    # --------------------------------------------------
    # Status
    # --------------------------------------------------

    def status(self):

        return {

            "module": "ContextManager",

            "history":

                len(self.history),

            "goal":

                self.current.current_goal,

            "task":

                self.current.current_task,

            "active_app":

                self.current.active_app,

            "ready": True

        }


context = ContextManager()