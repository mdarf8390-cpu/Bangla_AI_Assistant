"""
Ayesha - Bangla Voice-Controlled Assistant (assistant.py)

Goal: Voice-driven assistant that understands Bangla natural language commands
to perform file operations, typing, clipboard, and basic mouse/keyboard actions.

Important:
- This is a starter, dependency-aware implementation focused on safety and
  helpful fallbacks. It tries to use offline/locally-available libraries but
  degrades gracefully with clear instructions if packages are missing.
- Destructive actions (file delete) ALWAYS ask for confirmation before running.
  When strict delete confirmation is enabled, only an explicit "হ্যাঁ"/"yes"
  (whole-word) will confirm deletion — short replies like "হুম" will NOT confirm.
- If media (music/video) appears to be playing on the PC, Ayesha will ask an
  extra explicit confirmation before listening, to avoid treating ambient audio
  as commands.
- Test in a safe directory first. The assistant will expand common location
  names like "Desktop" to the user's home Desktop.

Dependencies (recommended):
  pip install SpeechRecognition pyttsx3 pyautogui pyperclip psutil
  # For microphone input on Windows: pip install pipwin && pipwin install pyaudio
  # On mac/linux, install portaudio (system package) then pip install pyaudio

How to run:
  python cpu/Bangla_AI_Assistant/assistant.py --mode voice
  python cpu/Bangla_AI_Assistant/assistant.py --mode text

The assistant is intentionally conservative: if a dependency is missing it
prints clear instructions and continues in text-only mode.

Author: generated for pipraa on 2026-07-18
"""

from pathlib import Path
import os
import sys
import time
import re
import shutil
import argparse
import subprocess

# Optional imports - handled at runtime with fallbacks
try:
    import speech_recognition as sr
except Exception:
    sr = None

try:
    import pyttsx3
except Exception:
    pyttsx3 = None

try:
    import pyautogui
except Exception:
    pyautogui = None

try:
    import pyperclip
except Exception:
    pyperclip = None

# Optional process-checking package for media detection
try:
    import psutil
except Exception:
    psutil = None

HOME = Path.home()

# Map simple location words in Bangla/English to paths
LOCATION_MAP = {
    'desktop': HOME / 'Desktop',
    'ডেস্কটপ': HOME / 'Desktop',
    'home': HOME,
    'হোম': HOME,
    'documents': HOME / 'Documents',
    'ডকুমেন্টস': HOME / 'Documents',
}


def ensure_dir(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)


def is_media_playing_process_based() -> bool:
    """Heuristic: check running processes for common media players / browsers.
    This is a fast, cross-platform heuristic but not 100% accurate.
    Requires psutil installed.
    """
    if psutil is None:
        return False
    media_names = [
        'spotify', 'vlc', 'chrome', 'firefox', 'msedge', 'edge', 'wmplayer',
        'itunes', 'rhythmbox', 'mpv', 'totem', 'spotify.exe', 'vlc.exe',
        'chrome.exe', 'firefox.exe', 'msedge.exe', 'brave', 'opera',
    ]
    try:
        for p in psutil.process_iter(attrs=['name', 'cmdline']):
            name = (p.info.get('name') or '').lower()
            cmdline = ' '.join(p.info.get('cmdline') or []).lower()
            for mn in media_names:
                if mn in name or mn in cmdline:
                    return True
    except Exception:
        return False
    return False


class AyeshaAssistant:
    def __init__(self, voice_enabled=True, tts_enabled=True, dry_run=False, strict_delete_confirm=False):
        self.dry_run = dry_run
        self.recognizer = None
        self.mic = None
        self.voice_enabled = voice_enabled and (sr is not None)
        self.tts_enabled = tts_enabled and (pyttsx3 is not None)
        self.tts_engine = None
        self.strict_delete_confirm = strict_delete_confirm

        if self.voice_enabled:
            try:
                self.recognizer = sr.Recognizer()
                self.mic = sr.Microphone()
            except Exception as e:
                print("Microphone not available or speech_recognition not configured:", e)
                self.voice_enabled = False

        if self.tts_enabled:
            try:
                self.tts_engine = pyttsx3.init()
            except Exception as e:
                print("TTS engine (pyttsx3) not available:", e)
                self.tts_enabled = False

    def speak(self, text: str):
        # Print always for visibility
        print("Ayesha:", text)
        if self.tts_enabled and self.tts_engine:
            try:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            except Exception as e:
                print("TTS failed:", e)

    def listen(self, timeout=6, phrase_time_limit=15):
        """Listen from microphone and return recognized text (Bangla preferred).
        If media is detected playing on the PC, ask an explicit confirmation first
        to avoid treating background audio as commands.
        """
        if not self.voice_enabled:
            raise RuntimeError("Voice not available. Run in --mode text or install SpeechRecognition + microphone drivers.")

        # If media is playing, require an explicit confirmation before listening
        if is_media_playing_process_based():
            self.speak('আমি মনে করছি আপনার পিসিতে গান/ভিডিও চলছে — তাহলে ব্যাকগ্রাউন্ড শব্দ কম তবেই আমি শুনব। আপনি নিশ্চিতভাবে এখনই আমার কথা শুনতে চান কি?')
            try:
                ok = self.confirm('এখন শুনব কি?', strict=True)
            except Exception:
                ok = False
            if not ok:
                raise RuntimeError('Media playing — user did not confirm listening')

        with self.mic as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print("Listening...")
            try:
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                # Try Bangla recognition first
                for lang in ('bn-BD', 'bn-IN', 'bn'):
                    try:
                        text = self.recognizer.recognize_google(audio, language=lang)
                        print("(recognized [{}]):".format(lang), text)
                        return text
                    except Exception:
                        continue
                # Fallback to English
                text = self.recognizer.recognize_google(audio)
                print("(recognized [en]):", text)
                return text
            except sr.WaitTimeoutError:
                raise RuntimeError('Listening timed out; no speech detected')
            except Exception as e:
                raise RuntimeError('Speech recognition failed: ' + str(e))

    def confirm(self, prompt: str, strict: bool = False) -> bool:
        # Ask for confirmation by voice or text
        # strict=True requires an explicit whole-word match: 'হ্যাঁ', 'yes', 'y', 'ok', etc.
        self.speak(prompt + ' নিশ্চিত করতে "হ্যাঁ" বলুন অথবা "না" বলুন।')
        if self.voice_enabled:
            try:
                answer = self.listen(timeout=5, phrase_time_limit=4)
                answer = (answer or '').strip().lower()
                if strict:
                    # split into tokens and require an exact token
                    tokens = re.findall(r"[\w\u0980-\u09FF]+", answer)
                    good = set(['হ্যাঁ', 'হ্যা', 'yes', 'y', 'ok'])
                    for t in tokens:
                        if t in good:
                            return True
                    return False
                else:
                    return 'হ্যাঁ' in answer or answer in ('ha', 'yes', 'ok', 'y')
            except Exception as e:
                print('Confirmation listen failed:', e)
                return False
        else:
            resp = input('Confirm (হ্যাঁ/না): ').strip().lower()
            if strict:
                return resp in ('হ্যাঁ', 'হ্যা', 'yes', 'y', 'ok')
            return resp in ('হ্যাঁ', 'হ্যা', 'ha', 'yes', 'y', 'ok')

    def parse_command(self, text: str) -> dict:
        """Simple NLP to extract intents and arguments from Bangla natural language.
        Returns a dict with keys: intent, path, filename, content, raw
        intent: create_file, delete_file, write_file, type_text, clipboard_copy, unknown
        """
        raw = text.strip()
        lower = raw.lower()

        # Quick patterns
        # 1) Create file: 'তৈরি' or 'create' or 'নতুন ফাইল' and includes name
        m_name = re.search(r"['\"]([^'\"]+)['\"]", raw)  # quoted name
        filename = None
        if m_name:
            filename = m_name.group(1)

        # Try to extract name after 'নাম দে' বা 'নাম' patterns
        if not filename:
            m = re.search(r'নাম[ে]?\s+([\w\.\-]+)', raw)
            if m:
                filename = m.group(1)

        # Try to find location word
        location = None
        for key in LOCATION_MAP.keys():
            if key in lower:
                location = LOCATION_MAP[key]
                break

        # Create file
        if any(k in lower for k in ('তৈরি', 'create', 'নতুন ফাইল', 'ফাইল তৈরি')):
            return {'intent': 'create_file', 'path': location, 'filename': filename, 'raw': raw}

        # Delete file
        if any(k in lower for k in ('মুছে', 'ডিলিট', 'delete', 'মুছে ফেল')):
            # If quoted filename present, use it
            return {'intent': 'delete_file', 'path': location, 'filename': filename, 'raw': raw}

        # Write into file / Append
        if any(k in lower for k in ('লিখ', 'লেখ', "লেখা")):
            # extract text to write
            m_text = re.search(r"['\"]([^'\"]+)['\"]", raw)
            text_to_write = m_text.group(1) if m_text else None
            return {'intent': 'write_file', 'path': location, 'filename': filename, 'content': text_to_write, 'raw': raw}

        # Type text (keyboard)
        if any(k in lower for k in ('টাইপ', 'type', 'কিবোর্ড')) or 'এখানে' in lower:
            m_text = re.search(r"['\"]([^'\"]+)['\"]", raw)
            text_to_type = m_text.group(1) if m_text else None
            return {'intent': 'type_text', 'content': text_to_type, 'raw': raw}

        # Clipboard copy
        if any(k in lower for k in ('কপি কর', 'clipboard', 'ক্লিপবোর্ড')) and m_name:
            return {'intent': 'clipboard_copy', 'content': filename, 'raw': raw}

        # Open file
        if any(k in lower for k in ('খোল', 'open', 'ইনিস্টল')) and filename:
            return {'intent': 'open_file', 'path': location, 'filename': filename, 'raw': raw}

        return {'intent': 'unknown', 'raw': raw}

    def resolve_path(self, path: Path or None, filename: str or None) -> Path:
        if filename is None:
            raise ValueError('filename is required')
        if path is None:
            # default to current working directory
            path = Path.cwd()
        target = Path(path) / filename
        return target.expanduser()

    def act(self, cmd: dict):
        intent = cmd.get('intent')
        try:
            if intent == 'create_file':
                fn = cmd.get('filename') or 'untitled.txt'
                target = self.resolve_path(cmd.get('path'), fn)
                ensure_dir(target)
                if target.exists():
                    self.speak(f"{target} আগেই আছে। আমি নতুন ফাইল তৈরি করছি না।")
                    return
                if self.dry_run:
                    self.speak(f"Dry-run: would create {target}")
                    return
                target.write_text('')
                self.speak(f"✅ {target} তৈরি হয়ে গেছে।")

            elif intent == 'delete_file':
                fn = cmd.get('filename')
                if not fn:
                    self.speak('কোন ফাইল মুছতে হবে সেটা বলুন (ফাইলের নাম).')
                    return
                target = self.resolve_path(cmd.get('path'), fn)
                if not target.exists():
                    self.speak(f"{target} পাওয়া যায়নি।")
                    return
                # Use strict confirmation for delete when enabled
                confirmed = self.confirm(f'আপনি কি নিশ্চিত যে {target} মুছে ফেলতে চান?', strict=self.strict_delete_confirm)
                if not confirmed:
                    self.speak('মুছে ফেলা বাতিল করা হয়েছে।')
                    return
                if self.dry_run:
                    self.speak(f"Dry-run: would delete {target}")
                    return
                if target.is_dir():
                    shutil.rmtree(target)
                else:
                    target.unlink()
                self.speak('✅ Deleted!')

            elif intent == 'write_file':
                fn = cmd.get('filename') or 'untitled.txt'
                content = cmd.get('content') or ''
                target = self.resolve_path(cmd.get('path'), fn)
                ensure_dir(target)
                if self.dry_run:
                    self.speak(f"Dry-run: would append to {target}: {content}")
                    return
                with target.open('a', encoding='utf-8') as f:
                    f.write(content + '\n')
                self.speak(f"✅ লেখাটি {target} এ যোগ করা হয়েছে।")

            elif intent == 'type_text':
                content = cmd.get('content')
                if not content:
                    self.speak('কী লিখতে হবে সেটা বলেন।')
                    return
                if pyautogui is None:
                    self.speak('Typing (pyautogui) লাইব্রেরি পাওয়া যায়নি। টেক্সট কপি করে ক্লিপবোর্ডে রাখছি।')
                    if pyperclip:
                        pyperclip.copy(content)
                        self.speak('ক্লিপবোর্ডে কপি করা হয়েছে — যেখানে পেস্ট করবেন সেখানে পেস্ট করুন।')
                    else:
                        self.speak('pyperclip নেই; অনুগ্রহ করে pip install pyperclip করুন।')
                    return
                if self.dry_run:
                    self.speak(f"Dry-run: would type: {content}")
                    return
                # give user 2 seconds to focus the input field
                self.speak('আমি ২ সেকেন্ড পরে টাইপ শুরু করব — যে ইক্সটে লিখতে চান সেখানে কার্সার রাখুন।')
                time.sleep(2)
                pyautogui.typewrite(content)
                self.speak('✅ টাইপ শেষ।')

            elif intent == 'clipboard_copy':
                content = cmd.get('content')
                if not content:
                    self.speak('কপির জন্য কিছু নেই।')
                    return
                if pyperclip is None:
                    self.speak('pyperclip নেই; pip install pyperclip করে নিন।')
                    return
                pyperclip.copy(content)
                self.speak('✅ ক্লিপবোর্ডে কপি করা হয়েছে।')

            elif intent == 'open_file':
                fn = cmd.get('filename')
                target = self.resolve_path(cmd.get('path'), fn)
                if not target.exists():
                    self.speak(f"{target} পাওয়া যায়নি।")
                    return
                if sys.platform.startswith('darwin'):
                    subprocess.run(['open', str(target)])
                elif os.name == 'nt':
                    os.startfile(str(target))
                else:
                    subprocess.run(['xdg-open', str(target)])
                self.speak('✅ ফাইল খোলা হয়েছে (ডিফল্ট অ্যাপ)।')

            else:
                self.speak('দুঃখিত — আমি সেটি বুঝতে পারিনি। আরেকবার বলুন বা টেক্সট মোড ট্রাই করুন।')
        except Exception as e:
            self.speak('অপারেশন করার সময় ত্রুটি: ' + str(e))


def check_dependencies():
    missing = []
    if sr is None:
        missing.append('SpeechRecognition')
    if pyttsx3 is None:
        missing.append('pyttsx3')
    if pyautogui is None:
        missing.append('pyautogui')
    if pyperclip is None:
        missing.append('pyperclip')
    if psutil is None:
        missing.append('psutil (recommended for media-detection)')

    if missing:
        print('\n================= Missing optional packages =================')
        print('কিছু প্যাকেজ ইনস্টল নেই — পুরো ফিচার কাজ নাও করতে পারে:')
        for m in missing:
            print('-', m)
        print('\nInstall recommendations:')
        print('  pip install SpeechRecognition pyttsx3 pyautogui pyperclip psutil')
        print('For pyaudio (mic) on Windows: pip install pipwin && pipwin install pyaudio')
        print('============================================================\n')


def main():
    parser = argparse.ArgumentParser(description='Ayesha - Bangla voice assistant')
    parser.add_argument('--mode', choices=['voice', 'text'], default='voice')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    check_dependencies()

    mode = args.mode
    # strict_delete_confirm=True as requested
    assistant = AyeshaAssistant(voice_enabled=(mode == 'voice'), tts_enabled=True, dry_run=args.dry_run, strict_delete_confirm=True)

    assistant.speak('Ayesha প্রস্তুত। কিভাবে সাহায্য করতে পারি?')

    while True:
        try:
            if mode == 'voice' and assistant.voice_enabled:
                try:
                    text = assistant.listen()
                except Exception as e:
                    print('Voice failed or skipped:', e)
                    # fallback to text mode interaction
                    mode = 'text'
                    continue
            else:
                text = input('আপনি বলুন (বা exit): ')

            if not text:
                continue
            if text.strip().lower() in ('exit', 'quit', 'বন্ধ', 'শেষ'):
                assistant.speak('বিদায়!')
                break

            cmd = assistant.parse_command(text)
            # If unknown and voice mode, optionally ask to confirm parsing via text in future
            assistant.act(cmd)

        except KeyboardInterrupt:
            assistant.speak('বিদায়!')
            break
        except Exception as e:
            print('Error in loop:', e)
            assistant.speak('কিছু সমস্যা হয়েছে: ' + str(e))


if __name__ == '__main__':
    main()
