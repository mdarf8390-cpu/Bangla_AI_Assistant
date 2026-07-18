from automation.engine import AutomationEngine


engine = AutomationEngine()


result = engine.execute({
    "action": "open",
    "app": "telegram"
})


print(result)