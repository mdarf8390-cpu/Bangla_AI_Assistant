"""
AYESHA AI - Voice Manager
"""

from __future__ import annotations
import logging

from voice.microphone import microphone
from voice.noise import noise
from voice.language import language
from voice.hotword import hotword
from voice.stt import stt
from voice.tts import tts

logger = logging.getLogger("AYESHA_CORE")


class VoiceManager:

    def __init__(self):
        self.running = False
        logger.info("Voice Manager Initialized")

    def start(self) -> bool:
        if self.running:
            return True
        microphone.start()
        stt.start()
        self.running = True
        logger.info("Voice Manager Started")
        return True

    def stop(self) -> bool:
        if not self.running:
            return True
        stt.stop()
        microphone.stop()
        hotword.deactivate()
        self.running = False
        logger.info("Voice Manager Stopped")
        return True

    def process_text(self, text: str) -> dict:
        lang = language.analyze(text)
        wake = hotword.process(text)
        return {
            "text": text,
            "language": lang,
            "hotword": wake,
        }

    def speak(self, text: str) -> bool:
        return tts.speak(text)

    def listen_once(self) -> str:
        if not self.running:
            return ""
        return stt.recognize()

    def status(self) -> dict:
        return {
            "module": "VoiceManager",
            "running": self.running,
            "microphone": microphone.status(),
            "stt": stt.status(),
            "hotword": hotword.status(),
            "language": language.status(),
            "tts": tts.status(),
            "ready": True,
        }


voice_manager = VoiceManager()
