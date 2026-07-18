from automation.engine import AutomationEngine

engine = AutomationEngine()

engine.execute({
    "action": "search",
    "app": "youtube",
    "query": "GTA 6 Trailer"
})

print("Engine Test Complete")