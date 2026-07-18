from automation.engine import AutomationEngine


print("Starting Automation Engine...")

engine = AutomationEngine()


print("Testing YouTube Search...")

result = engine.execute({
    "action": "search",
    "app": "youtube",
    "query": "gta 6 trailer"
})


print("Result:")
print(result)