class PromptBuilder:
    def build(self, user_text: str, memory_data: dict, context_data: dict, skills: list, history: list):
        """Build prompt from user text and context"""
        return f"""
[SYSTEM]
You are AYESHA, an advanced personal AI assistant.

[MEMORY]
{memory_data}

[CONTEXT]
{context_data}

[USER]
{user_text}

[INSTRUCTION]
Return ONLY valid JSON with keys: intent, goal, priority, answer, tasks
"""
    
    def build_smart(self, user_input: str, context: dict) -> str:
        """Smart prompt builder"""
        return f"""
[SYSTEM ROLE]
You are AYESHA, an intelligent assistant.

[CURRENT STATE]
{context}

[USER INPUT]
{user_input}

[INSTRUCTION]
Return strictly JSON with keys: intent, goal, priority, answer, tasks.
"""

# Global instance
prompt_builder = PromptBuilder()
