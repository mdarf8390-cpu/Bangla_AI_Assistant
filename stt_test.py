from voice.stt import stt


print(
    stt.status()
)


stt.start()


print(
    "Recognized:",
    stt.recognize()
)


stt.set_language(
    "bn"
)


print(
    stt.status()
)


stt.stop()


print(
    stt.status()
)