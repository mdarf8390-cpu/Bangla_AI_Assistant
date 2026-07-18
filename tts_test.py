from voice.tts import tts


print(
    tts.status()
)


tts.speak(
    "Hello Arfat, I am AYESHA"
)


tts.set_rate(
    180
)


tts.set_volume(
    0.8
)


print(
    tts.status()
)


tts.test()