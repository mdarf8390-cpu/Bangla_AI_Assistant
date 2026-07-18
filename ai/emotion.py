from enum import Enum


class Emotion(Enum):
    HAPPY = "happy"
    NORMAL = "normal"
    THINKING = "thinking"
    ANGRY = "angry"
    SAD = "sad"
    SLEEP = "sleep"
    EXCITED = "excited"


class EmotionManager:

    def __init__(self):
        self.current = Emotion.NORMAL

    def set(self, emotion: Emotion):
        self.current = emotion

    def get(self):
        return self.current

    def avatar_expression(self):
        return {
            Emotion.NORMAL: "normal",
            Emotion.HAPPY: "happy",
            Emotion.THINKING: "thinking",
            Emotion.ANGRY: "angry",
            Emotion.SAD: "sad",
            Emotion.SLEEP: "sleep",
            Emotion.EXCITED: "happy",
        }[self.current]

    def voice_style(self):
        return {
            Emotion.NORMAL: "normal",
            Emotion.HAPPY: "cheerful",
            Emotion.THINKING: "slow",
            Emotion.ANGRY: "firm",
            Emotion.SAD: "soft",
            Emotion.SLEEP: "quiet",
            Emotion.EXCITED: "energetic",
        }[self.current]


if __name__ == "__main__":

    emotion = EmotionManager()

    print("Current:", emotion.get().value)

    emotion.set(Emotion.HAPPY)

    print("Now:", emotion.get().value)
    print("Avatar:", emotion.avatar_expression())
    print("Voice:", emotion.voice_style())