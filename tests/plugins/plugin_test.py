from plugins.plugin_manager import PluginManager
from plugins.qwen_plugin import QwenPlugin

manager = PluginManager()

manager.register("qwen", QwenPlugin())

manager.use("qwen")

print("AYESHA Ready! Type 'exit' to quit.\n")

while True:
    prompt = input("You: ")

    if prompt.lower() == "exit":
        break

    answer = manager.ask(prompt)

    print(f"\nAYESHA: {answer}\n")