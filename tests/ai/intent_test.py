from core.intent import IntentDetector

detector = IntentDetector()

while True:

    text = input("You : ")

    if text == "exit":
        break

    intent = detector.detect(text)

    print("\nIntent =", intent)