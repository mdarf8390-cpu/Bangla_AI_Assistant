from automation.engine import AutomationEngine


print("Starting Automation Engine...")

engine = AutomationEngine()


print("Opening Notepad...")

result = engine.execute({
    "action": "open",
    "app": "notepad"
})


print("Result:")
print(result)