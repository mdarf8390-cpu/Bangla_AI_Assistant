from core.memory import memory

print(memory.status())

memory.remember(
    "assistant",
    "AYESHA"
)

memory.add_conversation(
    "user",
    "Hello"
)

memory.add_goal(
    "Finish AI"
)

print(memory.recall("assistant"))

print(memory.statistics())