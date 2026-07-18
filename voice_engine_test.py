from voice.engine import engine


print(
    engine.status()
)


engine.start()


print(
    engine.process_text(
        "AYESHA open chrome"
    )
)


print(
    engine.get_last_text()
)


engine.stop()


print(
    engine.status()
)