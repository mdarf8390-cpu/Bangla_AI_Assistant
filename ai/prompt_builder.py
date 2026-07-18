class PromptBuilder:
    def build_smart(self, user_input: str, context: dict) -> str:
        # Context থেকে সিস্টেম স্টেট পাঠানো হচ্ছে
        return f"""
        [SYSTEM ROLE]
        You are AYESHA, an intelligent assistant. 
        [CURRENT STATE]
        {context}
        [USER INPUT]
        {user_input}
        [INSTRUCTION]
        Return strictly JSON with keys: "intent", "goal", "priority", "answer", "tasks".
        """