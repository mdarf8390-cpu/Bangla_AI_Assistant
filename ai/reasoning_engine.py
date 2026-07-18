from __future__ import annotations

import asyncio

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Dict, Any, Callable, Awaitable

from core.memory_manager import memory
from automation.action_executor import action_executor


# =========================================================
# Brain State
# =========================================================

class BrainState(Enum):

    IDLE = auto()

    OBSERVING = auto()

    ANALYZING = auto()

    EXECUTING = auto()

    FINISHED = auto()

    ERROR = auto()


# =========================================================
# Event
# =========================================================

@dataclass
class ReasoningEvent:

    state: BrainState

    payload: Any = None

    metadata: Dict[str, Any] = field(default_factory=dict)


# =========================================================
# Result
# =========================================================

@dataclass
class ReasoningResult:

    success: bool = True

    response: str = ""

    actions: List[Dict[str, Any]] = field(default_factory=list)

    state: BrainState = BrainState.IDLE

    error: str = ""

# =========================================================
# Reasoning Engine
# =========================================================

class ReasoningEngine:

    def __init__(self):

        self.state = BrainState.IDLE

        self.history: List[ReasoningResult] = []

        self.hooks: Dict[
            BrainState,
            List[Callable[[ReasoningEvent], Awaitable[None]]]
        ] = {}


    # =====================================================
    # Hook Register
    # =====================================================

    def register_hook(self, state, callback):

        self.hooks.setdefault(state, []).append(callback)


    def unregister_hook(self, state, callback):

        if state in self.hooks:

            if callback in self.hooks[state]:

                self.hooks[state].remove(callback)


    async def _emit(self, state, payload=None):

        self.state = state

        event = ReasoningEvent(

            state=state,

            payload=payload

        )

        for callback in self.hooks.get(state, []):

            try:

                await callback(event)

            except Exception as e:

                print("Hook Error:", e)


    # =====================================================
    # Async Intent Processor
    # =====================================================

    async def process_intent(self, text: str):

        await self._emit(

            BrainState.OBSERVING,

            text

        )

        if hasattr(memory, "add_conversation"):

            memory.add_conversation(

                "user",

                text

            )

        await asyncio.sleep(0)

        await self._emit(

            BrainState.ANALYZING,

            text

        )

        response = f"আমি বুঝতে পেরেছি: {text}"

        await asyncio.sleep(0)

        await self._emit(

            BrainState.EXECUTING,

            response

        )

        try:

            action_executor.execute(

                "speak",

                response

            )

        except Exception:

            pass

        if hasattr(memory, "add_conversation"):

            memory.add_conversation(

                "assistant",

                response

            )

        result = ReasoningResult(

            success=True,

            response=response,

            actions=[

                {

                    "action": "speak",

                    "text": response

                }

            ],

            state=BrainState.FINISHED

        )

        self.history.append(result)

        self.state = BrainState.FINISHED

        return result

    # =====================================================
    # Backward Compatible API
    # =====================================================

    def process_input(self, user_text: str):
        """
        পুরোনো কোডের জন্য Compatibility।
        Async process_intent() কে Sync ভাবে চালায়।
        """

        try:

            result = asyncio.run(
                self.process_intent(user_text)
            )

            return result

        except RuntimeError:
            # যদি আগে থেকেই Event Loop চলতে থাকে

            loop = asyncio.get_event_loop()

            return loop.run_until_complete(
                self.process_intent(user_text)
            )


    # =====================================================
    # Status
    # =====================================================

    def status(self):

        return {

            "module": "ReasoningEngine",

            "state": self.state.name,

            "history": len(self.history),

            "hooks": sum(
                len(v) for v in self.hooks.values()
            ),

            "ready": True

        }


# =========================================================
# Singleton
# =========================================================

reasoning_engine = ReasoningEngine()
