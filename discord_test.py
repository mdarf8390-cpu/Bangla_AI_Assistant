from automation.engine import AutomationEngine


engine = AutomationEngine()


result = engine.execute({
    "action": "open",
    "app": "discord"
})


print(result)