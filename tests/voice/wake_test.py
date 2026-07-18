from voice.speech import SpeechRecognizer
from voice.wake_word import WakeWordDetector


speech = SpeechRecognizer()
wake = WakeWordDetector()


print("🎤 Say 'Ayesha' to activate")


while True:

    text = speech.listen()


    if text:
        print("You:", text)


        result = wake.check(text)


        if result:
            print("Status:", result)


        print("Active:", wake.is_active())