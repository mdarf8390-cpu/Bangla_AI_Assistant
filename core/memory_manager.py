"""
AYESHA AI
Memory Manager
"""

from core.memory import memory

class MemoryManager:
    def __init__(self):
        self.memory = memory

    def save(self):
        if hasattr(self.memory, "save"):
            return self.memory.save()

    def load(self):
        if hasattr(self.memory, "load"):
            return self.memory.load()

    def statistics(self):
        if hasattr(self.memory, "statistics"):
            return self.memory.statistics()
        return {}

    def add_conversation(self, role, message):
        if hasattr(self.memory, "add_conversation"):
            return self.memory.add_conversation(role, message)

    def add_goal(self, goal):
        if hasattr(self.memory, "add_goal"):
            return self.memory.add_goal(goal)

    def get_memory(self):
        return self.memory


# Singleton
memory_manager = MemoryManager()

# Backward Compatibility
memory = memory_manager