from automation.skills.youtube import YouTubeSkill
from automation.skills.google import GoogleSkill
from automation.skills.notepad import NotepadSkill
from automation.skills.vscode import VSCodeSkill
from automation.skills.whatsapp import WhatsAppSkill
from automation.skills.telegram import TelegramSkill
from automation.skills.discord import DiscordSkill
from automation.skills.spotify import SpotifySkill

print("Loading Skills...")

YouTubeSkill()
GoogleSkill()
NotepadSkill()
VSCodeSkill()
WhatsAppSkill()
TelegramSkill()
DiscordSkill()
SpotifySkill()

print("All Skills Loaded Successfully!")