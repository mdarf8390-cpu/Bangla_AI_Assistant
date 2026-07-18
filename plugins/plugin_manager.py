from typing import Dict

from plugins.qwen_plugin import QwenPlugin


class PluginManager:

    def __init__(self):

        self.plugins: Dict[str, object] = {}

        # Register all plugins
        self.register("qwen", QwenPlugin())

        # Default plugin
        self.current = self.plugins["qwen"]

    def register(self, name: str, plugin):

        self.plugins[name] = plugin

    def use(self, name: str):

        if name not in self.plugins:
            raise ValueError(f"{name} plugin not found.")

        self.current = self.plugins[name]

    def ask(self, prompt: str):

        if self.current is None:
            return "No AI plugin selected."

        return self.current.generate(prompt)

    def available(self):

        return list(self.plugins.keys())