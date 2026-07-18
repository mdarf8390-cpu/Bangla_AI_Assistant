from voice.noise import noise


samples = [
    0.01,
    0.02,
    0.03,
    0.04
]


print(
    noise.analyze(samples)
)


print(
    noise.status()
)


print(
    "Voice:",
    noise.has_voice(samples)
)