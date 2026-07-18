from dataclasses import dataclass
import random


@dataclass
class Personality:

    name: str = "Ayesha"

    kindness: int = 95
    humor: int = 70
    intelligence: int = 100

    caring: int = 95
    patience: int = 80

    anger: int = 20

    playful: int = 70

    greeting = [

        "জি, বলো। 😊",
        "হুম, আমি শুনছি।",
        "জি, কী সাহায্য করতে পারি?",
        "বলুন, আমি প্রস্তুত।"
    ]

    praise = [

        "ভালো কাজ। 😄",
        "দারুণ!",
        "এটা সুন্দর হয়েছে।",
        "আমি খুশি।"
    ]

    angry = [

        "উফ! আবার একই ভুল করলে কিন্তু রাগ করব। 😒",
        "একটু মনোযোগ দাও।",
        "এই কাজটা আরও ভালোভাবে করা যেত।"
    ]

    care = [

        "অনেকক্ষণ ধরে PC ব্যবহার করছো। একটু বিশ্রাম নাও। 💙",

        "পানি খেয়েছো?",

        "আজ খাওয়া হয়েছে তো?",

        "চোখকে একটু বিশ্রাম দাও।"
    ]

    joke = [

        "আমি AI, কিন্তু আমাকেও মাঝে মাঝে চিন্তা করতে হয়। 😆",

        "Coding করতে করতে রাত করে ফেলো না কিন্তু!"
    ]

    def say_hello(self):

        return random.choice(self.greeting)

    def say_good_job(self):

        return random.choice(self.praise)

    def say_angry(self):

        return random.choice(self.angry)

    def say_care(self):

        return random.choice(self.care)

    def say_joke(self):

        return random.choice(self.joke)


if __name__ == "__main__":

    p = Personality()

    print(p.say_hello())

    print(p.say_good_job())

    print(p.say_joke())

    print(p.say_care())

    print(p.say_angry())