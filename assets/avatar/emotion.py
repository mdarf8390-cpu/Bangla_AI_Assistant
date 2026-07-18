# emotion.py

import random


class AyeshaEmotion:


    def __init__(self):

        self.current_mood = "normal"



    def set_mood(self, mood):

        self.current_mood = mood



    def get_mood(self):

        return self.current_mood



    def analyze_message(self, message):

        msg = message.lower()


        # Happy trigger
        if any(word in msg for word in [
            "ভালো",
            "ধন্যবাদ",
            "thank",
            "nice",
            "great"
        ]):

            self.current_mood = "happy"



        # Sad/Caring trigger
        elif any(word in msg for word in [
            "খারাপ",
            "মন খারাপ",
            "দুঃখ",
            "sad"
        ]):

            self.current_mood = "caring"



        # Playful angry trigger
        elif any(word in msg for word in [
            "ভুলে গেছি",
            "অনেক দেরি",
            "আবার",
        ]):

            self.current_mood = "playful_angry"



        else:

            self.current_mood = "normal"



        return self.current_mood




def emotion_reply(mood):


    replies = {


        "happy":
        [
            "এটা শুনে আমার ভালো লাগলো 😊",
            "দারুণ! 😄"
        ],


        "caring":
        [
            "সব ঠিক হয়ে যাবে, আমি আছি 💙",
            "নিজের যত্ন নিও 😊"
        ],


        "playful_angry":
        [
            "আবার একই কাজ করলে কিন্তু আমি একটু অভিমান করবো 😤😄",
            "আমাকে ভুলে গেলে নাকি? 😒"
        ],


        "normal":
        [
            "বুঝতে পারছি 😊"
        ]

    }


    return random.choice(
        replies.get(mood, replies["normal"])
    )