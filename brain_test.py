from core.brain import brain
import time

print("=" * 50)
print("Brain Test")
print("=" * 50)

try:
    print("1. Ping Test...")
    print("Ping:", brain.ping())

    print("\n2. Calling brain.ask()...")

    start = time.time()

    response = brain.ask("Open Chrome and search Python AI")

    end = time.time()

    print("\n3. Response received")
    print("Success :", getattr(response, "success", None))
    print("Data    :", getattr(response, "data", None))
    print("Latency :", getattr(response, "latency", end - start))
    print("Error   :", getattr(response, "error", None))

    print("\n✅ Brain Test Passed")

except Exception as e:
    print("\n❌ Brain Test Failed")
    print(type(e).__name__)
    print(e)