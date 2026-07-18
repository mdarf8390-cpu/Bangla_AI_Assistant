import json
import os
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from enum import Enum

logger = logging.getLogger(__name__)


class KnowledgeType(Enum):
    """Type of knowledge learned"""
    CORRECT = "correct"
    INCORRECT = "incorrect"
    USER_FEEDBACK = "user_feedback"


class UserProfile:
    """Profile for individual users"""
    
    def __init__(self, name: str):
        self.name = name
        self.first_met = datetime.now()
        self.last_interaction = datetime.now()
        self.interaction_count = 0
        self.active_sessions = 0
        self.total_active_time = 0  # in seconds
        self.preferences = {}
        
    def to_dict(self) -> dict:
        """Convert to dictionary for storage"""
        return {
            "name": self.name,
            "first_met": self.first_met.isoformat(),
            "last_interaction": self.last_interaction.isoformat(),
            "interaction_count": self.interaction_count,
            "active_sessions": self.active_sessions,
            "total_active_time": self.total_active_time,
            "preferences": self.preferences
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'UserProfile':
        """Create from dictionary"""
        profile = UserProfile(data["name"])
        profile.first_met = datetime.fromisoformat(data["first_met"])
        profile.last_interaction = datetime.fromisoformat(data["last_interaction"])
        profile.interaction_count = data["interaction_count"]
        profile.active_sessions = data["active_sessions"]
        profile.total_active_time = data["total_active_time"]
        profile.preferences = data.get("preferences", {})
        return profile


class LearnedBehavior:
    """Behavior learned from user feedback"""
    
    def __init__(self, behavior_id: str, description: str, category: str):
        self.id = behavior_id
        self.description = description
        self.category = category
        self.knowledge_type = KnowledgeType.CORRECT
        self.confidence = 0.5
        self.learned_on = datetime.now()
        self.reinforcement_count = 0
        self.last_reinforced = datetime.now()
        
    def reinforce(self):
        """Increase confidence through reinforcement"""
        self.reinforcement_count += 1
        self.confidence = min(1.0, self.confidence + 0.1)
        self.last_reinforced = datetime.now()
        
    def weaken(self):
        """Decrease confidence if proven wrong"""
        self.confidence = max(0.0, self.confidence - 0.2)
        self.reinforcement_count = max(0, self.reinforcement_count - 1)
        
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "description": self.description,
            "category": self.category,
            "knowledge_type": self.knowledge_type.value,
            "confidence": self.confidence,
            "learned_on": self.learned_on.isoformat(),
            "reinforcement_count": self.reinforcement_count,
            "last_reinforced": self.last_reinforced.isoformat()
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'LearnedBehavior':
        """Create from dictionary"""
        behavior = LearnedBehavior(data["id"], data["description"], data["category"])
        behavior.knowledge_type = KnowledgeType(data["knowledge_type"])
        behavior.confidence = data["confidence"]
        behavior.learned_on = datetime.fromisoformat(data["learned_on"])
        behavior.reinforcement_count = data["reinforcement_count"]
        behavior.last_reinforced = datetime.fromisoformat(data["last_reinforced"])
        return behavior


class ConversationHistory:
    """Store conversation history with context"""
    
    def __init__(self, user_name: str):
        self.user_name = user_name
        self.messages: List[Dict] = []
        self.contexts: List[Dict] = []
        
    def add_message(self, role: str, content: str, timestamp: Optional[datetime] = None):
        """Add message to history"""
        if timestamp is None:
            timestamp = datetime.now()
        
        self.messages.append({
            "role": role,
            "content": content,
            "timestamp": timestamp.isoformat(),
            "language": "bangla"
        })
    
    def add_context(self, context_key: str, context_value: str):
        """Add context information"""
        self.contexts.append({
            "key": context_key,
            "value": context_value,
            "timestamp": datetime.now().isoformat()
        })
    
    def get_recent_context(self, num_messages: int = 5) -> List[str]:
        """Get recent message context"""
        return [msg["content"] for msg in self.messages[-num_messages:]]
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "user_name": self.user_name,
            "messages": self.messages,
            "contexts": self.contexts
        }


class CharacterMemory:
    """Character's memory system with learning capabilities"""
    
    def __init__(self, storage_path: str = "character_memory.json"):
        self.storage_path = storage_path
        
        # Core memory
        self.learned_behaviors: Dict[str, LearnedBehavior] = {}
        self.user_profiles: Dict[str, UserProfile] = {}
        self.conversation_histories: Dict[str, ConversationHistory] = {}
        self.mistakes_corrected: List[Dict] = []
        self.positive_reinforcements: List[Dict] = []
        
        # Active session tracking
        self.active_user = None
        self.session_start_time = None
        self.is_active = False
        
        # Load existing memory
        self._load_memory()

    def _load_memory(self):
        """Load memory from storage"""
        try:
            if os.path.exists(self.storage_path):
                with open(self.storage_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    # Load learned behaviors
                    for behavior_id, behavior_data in data.get("learned_behaviors", {}).items():
                        self.learned_behaviors[behavior_id] = LearnedBehavior.from_dict(behavior_data)
                    
                    # Load user profiles
                    for user_name, profile_data in data.get("user_profiles", {}).items():
                        self.user_profiles[user_name] = UserProfile.from_dict(profile_data)
                    
                    # Load conversation histories
                    for user_name, history_data in data.get("conversation_histories", {}).items():
                        history = ConversationHistory(user_name)
                        history.messages = history_data.get("messages", [])
                        history.contexts = history_data.get("contexts", [])
                        self.conversation_histories[user_name] = history
                    
                    self.mistakes_corrected = data.get("mistakes_corrected", [])
                    self.positive_reinforcements = data.get("positive_reinforcements", [])
                    
                    logger.info("Memory loaded successfully")
            else:
                logger.info("No existing memory found, starting fresh")
        except Exception as e:
            logger.error(f"Error loading memory: {str(e)}")

    def _save_memory(self):
        """Save memory to storage"""
        try:
            data = {
                "learned_behaviors": {
                    bid: behavior.to_dict() 
                    for bid, behavior in self.learned_behaviors.items()
                },
                "user_profiles": {
                    name: profile.to_dict() 
                    for name, profile in self.user_profiles.items()
                },
                "conversation_histories": {
                    name: history.to_dict() 
                    for name, history in self.conversation_histories.items()
                },
                "mistakes_corrected": self.mistakes_corrected,
                "positive_reinforcements": self.positive_reinforcements
            }
            
            with open(self.storage_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            logger.info("Memory saved successfully")
        except Exception as e:
            logger.error(f"Error saving memory: {str(e)}")

    def activate_user(self, user_name: str) -> str:
        """Activate a user and start tracking"""
        # Recognize or create user
        if user_name not in self.user_profiles:
            self.user_profiles[user_name] = UserProfile(user_name)
            response = f"🎉 আহা! নতুন বন্ধু {user_name}! আমি তোমাকে চিনলাম। আমার নাম Ayesha। তোমার সাথে কাজ করতে পেরে আমি খুশি!"
        else:
            profile = self.user_profiles[user_name]
            last_seen = profile.last_interaction
            time_diff = datetime.now() - last_seen
            
            if time_diff.days > 0:
                response = f"😊 আহ {user_name}! তুমি আবার ফিরে এসেছ! আমি তোমাকে মনে আছে। গত {time_diff.days} দিন পর দেখা হচ্ছে!"
            else:
                response = f"👋 স্বাগতম {user_name}! আবার দেখা হলো। আমি তোমাকে কিভাবে সাহায্য করতে পারি?"
        
        # Start session
        self.active_user = user_name
        self.session_start_time = datetime.now()
        self.is_active = True
        
        profile = self.user_profiles[user_name]
        profile.active_sessions += 1
        profile.last_interaction = datetime.now()
        
        # Create conversation history if not exists
        if user_name not in self.conversation_histories:
            self.conversation_histories[user_name] = ConversationHistory(user_name)
        
        self._save_memory()
        return response

    def deactivate_user(self) -> str:
        """End user session and track time"""
        if not self.active_user:
            return "কোন active session নেই।"
        
        if self.session_start_time:
            session_duration = (datetime.now() - self.session_start_time).total_seconds()
            profile = self.user_profiles[self.active_user]
            profile.total_active_time += int(session_duration)
            
            # Format duration
            hours = int(session_duration // 3600)
            minutes = int((session_duration % 3600) // 60)
            
            if hours > 0:
                duration_str = f"{hours} ঘন্টা {minutes} মিনিট"
            else:
                duration_str = f"{minutes} মিনিট"
            
            response = f"👋 বাই {self.active_user}! তুমি {duration_str} সময় আমার সাথে ছিলে। আশা করি পরবর্তী দেখা হবে! আমি তোমাকে মনে রাখব।"
        else:
            response = f"👋 বাই {self.active_user}!"
        
        self.active_user = None
        self.session_start_time = None
        self.is_active = False
        self._save_memory()
        
        return response

    def learn_behavior(self, behavior_id: str, description: str, category: str, is_correct: bool = True):
        """Learn a behavior from user feedback"""
        if behavior_id not in self.learned_behaviors:
            behavior = LearnedBehavior(behavior_id, description, category)
            if is_correct:
                behavior.knowledge_type = KnowledgeType.CORRECT
                behavior.confidence = 0.8
            else:
                behavior.knowledge_type = KnowledgeType.INCORRECT
                behavior.confidence = 0.2
            self.learned_behaviors[behavior_id] = behavior
        else:
            behavior = self.learned_behaviors[behavior_id]
            if is_correct:
                behavior.reinforce()
            else:
                behavior.weaken()
        
        self._save_memory()

    def correct_mistake(self, mistake_description: str, correction: str, category: str = "general") -> str:
        """User corrects a mistake the character made"""
        timestamp = datetime.now().isoformat()
        
        # Record the correction
        self.mistakes_corrected.append({
            "mistake": mistake_description,
            "correction": correction,
            "category": category,
            "timestamp": timestamp,
            "user": self.active_user
        })
        
        # Learn from mistake
        mistake_id = f"mistake_{len(self.mistakes_corrected)}"
        self.learn_behavior(
            mistake_id,
            f"না করব: {mistake_description}। সঠিক উপায়: {correction}",
            category,
            is_correct=False
        )
        
        # Generate response in Bangla
        response = f"🙏 ধন্যবাদ {self.active_user}! আমি এটা ভুল করেছিলাম। এখন আমি জানি যে {correction}। আমি এটা মনে রাখব এবং আবার ভুল করব না।"
        
        self._save_memory()
        return response

    def reinforce_correct_behavior(self, behavior_description: str, category: str = "general") -> str:
        """User reinforces a correct behavior"""
        timestamp = datetime.now().isoformat()
        
        # Record the reinforcement
        self.positive_reinforcements.append({
            "behavior": behavior_description,
            "category": category,
            "timestamp": timestamp,
            "user": self.active_user
        })
        
        # Learn from positive feedback
        behavior_id = f"positive_{len(self.positive_reinforcements)}"
        self.learn_behavior(
            behavior_id,
            behavior_description,
            category,
            is_correct=True
        )
        
        # Generate response
        response = f"😊 ধন্যবাদ {self.active_user}! আমি খুশি যে আমি এটা ঠিক করেছি। এটা আমাকে আরও ভালো হতে সাহায্য করে। আমি এটা মনে রাখব!"
        
        self._save_memory()
        return response

    def add_message_to_history(self, role: str, content: str):
        """Add message to conversation history"""
        if not self.active_user:
            return
        
        if self.active_user not in self.conversation_histories:
            self.conversation_histories[self.active_user] = ConversationHistory(self.active_user)
        
        self.conversation_histories[self.active_user].add_message(role, content)
        self._save_memory()

    def get_user_info(self, user_name: str) -> Dict:
        """Get information about a user"""
        if user_name not in self.user_profiles:
            return None
        
        profile = self.user_profiles[user_name]
        return {
            "name": profile.name,
            "first_met": profile.first_met.isoformat(),
            "last_interaction": profile.last_interaction.isoformat(),
            "interaction_count": profile.interaction_count,
            "total_sessions": profile.active_sessions,
            "total_active_time_seconds": profile.total_active_time,
            "total_active_time_formatted": self._format_duration(profile.total_active_time)
        }

    def _format_duration(self, seconds: int) -> str:
        """Format duration in Bangla"""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        
        if hours > 0:
            return f"{hours} ঘন্টা {minutes} মিনিট"
        else:
            return f"{minutes} মিনিট"

    def get_learned_behaviors(self, category: Optional[str] = None) -> List[Dict]:
        """Get learned behaviors, optionally filtered by category"""
        behaviors = []
        for bid, behavior in self.learned_behaviors.items():
            if category is None or behavior.category == category:
                behaviors.append({
                    "id": bid,
                    "description": behavior.description,
                    "category": behavior.category,
                    "confidence": behavior.confidence,
                    "reinforcements": behavior.reinforcement_count
                })
        return behaviors

    def get_session_info(self) -> Dict:
        """Get current session information"""
        if not self.is_active or not self.active_user:
            return {
                "active": False,
                "current_user": None,
                "session_duration": 0
            }
        
        duration = (datetime.now() - self.session_start_time).total_seconds()
        return {
            "active": True,
            "current_user": self.active_user,
            "session_duration": int(duration),
            "session_duration_formatted": self._format_duration(int(duration))
        }

    def recognize_user_by_voice_or_name(self, name: str) -> Tuple[bool, str]:
        """Check if user is recognized"""
        if name in self.user_profiles:
            profile = self.user_profiles[name]
            return True, f"😊 আহ {name}! আমি তোমাকে চিনি। তুমি {profile.interaction_count} বার আমার সাথে কথা বলেছ।"
        else:
            return False, f"আমি {name} কে চিনি না। কিন্তু আমি তোমাকে শিখতে পারি!"


# Global memory instance
character_memory = None


def initialize_memory(storage_path: str = "character_memory.json") -> CharacterMemory:
    """Initialize global character memory"""
    global character_memory
    character_memory = CharacterMemory(storage_path)
    return character_memory


def get_memory() -> CharacterMemory:
    """Get global character memory instance"""
    global character_memory
    if character_memory is None:
        character_memory = CharacterMemory()
    return character_memory
