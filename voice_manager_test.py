from core.voice_manager import voice_manager


print("=" * 50)
print("AYESHA Voice Manager Test")
print("=" * 50)

print("\nInitial Status:\n")
print(
    voice_manager.status()
)

print("\nStarting Voice Manager...\n")

voice_manager.start()

print(
    voice_manager.status()
)

print("\nProcessing Text...\n")

result = voice_manager.process_text(
    "AYESHA open chrome"
)

print(result)

print("\nSpeaking...\n")

voice_manager.speak(
    "Hello Arfat, I am AYESHA."
)

print("\nListening Once...\n")

text = voice_manager.listen_once()

print("Recognized :", text)

print("\nStopping...\n")

voice_manager.stop()

print(
    voice_manager.status()
)

print("\nTest Finished.")