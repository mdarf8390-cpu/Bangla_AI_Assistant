from voice.microphone import microphone


print(
    microphone.status()
)


microphone.start()


microphone.add_sample(
    0.55
)


microphone.add_sample(
    0.23
)


print(
    microphone.get_buffer()
)


print(
    microphone.status()
)


microphone.clear_buffer()


microphone.stop()


print(
    microphone.status()
)