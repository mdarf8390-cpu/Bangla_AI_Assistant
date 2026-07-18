import speech_recognition as sr

recognizer = sr.Recognizer()

active = False

print("😴 Ayesha Sleep Mode")


while True:

    with sr.Microphone() as source:

        audio = recognizer.listen(
            source,
            phrase_time_limit=5
        )

    try:

        text = recognizer.recognize_google(
            audio,
            language="bn-BD"
        ).lower()


        if "আয়েশা" in text or "ayesha" in text:

            active = True
            print("✨ Ayesha Active")


        elif active:

            if "অফ" in text or "off" in text:

                active = False
                print("😴 Ayesha Sleep Mode")

            else:
                # এখানে এখন কিছু print হবে না
                pass


    except:
        pass