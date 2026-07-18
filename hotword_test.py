from voice.hotword import hotword


tests = [
    "hello",
    "AYESHA open browser",
    "hey ayesha"
]


for text in tests:

    print(
        hotword.process(text)
    )


print()

print(
    hotword.status()
)