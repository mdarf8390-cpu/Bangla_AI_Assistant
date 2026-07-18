"""
===============================================================
AYESHA AI - EVENT BUS SYSTEM
Version : 1.0.0

Purpose:
Central event communication system.
All modules communicate through events.
===============================================================
"""

import asyncio
import logging
from typing import (
    Dict,
    List,
    Callable,
    Awaitable,
    Any
)
from dataclasses import dataclass
from datetime import datetime


logger = logging.getLogger("AYESHA_CORE")


# =============================================================
# Event Object
# =============================================================

@dataclass
class Event:

    name: str
    payload: Any = None
    timestamp: datetime = datetime.now()



# =============================================================
# Event Bus
# =============================================================

class EventBus:


    def __init__(self):

        self.listeners: Dict[
            str,
            List[Callable[..., Awaitable]]
        ] = {}

        logger.info(
            "Event Bus Initialized"
        )


    # ---------------------------------------------------------
    # Subscribe
    # ---------------------------------------------------------

    def subscribe(
        self,
        event_name: str,
        callback: Callable[..., Awaitable]
    ):

        if event_name not in self.listeners:

            self.listeners[event_name] = []


        self.listeners[event_name].append(
            callback
        )


        logger.info(
            f"Listener Added: {event_name}"
        )



    # ---------------------------------------------------------
    # Emit Event (Production Safe)
    # ---------------------------------------------------------

    async def emit(
        self,
        event_name: str,
        payload: Any = None
    ):

        if event_name not in self.listeners:
            return

        event = Event(
            name=event_name,
            payload=payload
        )

        logger.info(
            f"Event Fired: {event_name}"
        )

        tasks = []
        for callback in self.listeners[event_name]:
            
            # লিসেনারের নাম বের করা (lambda ফাংশনের ক্ষেত্রেও কাজ করবে)
            listener_name = getattr(callback, "__name__", "unknown_callback")

            # র‍্যাপার ফাংশন যাতে একটির এরর অন্যটিকে না থামায়
            async def safe_run(cb, ev, name):
                try:
                    await cb(ev)
                except Exception as e:
                    logger.error(f"Error in listener '{name}' for event '{event_name}': {e}")
            
            tasks.append(safe_run(callback, event, listener_name))

        # সব টাস্ক একসাথে রান হবে
        if tasks:
            await asyncio.gather(*tasks)



    # ---------------------------------------------------------
    # Remove Listener
    # ---------------------------------------------------------

    def unsubscribe(
        self,
        event_name: str,
        callback
    ):

        if event_name in self.listeners:

            if callback in self.listeners[event_name]:

                self.listeners[event_name].remove(
                    callback
                )

                logger.info(
                    f"Listener Removed: {event_name}"
                )



# =============================================================
# Global Event Bus Instance
# =============================================================

event_bus = EventBus()