import asyncio

from core.reasoning_engine import reasoning_engine
from core.planner import Planner
from core.executor import Executor


planner = Planner()
executor = Executor()


async def main():

    command = input("You: ")

    print("👀 OBSERVING")
    print(command)

    decision = reasoning_engine.prepare(command)

    print("🧠 ANALYZING")

    print(decision)

    print("⚙ EXECUTING")

    plan = planner.create_plan(
        decision.actions[0]
    )

    result = executor.execute(plan)

    print("RESULT:")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())