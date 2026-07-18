from __future__ import annotations

import uuid
import threading

from dataclasses import dataclass, field
from typing import Dict, List, Any

from core.memory import memory
from core.context_manager import context
from core.goal_manager import goal_manager


@dataclass
class Decision:

    id: str = field(
        default_factory=lambda: str(uuid.uuid4())
    )

    user_input: str = ""

    intent: str = "unknown"

    goal: str = ""

    confidence: float = 0.0

    actions: List[Dict[str, Any]] = field(
        default_factory=list
    )

    reasoning: List[str] = field(
        default_factory=list
    )


class ReasoningEngine:


    def __init__(self):

        self.lock = threading.RLock()

        self.history: List[Decision] = []


        # ======================================
        # Intent Map
        # ======================================

        self.intent_map = {


            "youtube": {

                "goal": "Open YouTube",

                "priority": 8,

                "action": "youtube",

                "url": "https://youtube.com"

            },


            "google": {

                "goal": "Open Google",

                "priority": 7,

                "action": "google",

                "url": "https://google.com"

            },


            "chrome": {

                "goal": "Open Chrome",

                "priority": 6,

                "action": "chrome",

                "app": "chrome"

            },


            "notepad": {

                "goal": "Open Notepad",

                "priority": 6,

                "action": "open",

                "app": "notepad"

            },


            "vscode": {

                "goal": "Open Visual Studio Code",

                "priority": 6,

                "action": "open",

                "app": "vscode"

            },


            "telegram": {

                "goal": "Open Telegram",

                "priority": 6,

                "action": "open",

                "app": "telegram"

            },


            "discord": {

                "goal": "Open Discord",

                "priority": 6,

                "action": "open",

                "app": "discord"

            },


            "spotify": {

                "goal": "Open Spotify",

                "priority": 6,

                "action": "open",

                "app": "spotify"

            }

        }



    def analyze(self, text: str) -> Decision:


        text = text.strip().lower()


        decision = Decision(

            user_input=text,

            intent="chat",

            goal="Conversation"

        )


        for keyword, config in self.intent_map.items():


            if keyword in text:


                decision.intent = keyword


                decision.goal = config["goal"]


                decision.actions.append(

                    {

                        "action": config["action"],

                        "app": config.get("app"),

                        "query": config.get("query"),

                        "params": config.get("url")

                    }

                )


                decision.reasoning.append(

                    f"User requested {keyword}"

                )


                decision.confidence = 0.95


                break



        if decision.intent == "chat":


            decision.actions.append(

                {

                    "action": "chat",

                    "params": text

                }

            )


            decision.reasoning.append(

                "General conversation"

            )



        with self.lock:

            self.history.append(decision)



        return decision




    def prepare(self, user_input: str) -> Decision:

        return self.analyze(user_input)



    def explain(self, decision):

        return {

            "intent": decision.intent,

            "goal": decision.goal,

            "confidence": decision.confidence,

            "reasoning": decision.reasoning,

            "actions": decision.actions

        }



    def status(self):

        return {

            "history_count": len(self.history),

            "status": "running"

            if len(self.history) > 0

            else "idle"

        }



reasoning_engine = ReasoningEngine()