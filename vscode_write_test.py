from automation.engine import AutomationEngine


engine = AutomationEngine()


result = engine.execute({
    "action": "write",
    "app": "vscode",
    "text": "print('Hello AYESHA AI')"
})


print(result)