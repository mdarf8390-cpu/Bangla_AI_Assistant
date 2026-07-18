# voice/speech.py

import speech_recognition as sr


class SpeechRecognizer:

    def __init__(self):

        self.recognizer = sr.Recognizer()


    def listen(self):

        with sr.Microphone() as source:

            print("🎤 Listening...")

            self.recognizer.adjust_for_ambient_noise(
                source,
                duration=0.5
            )

            audio = self.recognizer.listen(
                source,
                phrase_time_limit=5
            )


        try:

            text = self.recognizer.recognize_google(
                audio,
                language="bn-BD"
            )

            return text.lower()


        except:

            return ""