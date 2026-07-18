from voice.speech import SpeechRecognizer


speech = SpeechRecognizer()


while True:

    text = speech.listen()

    if text:
        print("You:", text)