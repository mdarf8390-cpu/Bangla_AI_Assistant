from voice.dialogue import dialogue


dialogue.add_message(
    "user",
    "Hello AYESHA"
)

dialogue.add_message(
    "assistant",
    "Hello Arfat"
)


print(
    dialogue.statistics()
)


print()


for msg in dialogue:
    print(
        msg.role,
        ":",
        msg.content
    )