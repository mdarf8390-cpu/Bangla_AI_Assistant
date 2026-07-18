import customtkinter as ctk
import threading
import asyncio
import time
import os
import logging
from edge_tts import Communicate

# প্রয়োজনীয় মডিউলসমূহ
from ai.reasoning_engine import reasoning_engine
from automation.action_executor import action_executor
from core.memory_manager import memory

# Avatar modules
try:
    from ui.floating_avatar import FloatingCharacterWindow, Emotion
    FLOATING_AVATAR_AVAILABLE = True
except ImportError:
    FLOATING_AVATAR_AVAILABLE = False
    logging.warning("Floating avatar module not available")

# Character Memory
try:
    from ai.character_memory import get_memory, Emotion as CharacterEmotion
    CHARACTER_MEMORY_AVAILABLE = True
except ImportError:
    CHARACTER_MEMORY_AVAILABLE = False
    logging.warning("Character memory module not available")

# Feature Request System
try:
    from ai.feature_requests import get_feature_system
    FEATURE_SYSTEM_AVAILABLE = True
except ImportError:
    FEATURE_SYSTEM_AVAILABLE = False
    logging.warning("Feature request system not available")

# Media Detection Module
try:
    import psutil
    import subprocess
    MEDIA_DETECTION_AVAILABLE = True
except ImportError:
    MEDIA_DETECTION_AVAILABLE = False
    logging.warning("Media detection module not available")

# লগিং কনফিগারেশন
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MediaDetector:
    """মিডিয়া প্লেয়ার এবং সাউন্ড ডিটেক্ট করার ক্লাস"""
    
    def __init__(self):
        self.is_playing = False
        self.current_media = None
        self.media_players = [
            'vlc.exe', 'wmplayer.exe', 'chrome.exe', 'firefox.exe',
            'spotify.exe', 'mpv.exe', 'mpc-hc.exe', 'potplayer.exe',
            'mpc-be.exe', 'foobar2000.exe', 'winamp.exe', 'davplayer.exe'
        ]
    
    def check_audio_output(self):
        """Windows এ অডিও আউটপুট ডিটেক্ট করা"""
        try:
            if not MEDIA_DETECTION_AVAILABLE:
                return False
            
            # Windows এ প্রসেস চেক করা
            for proc in psutil.process_iter(['name']):
                try:
                    if proc.info['name'].lower() in self.media_players:
                        return True
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            return False
        except Exception as e:
            logger.error(f"Audio detection error: {str(e)}")
            return False
    
    def get_current_media_info(self):
        """বর্তমান মিডিয়া ইনফরমেশন পান"""
        try:
            if not MEDIA_DETECTION_AVAILABLE:
                return None
            
            for proc in psutil.process_iter(['name']):
                try:
                    process_name = proc.info['name'].lower()
                    if process_name in self.media_players:
                        return {
                            'player': process_name.replace('.exe', '').upper(),
                            'status': 'Playing',
                            'pid': proc.pid
                        }
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            return None
        except Exception as e:
            logger.error(f"Media info error: {str(e)}")
            return None
    
    def pause_media(self):
        """মিডিয়া পজ করার চেষ্টা করা (Spacebar simulation)"""
        try:
            if MEDIA_DETECTION_AVAILABLE:
                # Windows এ Spacebar প্রেস করা (Play/Pause)
                import pyautogui
                pyautogui.press('space')
                return True
        except Exception as e:
            logger.error(f"Pause media error: {str(e)}")
        
        return False
    
    def resume_media(self):
        """মিডিয়া রিজিউম করার চেষ্টা করা"""
        try:
            if MEDIA_DETECTION_AVAILABLE:
                import pyautogui
                pyautogui.press('space')
                return True
        except Exception as e:
            logger.error(f"Resume media error: {str(e)}")
        
        return False


class AyeshaAI_Professional:
    def __init__(self):
        self.app = ctk.CTk()
        self.app.title("Ayesha AI - Autonomous System with Memory")
        self.app.geometry("1300x700")
        
        # Media Detector Initialize করা
        self.media_detector = MediaDetector()
        self.media_was_playing = False
        
        # Character Memory
        self.char_memory = None
        if CHARACTER_MEMORY_AVAILABLE:
            try:
                self.char_memory = get_memory()
                logger.info("Character memory initialized")
            except Exception as e:
                logger.error(f"Failed to initialize character memory: {str(e)}")
        
        # Feature Request System
        self.feature_system = None
        if FEATURE_SYSTEM_AVAILABLE:
            try:
                self.feature_system = get_feature_system()
                logger.info("Feature request system initialized")
            except Exception as e:
                logger.error(f"Failed to initialize feature system: {str(e)}")
        
        # Floating Avatar
        self.avatar_window = None
        if FLOATING_AVATAR_AVAILABLE:
            try:
                self.avatar_window = FloatingCharacterWindow()
                logger.info("Floating avatar initialized")
                # Start avatar in separate thread
                avatar_thread = threading.Thread(target=self.avatar_window.show, daemon=True)
                avatar_thread.start()
            except Exception as e:
                logger.error(f"Failed to initialize floating avatar: {str(e)}")
                self.avatar_window = None
        
        # Chat UI Setup (Right side)
        chat_frame = ctk.CTkFrame(self.app)
        chat_frame.pack(side="right", padx=20, pady=20, fill="both", expand=True)
        
        # Chat title
        title_label = ctk.CTkLabel(
            chat_frame,
            text="💬 Chat with Ayesha AI",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=10)
        
        # Active user info
        self.user_info_label = ctk.CTkLabel(
            chat_frame,
            text="👤 No active user",
            font=("Arial", 12),
            text_color="orange"
        )
        self.user_info_label.pack(pady=5)
        
        # Media Status Label
        self.media_status_label = ctk.CTkLabel(
            chat_frame,
            text="🔇 No media playing",
            font=("Arial", 10),
            text_color="gray"
        )
        self.media_status_label.pack(pady=3)
        
        # Chat box
        self.chat_box = ctk.CTkTextbox(
            chat_frame,
            width=600,
            height=400,
            font=("Arial", 14),
            text_color="white"
        )
        self.chat_box.pack(pady=10, fill="both", expand=True)
        
        # Input frame
        input_frame = ctk.CTkFrame(chat_frame)
        input_frame.pack(pady=10, fill="x")
        
        # Input entry
        self.entry = ctk.CTkEntry(
            input_frame,
            width=500,
            height=40,
            placeholder_text="আপনার কমান্ড লিখুন...",
            font=("Arial", 12)
        )
        self.entry.pack(side="left", padx=5, fill="x", expand=True)
        self.entry.bind("<Return>", lambda e: self.handle_input())
        
        # Send button
        self.send_btn = ctk.CTkButton(
            input_frame,
            text="📤 Send",
            command=self.handle_input,
            width=100,
            height=40
        )
        self.send_btn.pack(side="right", padx=5)
        
        # Status label
        self.status_label = ctk.CTkLabel(
            chat_frame,
            text="✅ Ready",
            font=("Arial", 10),
            text_color="green"
        )
        self.status_label.pack(pady=5)
        
        # Help label
        help_text = """📋 Commands:
activate [name] - নতুন user শুরু করো
deactivate - session শেষ করো
ভুল [desc] - ভুল correct করো
ঠিক আছে - সঠিক confirm করো
তথ্য [name] - user info দেখো
feature [desc] - নতুন feature add কর
status [ID] - feature status দেখো
তালিকা - সব feature দেখো
পরিসংখ্যান - feature stats দেখো
মিডিয়া - মিডিয়া স্ট্যাটাস চেক করো"""
        
        help_label = ctk.CTkLabel(
            chat_frame,
            text=help_text,
            font=("Arial", 9),
            text_color="gray",
            justify="left"
        )
        help_label.pack(pady=5)
        
        # Media Monitor Start করা
        threading.Thread(target=self._media_monitor, daemon=True).start()
        
        # Autonomous Monitor Start
        threading.Thread(target=self._autonomous_monitor, daemon=True).start()

    def _media_monitor(self):
        """সঙ্গ বা মুভি চলছে কিনা মনিটর করা"""
        while True:
            try:
                media_playing = self.media_detector.check_audio_output()
                
                if media_playing and not self.media_was_playing:
                    # মিডিয়া শুরু হয়েছে
                    media_info = self.media_detector.get_current_media_info()
                    if media_info:
                        message = f"🎵 {media_info['player']} চলছে!"
                        self.chat_box.insert("end", f"📢 সিস্টেম: {message}\n\n")
                        self.chat_box.see("end")
                        self.media_status_label.configure(
                            text=f"🎵 {media_info['player']} চলছে",
                            text_color="orange"
                        )
                    self.media_was_playing = True
                
                elif not media_playing and self.media_was_playing:
                    # মিডিয়া থেমে গেছে
                    self.media_status_label.configure(
                        text="🔇 No media playing",
                        text_color="gray"
                    )
                    self.media_was_playing = False
                
                time.sleep(2)  # প্রতি ২ সেকেন্ডে চেক করা
            except Exception as e:
                logger.error(f"Media monitor error: {str(e)}")
                time.sleep(5)

    def _autonomous_monitor(self):
        """Monitor system autonomously"""
        while True:
            time.sleep(300)

    def _update_avatar_emotion(self, emotion):
        """Update avatar emotion safely"""
        if self.avatar_window:
            try:
                from ui.floating_avatar import Emotion as AvatarEmotion
                self.avatar_window.set_emotion(emotion)
            except Exception as e:
                logger.error(f"Error updating avatar emotion: {str(e)}")

    def _update_user_info(self):
        """Update user info display"""
        if self.char_memory and self.char_memory.is_active:
            user = self.char_memory.active_user
            session_info = self.char_memory.get_session_info()
            duration_str = session_info.get("session_duration_formatted", "0 মিনিট")
            self.user_info_label.configure(
                text=f"👤 Active: {user} | ⏱️ {duration_str}",
                text_color="green"
            )
        else:
            self.user_info_label.configure(
                text="👤 No active user",
                text_color="orange"
            )

    def _handle_activate_command(self, user_name: str) -> str:
        """Handle activate command"""
        if not self.char_memory:
            return "❌ Character memory not available"
        
        response = self.char_memory.activate_user(user_name)
        self._update_avatar_emotion("excited")
        self._update_user_info()
        return response

    def _handle_deactivate_command(self) -> str:
        """Handle deactivate command"""
        if not self.char_memory:
            return "❌ Character memory not available"
        
        response = self.char_memory.deactivate_user()
        self._update_avatar_emotion("neutral")
        self._update_user_info()
        return response

    def _handle_mistake_correction(self, mistake_text: str) -> str:
        """Handle mistake correction"""
        if not self.char_memory:
            return "❌ Character memory not available"
        
        if not self.char_memory.is_active:
            return "⚠️ কোন active user নেই। প্রথমে 'activate [name]' বলো।"
        
        response = self.char_memory.correct_mistake(
            mistake_text,
            f"এটা ঠিক করতে হবে",
            category="learning"
        )
        self._update_avatar_emotion("thinking")
        return response

    def _handle_positive_reinforcement(self) -> str:
        """Handle positive reinforcement"""
        if not self.char_memory:
            return "❌ Character memory not available"
        
        if not self.char_memory.is_active:
            return "⚠️ কোন active user নেই। প্রথমে 'activate [name]' বলো।"
        
        response = self.char_memory.reinforce_correct_behavior(
            "User সঠিক confirm করেছে",
            category="positive"
        )
        self._update_avatar_emotion("happy")
        return response

    def _handle_user_info_command(self, user_name: str = None) -> str:
        """Handle user info command"""
        if not self.char_memory:
            return "❌ Character memory not available"
        
        if user_name is None:
            user_name = self.char_memory.active_user
        
        if not user_name:
            return "⚠️ কোন active user নেই। 'activate [name]' বলো অথবা 'তথ্য [name]' বলো।"
        
        info = self.char_memory.get_user_info(user_name)
        if not info:
            return f"❌ {user_name} সম্পর্কে কোন তথ্য নেই।"
        
        response = f"""📊 {user_name} এর তথ্য:
👤 নাম: {info['name']}
📅 প্রথম সাক্ষাৎ: {info['first_met'][:10]}
🕐 শেষ যোগাযোগ: {info['last_interaction'][:10]}
💬 মোট কথোপকথন: {info['interaction_count']}
📈 মোট সেশন: {info['total_sessions']}
⏱️ মোট সময়: {info['total_active_time_formatted']}"""
        
        return response

    def _handle_feature_request(self, description: str) -> str:
        """Handle feature request"""
        if not self.feature_system:
            return "❌ Feature system not available"
        
        if not self.char_memory or not self.char_memory.is_active:
            return "⚠️ কোন active user নেই। প্রথমে 'activate [name]' বলো।"
        
        requested_by = self.char_memory.active_user
        success, response, request_id = self.feature_system.add_feature_request(
            description,
            requested_by,
            priority="medium"
        )
        
        self._update_avatar_emotion("excited")
        return response

    def _handle_feature_status(self, request_id: str) -> str:
        """Handle feature status check"""
        if not self.feature_system:
            return "❌ Feature system not available"
        
        return self.feature_system.get_request_status(request_id)

    def _handle_list_features(self) -> str:
        """Handle list features command"""
        if not self.feature_system:
            return "❌ Feature system not available"
        
        return self.feature_system.list_all_requests()

    def _handle_feature_statistics(self) -> str:
        """Handle feature statistics"""
        if not self.feature_system:
            return "❌ Feature system not available"
        
        return self.feature_system.get_statistics()

    def _handle_media_status(self) -> str:
        """মিডিয়া স্ট্যাটাস হ্যান্ডেল করা"""
        media_info = self.media_detector.get_current_media_info()
        if media_info:
            return f"🎵 {media_info['player']} চলছে! প্লেয়ার: {media_info['status']}"
        else:
            return "🔇 কোন মিডিয়া এখন চলছে না।"

    async def speak(self, text):
        """Speak the text using edge-tts"""
        try:
            self.status_label.configure(text="🔊 Speaking...", text_color="orange")
            
            # Check if media is playing and pause it
            if self.media_detector.check_audio_output():
                self.media_detector.pause_media()
                time.sleep(0.5)  # Wait for media to pause
            
            # Update avatar - happy
            self._update_avatar_emotion("happy")
            
            comm = Communicate(text=text, voice="bn-BD-NabanitaNeural")
            await comm.save("response.mp3")
            
            # Play audio based on OS
            if os.name == 'nt':  # Windows
                os.system("start response.mp3")
            else:  # Linux/Mac
                os.system("afplay response.mp3")
            
            self.status_label.configure(text="✅ Ready", text_color="green")
        except Exception as e:
            logger.error(f"Voice Error: {e}")
            self.status_label.configure(text="❌ Voice Error", text_color="red")
            self._update_avatar_emotion("confused")

    async def run_ai(self, user_text):
        """Process user input and generate AI response"""
        try:
            # ১. Update status
            self.status_label.configure(text="🤔 Processing...", text_color="blue")
            
            # २. Update avatar - thinking
            self._update_avatar_emotion("thinking")
            
            # Check for special commands
            if user_text.lower().startswith("activate "):
                user_name = user_text[9:].strip()
                response = self._handle_activate_command(user_name)
                self.chat_box.insert("end", f"🤖 Ayesha: {response}\n\n")
                self.chat_box.see("end")
                await self.speak(response)
                self.status_label.configure(text="✅ Ready", text_color="green")
                return
            
            elif user_text.lower() == "deactivate":
                response = self._handle_deactivate_command()
                self.chat_box.insert("end", f"🤖 Ayesha: {response}\n\n")
                self.chat_box.see("end")
                await self.speak(response)
                self.status_label.configure(text="✅ Ready", text_color="green")
                return
            
            elif user_text.lower().startswith("ভুল "):
                mistake = user_text[4:].strip()
                response = self._handle_mistake_correction(mistake)
                self.chat_box.insert("end", f"🤖 Ayesha: {response}\n\n")
                self.chat_box.see("end")
                await self.speak(response)
                self.status_label.configure(text="✅ Ready", text_color="green")
                return
            
            elif user_text.lower() == "ঠিক আছে":
                response = self._handle_positive_reinforcement()
                self.chat_box.insert("end", f"🤖 Ayesha: {response}\n\n")
                self.chat_box.see("end")
                await self.speak(response)
                self.status_label.configure(text="✅ Ready", text_color="green")
                return
            
            elif user_text.lower().startswith("তথ্য"):
                parts = user_text.split()
                user_name = parts[1] if len(parts) > 1 else None
                response = self._handle_user_info_command(user_name)
                self.chat_box.insert("end", f"🤖 Ayesha: {response}\n\n")
                self.chat_box.see("end")
                self.status_label.configure(text="✅ Ready", text_color="green")
                return
            
            elif user_text.lower().startswith("feature "):
                description = user_text[8:].strip()
                response = self._handle_feature_request(description)
                self.chat_box.insert("end", f"🤖 Ayesha: {response}\n\n")
                self.chat_box.see("end")
                await self.speak(response)
                self.status_label.configure(text="✅ Ready", text_color="green")
                return
            
            elif user_text.lower().startswith("status "):
                request_id = user_text[7:].strip()
                response = self._handle_feature_status(request_id)
                self.chat_box.insert("end", f"🤖 Ayesha: {response}\n\n")
                self.chat_box.see("end")
                self.status_label.configure(text="✅ Ready", text_color="green")
                return
            
            elif user_text.lower() == "তালিকা":
                response = self._handle_list_features()
                self.chat_box.insert("end", f"🤖 Ayesha: {response}\n\n")
                self.chat_box.see("end")
                self.status_label.configure(text="✅ Ready", text_color="green")
                return
            
            elif user_text.lower() == "পরিসংখ্যান":
                response = self._handle_feature_statistics()
                self.chat_box.insert("end", f"🤖 Ayesha: {response}\n\n")
                self.chat_box.see("end")
                self.status_label.configure(text="✅ Ready", text_color="green")
                return
            
            elif user_text.lower() == "মিডিয়া":
                response = self._handle_media_status()
                self.chat_box.insert("end", f"🤖 Ayesha: {response}\n\n")
                self.chat_box.see("end")
                self.status_label.configure(text="✅ Ready", text_color="green")
                return
            
            # Regular AI processing
            memory.add_conversation("user", user_text)
            
            # Save to character memory if active
            if self.char_memory and self.char_memory.is_active:
                self.char_memory.add_message_to_history("user", user_text)
            
            # ३. লজিক প্রসেসিং
            decision = reasoning_engine.analyze(user_text)
            
            # ४. কাজ সম্পাদন
            await action_executor.execute_tasks(decision.actions)
            
            # ५. এআই-এর উত্তর মেমরিতে সেভ করা
            memory.add_conversation("ai", decision.goal)
            
            if self.char_memory and self.char_memory.is_active:
                self.char_memory.add_message_to_history("ai", decision.goal)
            
            # Update avatar - happy
            self._update_avatar_emotion("happy")
            
            # ६. কথা বলা ও UI আপডেট
            await self.speak(decision.goal)
            self.chat_box.insert("end", f"🤖 Ayesha: {decision.goal}\n\n")
            self.chat_box.see("end")
            
            # Update status
            self.status_label.configure(text="✅ Ready", text_color="green")
            
        except Exception as e:
            logger.error(f"AI Error: {str(e)}")
            self.chat_box.insert("end", f"❌ Error: {str(e)}\n\n")
            self._update_avatar_emotion("confused")
            self.status_label.configure(text="❌ Error", text_color="red")

    def handle_input(self):
        """Handle user input"""
        user_text = self.entry.get().strip()
        if user_text:
            # Display user message
            self.chat_box.insert("end", f"👤 আপনি: {user_text}\n")
            self.chat_box.see("end")
            
            # Clear input
            self.entry.delete(0, "end")
            
            # Update avatar - excited
            self._update_avatar_emotion("excited")
            
            # Process in background thread
            threading.Thread(
                target=lambda: asyncio.run(self.run_ai(user_text)),
                daemon=True
            ).start()

    def cleanup(self):
        """Cleanup resources"""
        if self.avatar_window:
            try:
                self.avatar_window._on_closing()
            except Exception as e:
                logger.error(f"Error closing avatar: {str(e)}")

    def run(self):
        """Run the application"""
        try:
            # Set cleanup on window close
            self.app.protocol("WM_DELETE_WINDOW", self._on_closing)
            # Start info update loop
            threading.Thread(target=self._info_update_loop, daemon=True).start()
            self.app.mainloop()
        except Exception as e:
            logger.error(f"Application Error: {str(e)}")

    def _info_update_loop(self):
        """Update user info periodically"""
        while True:
            try:
                self._update_user_info()
                time.sleep(1)
            except Exception as e:
                logger.error(f"Info update error: {str(e)}")

    def _on_closing(self):
        """Handle window close event"""
        self.cleanup()
        self.app.destroy()


if __name__ == "__main__":
    try:
        ai = AyeshaAI_Professional()
        ai.run()
    except Exception as e:
        logger.error(f"Failed to start application: {str(e)}")
        print(f"Error: {str(e)}")
