"""
=========================================================
AYESHA AI
Production Brain V6 FIXED
=========================================================
"""

from __future__ import annotations

import json
import time
import threading
import requests

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional

from core.memory import memory
from core.context_manager import context
from core.reasoning_engine import reasoning_engine
from core.prompt_builder import prompt_builder
from core.json_parser import json_parser


# =========================================================
# Configuration
# =========================================================

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

MODEL = "qwen3:1.7b"

REQUEST_TIMEOUT = 120

MAX_HISTORY = 100

MAX_RETRY = 3



# =========================================================
# System Prompt
# =========================================================

SYSTEM_PROMPT = """
You are AYESHA.

Advanced personal AI assistant.

Understand user intention.

Return ONLY valid JSON.

Format:

{
"intent":"",
"goal":"",
"priority":1,
"answer":"",
"tasks":[]
}
"""



# =========================================================
# Brain Response
# =========================================================

@dataclass
class BrainResponse:

    success: bool = False

    raw: str = ""

    data: Dict[str,Any] = field(default_factory=dict)

    latency: float = 0.0

    retries: int = 0

    error: str = ""



# =========================================================
# Brain
# =========================================================

class Brain:


    def __init__(self):

        self.url = OLLAMA_URL

        self.model = MODEL

        self.lock = threading.RLock()

        self.history: List[BrainResponse] = []

        self.cache: Dict[str,BrainResponse] = {}



    # =====================================================
    # Ollama Check
    # =====================================================

    def ping(self):

        try:

            r = requests.get(
                "http://127.0.0.1:11434/api/tags",
                timeout=5
            )

            return r.status_code == 200


        except Exception:

            return False



    # =====================================================
    # Build Prompt
    # =====================================================

    def build_prompt(self,text:str):


        try:

            memory_data = memory.statistics()

        except Exception:

            memory_data = {}



        try:

            context_data = context.build_context()

        except Exception:

            context_data = {}



        return prompt_builder.build(

            user_text=text,

            memory_data=memory_data,

            context_data=context_data,

            skills=[],

            history=self.history[-3:]

        )



    # =====================================================
    # Send Request
    # =====================================================

    def _request(self,prompt:str):

        start=time.time()


        payload={

            "model":self.model,

            "prompt":prompt,

            "stream":False,

            "format":"json",

            "options": {
                "temperature": 0.3,
                "top_p": 0.9,
                "num_ctx": 2048,
                "num_predict": 256,
                "num_thread": 4
            }

        }


        try:


            response=requests.post(

                self.url,

                json=payload,

                timeout=REQUEST_TIMEOUT

            )


            response.raise_for_status()


            result=response.json()


            raw=result.get(
                "response",
                ""
            )


            data=json_parser.parse(raw)



            if data is None:

                return BrainResponse(

                    success=False,

                    raw=raw,

                    error="JSON ERROR",

                    latency=time.time()-start

                )



            brain_response=BrainResponse(

                success=True,

                raw=raw,

                data=data,

                latency=time.time()-start

            )


            self.history.append(brain_response)



            if len(self.history)>MAX_HISTORY:

                self.history.pop(0)



            return brain_response



        except Exception as e:


            return BrainResponse(

                success=False,

                error=str(e),

                latency=time.time()-start

            )



    # =====================================================
    # Ask
    # =====================================================

    def ask(self,text:str):


        if text in self.cache:

            return self.cache[text]



        prompt=self.build_prompt(text)


        last=None


        for attempt in range(MAX_RETRY):


            result=self._request(prompt)


            result.retries=attempt



            if result.success:


                self.cache[text]=result

                return result



            last=result



        return last



    # =====================================================
    # Status
    # =====================================================

    def status(self):

        return {

            "module":"Brain",

            "model":self.model,

            "history":len(self.history),

            "cache":len(self.cache),

            "ollama":self.ping(),

            "ready":True

        }



# =========================================================
# Singleton
# =========================================================

brain=Brain()