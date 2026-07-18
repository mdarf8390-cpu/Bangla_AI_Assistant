from plugins.plugin_manager import PluginManager
from plugins.qwen_plugin import QwenPlugin


manager = PluginManager()

manager.register("qwen", QwenPlugin())

manager.use("qwen")

while True:

    prompt = input("You : ")

    if prompt.lower() == "exit":
        break

    answer = manager.ask(prompt)

    print("\nAYESHA :", answer)