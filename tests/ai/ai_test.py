import asyncio

from ai.reasoning_engine import ReasoningEngine


async def main():

    engine = ReasoningEngine()

    await engine.process_intent(
        "youtube open koro"
    )

    print("\n===================")
    print("Test Completed")
    print("===================")

    print("Current State :", engine._state)

    print("History Events :", len(engine.history))

    for event in engine.history:

        print(
            event.state.name,
            event.payload
        )


if __name__ == "__main__":
    asyncio.run(main())