from core.command_parser import CommandParser

parser = CommandParser()

print("=" * 50)
print("Command Parser Test")
print("=" * 50)

test_commands = [
    "Open Chrome",
    "Open YouTube",
    "Play Music",
    "Close Chrome",
    "Shutdown PC",
    "Hello Ayesha"
]

passed = 0

for cmd in test_commands:
    try:
        result = parser.parse(cmd)
        print(f"\nInput : {cmd}")
        print(f"Output: {result}")
        passed += 1
    except Exception as e:
        print(f"\n❌ ERROR : {cmd}")
        print(e)

print("\n" + "=" * 50)
print(f"Passed : {passed}/{len(test_commands)}")

if passed == len(test_commands):
    print("✅ Parser Test Passed")
else:
    print("❌ Parser Test Failed")