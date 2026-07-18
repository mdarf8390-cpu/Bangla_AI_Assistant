from ai.brain import Brain
from core.executor import Executor


brain = Brain()
executor = Executor()


print("=" * 40)
print("      AYESHA Brain v2")
print("=" * 40)


while True:

    text = input("\nYou : ")

    if text.lower() == "exit":
        break


    plan = brain.think(text)

    print("\nPLAN:")
    print(plan)


    result = executor.execute(plan)

    print("\nRESULT:")
    print(result)