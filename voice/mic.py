# mic.py

import speech_recognition as sr

recognizer = sr.Recognizer()


def listen():

    with sr.Microphone() as source:

        audio = recognizer.listen(
            source,
            phrase_time_limit=5
        )

    try:

        text = recognizer.recognize_google(
            audio,
            language="bn-BD"
        )

        return text.lower()


    except:

        return ""



print("😴 Ayesha Sleep Mode")
print("Wake word: Ayesha")


active = False


while True:

    text = listen()


    if text:
        print("তুমি:", text)


    if not active:

        if "আয়েশা" in text or "ayesha" in text:

            active = True

            print("✨ Ayesha Active")


    else:

        if "অফ" in text or "off" in text:

            active = False

            print("😴 Ayesha Sleep Mode")


        else:

            print("Command:", text)