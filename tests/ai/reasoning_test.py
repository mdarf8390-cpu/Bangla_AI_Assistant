from ai.reasoning_engine import ReasoningEngine

brain = ReasoningEngine()

brain.new_decision("ইউটিউব খোলো")

intent = {

    "action":"open",

    "app":"youtube"

}

result = brain.analyze(intent)

print(result)

print()

print(brain.explain_decision())