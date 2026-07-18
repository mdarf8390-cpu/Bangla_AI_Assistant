from __future__ import annotations

import logging
import webbrowser
from typing import Callable, Any

from automation.browser import BrowserAutomation


class ActionExecutor:

    def __init__(self):

        self.logger = logging.getLogger("ActionExecutor")

        self.browser = BrowserAutomation()

        self.registry: dict[str, Callable] = {
            "speak": self._speak,
            "web": self._open_web,
            "open_browser": self._open_browser,
            "open_youtube": self._open_youtube,
            "open_google": self._open_google,
            "system": self._system_cmd
        }


    def execute(self, action_name: str, params: Any = None):

        if action_name in self.registry:
            return self.registry[action_name](params)

        self.logger.error(
            f"Action '{action_name}' not found in registry."
        )


    def _speak(self, text: str):

        print(f"AI Speaking: {text}")


    def _open_web(self, url: str):

        print(f"Opening web: {url}")
        webbrowser.open(url)


    def _open_browser(self, url: str):

        print(f"Opening browser: {url}")
        webbrowser.open(url)


    def _open_youtube(self, query: str):

        print(f"Opening YouTube: {query}")
        self.browser.open_youtube(query)


    def _open_google(self, query: str):

        print(f"Searching Google: {query}")
        self.browser.open_google(query)


    def _system_cmd(self, cmd: str):

        print(f"Running system cmd: {cmd}")


action_executor = ActionExecutor()