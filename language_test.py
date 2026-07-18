from voice.language import language


tests = [
    "আমি AYESHA ব্যবহার করি",
    "Hello AYESHA",
    "আমি use করি AI"
]


for text in tests:

    print(
        text,
        "=>",
        language.analyze(text)
    )


print(
    language.status()
)