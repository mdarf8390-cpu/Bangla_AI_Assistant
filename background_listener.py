"""
Bangla AI Assistant - Background Voice Listener
সবসময় background এ শুনবে, যখন activate করবে তখন respond করবে
"""

import speech_recognition as sr
import threading
import time
import logging
from datetime import datetime
import asyncio

# লগিং সেটআপ
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BackgroundVoiceListener:
    """Background এ voice শোনার ক্লাস"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.listening = True
        self.activated = False
        self.activation_keywords = ['hey ayesha', 'ayesha', 'হে আয়েশা', 'আয়েশা']
        self.deactivation_keywords = ['bye', 'stop', 'থামো', 'বন্ধ কর']
        
        try:
            from ui.floating_avatar import FloatingCharacterWindow
            from character_launcher import start_floating_character
            self.character_available = True
        except:
            self.character_available = False
            logger.warning("Character module not available")
    
    def listen_for_activation(self):
        """Activation keywords শুনুন"""
        logger.info("🎤 Background listening শুরু হয়েছে...")
        
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                logger.info("✅ Microphone ready")
                
                while self.listening:
                    try:
                        logger.debug("👂 Listening...")
                        audio = self.recognizer.listen(source, timeout=2, phrase_time_limit=5)
                        
                        # Recognize speech
                        text = self.recognizer.recognize_google(audio, language='bn-IN')
                        text_lower = text.lower()
                        
                        logger.info(f"🗣️ শোনা হয়েছে: {text}")
                        
                        # Check for activation keywords
                        if any(keyword in text_lower for keyword in self.activation_keywords):
                            logger.info(f"🔊 ACTIVATED! Text: {text}")
                            self.activated = True
                            self.handle_activated_command(text)
                        
                        # Check for deactivation keywords
                        elif any(keyword in text_lower for keyword in self.deactivation_keywords):
                            if self.activated:
                                logger.info("🔇 Deactivated")
                                self.activated = False
                    
                    except sr.UnknownValueError:
                        logger.debug("❓ Could not understand audio")
                        pass
                    
                    except sr.RequestError as e:
                        logger.warning(f"⚠️ API error: {e}")
                        time.sleep(2)
                    
                    except sr.Timeout:
                        pass
                    
                    except Exception as e:
                        logger.error(f"❌ Error: {e}")
                        time.sleep(1)
        
        except Exception as e:
            logger.error(f"❌ Microphone error: {e}")
            logger.info("⚠️ Please check microphone connection")
    
    def handle_activated_command(self, text):
        """যখন activate হবে তখন কি করবে"""
        logger.info(f"🤖 Processing: {text}")
        
        try:
            # Import AI modules
            from ai.reasoning_engine import reasoning_engine
            from automation.action_executor import action_executor
            from core.memory_manager import memory
            
            # Process with AI
            decision = reasoning_engine.analyze(text)
            
            # Execute actions
            asyncio.run(action_executor.execute_tasks(decision.actions))
            
            # Get response
            response = decision.goal
            logger.info(f"💬 Response: {response}")
            
            # Speak response
            asyncio.run(self.speak(response))
            
        except Exception as e:
            logger.error(f"❌ Processing error: {e}")
    
    async def speak(self, text):
        """Text কে voice এ রূপান্তর করুন"""
        try:
            from edge_tts import Communicate
            import os
            
            logger.info(f"🔊 Speaking: {text}")
            
            comm = Communicate(text=text, voice="bn-BD-NabanitaNeural")
            await comm.save("response.mp3")
            
            # Play audio
            if os.name == 'nt':  # Windows
                os.system("start response.mp3")
            else:  # Mac/Linux
                os.system("afplay response.mp3")
            
            logger.info("✅ Spoken")
        
        except Exception as e:
            logger.error(f"❌ Speech error: {e}")
    
    def start(self):
        """Background listener শুরু করুন"""
        logger.info("=" * 60)
        logger.info("🎨 Bangla AI Assistant - Background Listener")
        logger.info("=" * 60)
        logger.info("")
        logger.info("📢 Activation Commands:")
        for cmd in self.activation_keywords:
            logger.info(f"   • {cmd}")
        logger.info("")
        logger.info("🔇 Deactivation Commands:")
        for cmd in self.deactivation_keywords:
            logger.info(f"   • {cmd}")
        logger.info("")
        logger.info("=" * 60)
        logger.info("")
        
        # Start listening in thread
        listener_thread = threading.Thread(
            target=self.listen_for_activation,
            daemon=True
        )
        listener_thread.start()
        
        # Keep alive
        try:
            while self.listening:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("\n👋 Stopping listener...")
            self.listening = False
    
    def stop(self):
        """Listener বন্ধ করুন"""
        self.listening = False
        logger.info("✅ Listener stopped")


def start_background_listener():
    """Background listener শুরু করুন"""
    listener = BackgroundVoiceListener()
    listener.start()


if __name__ == "__main__":
    try:
        start_background_listener()
    except Exception as e:
        logger.error(f"Error: {e}")
        input("Press Enter to exit...")
