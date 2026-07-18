from core.reasoning_engine import reasoning_engine

decision = reasoning_engine.prepare(
    "Open YouTube and search Python AI"
)

print(reasoning_engine.explain(decision))

print()

print(reasoning_engine.status())