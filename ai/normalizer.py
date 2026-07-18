# ai/normalizer.py

import re
from difflib import get_close_matches


class BanglaNormalizer:

    def __init__(self):

        self.word_map = {

            # Apps
            "ইউটিউব": "youtube",
            "ইউটুব": "youtube",
            "ইউটিপ": "youtube",
            "ইউটুবে": "youtube",

            "গুগল": "google",
            "গুগুল": "google",
            "গুগলে": "google",

            "ক্রোম": "chrome",

            "ভিএসকোড": "vscode",
            "ভিএস কোড": "vscode",

            "নোটপ্যাড": "notepad",

            "টেলিগ্রাম": "telegram",

            "হোয়াটসঅ্যাপ": "whatsapp",
            "হোয়াটসেপ": "whatsapp",

            "ডিসকর্ড": "discord",

            "স্পটিফাই": "spotify",

            # Actions
            "খুলো": "open",
            "চালু করো": "open",
            "ওপেন": "open",

            "বন্ধ করো": "close",
            "বন্ধ": "close",

            "সার্চ": "search",
            "খুঁজো": "search",
            "খুঁজে দাও": "search",

            "লিখো": "write",
            "টাইপ করো": "write",

            "চালাও": "play",
            "প্লে": "play"
        }

        self.app_names = [
            "youtube",
            "google",
            "chrome",
            "vscode",
            "notepad",
            "telegram",
            "discord",
            "spotify",
            "whatsapp"
        ]


    def clean(self, text: str) -> str:

        text = text.lower()

        text = re.sub(r"[^\w\s\u0980-\u09FF]", " ", text)

        text = re.sub(r"\s+", " ", text)

        return text.strip()


    def replace_words(self, text: str) -> str:

        for k, v in self.word_map.items():

            text = text.replace(k.lower(), v)

        return text


    def fuzzy_apps(self, text: str) -> str:

        words = text.split()

        output = []

        for word in words:

            match = get_close_matches(
                word,
                self.app_names,
                n=1,
                cutoff=0.75
            )

            if match:

                output.append(match[0])

            else:

                output.append(word)

        return " ".join(output)


    def normalize(self, text: str) -> str:

        if not text:

            return ""

        text = self.clean(text)

        text = self.replace_words(text)

        text = self.fuzzy_apps(text)

        return text