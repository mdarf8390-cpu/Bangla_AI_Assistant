from automation.engine import AutomationEngine


print("Starting Automation Engine...")

engine = AutomationEngine()


print("Testing YouTube Open...")

result = engine.execute({
    "action": "open",
    "app": "youtube"
})


print("Result:")
print(result)