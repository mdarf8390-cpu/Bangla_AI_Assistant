from ai.normalizer import BanglaNormalizer
from ai.intent_ai import IntentAI

print("=" * 50)
print("Intent AI Test")
print("=" * 50)

normalizer = BanglaNormalizer()
intent = IntentAI()

while True:
    text = input("তুমি : ").strip()

    # Exit
    if text.lower() in ["exit", "quit", "q"]:
        print("\n✅ Intent AI Test Finished")
        break

    if not text:
        continue

    normalized = normalizer.normalize(text)

    print("Normalized :", normalized)

    try:
        result = intent.detect(normalized)
        print(result)
    except Exception as e:
        print("❌ Error :", e)

    print("-" * 50)