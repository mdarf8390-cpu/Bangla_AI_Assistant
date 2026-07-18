from automation.engine import AutomationEngine


engine = AutomationEngine()


print(
    engine.execute({
        "action": "open",
        "app": "google"
    })
)