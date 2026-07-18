import asyncio

from core.event_bus import event_bus


async def test_listener(event):

    print("EVENT RECEIVED:")
    print(event.name)
    print(event.payload)



async def main():

    event_bus.subscribe(
        "thinking_started",
        test_listener
    )


    await event_bus.emit(
        "thinking_started",
        {
            "message":
            "AYESHA is thinking"
        }
    )



if __name__ == "__main__":

    asyncio.run(main())