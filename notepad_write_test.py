from automation.engine import AutomationEngine


engine = AutomationEngine()


result = engine.execute({
    "action": "write",
    "app": "notepad",
    "text": "Hello, I am AYESHA AI"
})


print(result)