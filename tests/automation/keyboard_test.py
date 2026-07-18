import time

from services.keyboard import KeyboardService


keyboard = KeyboardService()


print("Switch to Notepad...")

time.sleep(3)


keyboard.type(

    text="Hello from AYESHA!",

    target="notepad"

)

keyboard.enter()

keyboard.type(

    text="This text was written automatically."
)