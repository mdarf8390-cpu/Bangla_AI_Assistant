import customtkinter as ctk
import asyncio
from core.event_bus import event_bus

class AyeshaUI:
    def __init__(self, loop):
        self.loop = loop # Asyncio loop পাস করতে হবে
        self.app = ctk.CTk()
        self.setup_ui()
        
        # AI রেসপন্স শোনার জন্য সাবস্ক্রাইব
        event_bus.subscribe("ai_response", self.display_response)

    def setup_ui(self):
        self.app.title("🤖 AYESHA AI")
        self.app.geometry("950x650")
        self.chat_box = ctk.CTkTextbox(self.app, width=900, height=500)
        self.chat_box.pack(pady=10)
        self.entry = ctk.CTkEntry(self.app, width=750, height=40)
        self.entry.pack(side="left", padx=10, pady=10)
        self.send_btn = ctk.CTkButton(self.app, text="Send", command=self.send_message)
        self.send_btn.pack(side="right", padx=10)

    def send_message(self):
        question = self.entry.get().strip()
        if not question: return
        
        self.chat_box.insert("end", f"👤 আপনি: {question}\n\n")
        self.entry.delete(0, "end")
        
        # সরাসরি কল না করে EventBus এর মাধ্যমে পাঠানো
        asyncio.run_coroutine_threadsafe(
            event_bus.emit("user_input", question), self.loop
        )

    async def display_response(self, event):
        # AI থেকে পাওয়া উত্তর স্ক্রিনে দেখানো
        answer = event.payload
        self.chat_box.insert("end", f"🤖 AYESHA: {answer}\n\n")
        self.chat_box.see("end")

    def run(self):
        self.app.mainloop()