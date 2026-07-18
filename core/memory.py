"""
=========================================================
AYESHA AI
Memory Manager
Version : 3.0
=========================================================
"""

from __future__ import annotations

import json
import time
import uuid
import threading
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Any


# =========================================================
# Memory Item
# =========================================================

@dataclass
class MemoryItem:

    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    category: str = "general"

    key: str = ""

    value: Any = None

    importance: int = 1

    created: float = field(default_factory=time.time)

    updated: float = field(default_factory=time.time)

    access_count: int = 0

    tags: List[str] = field(default_factory=list)

    metadata: Dict[str, Any] = field(default_factory=dict)


# =========================================================
# Conversation
# =========================================================

@dataclass
class Conversation:

    role: str

    message: str

    timestamp: float = field(default_factory=time.time)


# =========================================================
# Goal
# =========================================================

@dataclass
class Goal:

    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    title: str = ""

    status: str = "pending"

    created: float = field(default_factory=time.time)

    completed: Optional[float] = None


# =========================================================
# Task
# =========================================================

@dataclass
class TaskHistory:

    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    task: str = ""

    success: bool = False

    timestamp: float = field(default_factory=time.time)

    result: Dict[str, Any] = field(default_factory=dict)


# =========================================================
# User Profile
# =========================================================

@dataclass
class UserProfile:

    name: str = ""

    language: str = "bangla"

    city: str = ""

    preferences: Dict[str, Any] = field(default_factory=dict)

    favorite_apps: List[str] = field(default_factory=list)

    projects: List[str] = field(default_factory=list)


# =========================================================
# Memory Manager
# =========================================================

class MemoryManager:

    def __init__(self,
                 db_path: str = "database/memory.json"):

        self.db_path = Path(db_path)

        self.lock = threading.RLock()

        self.short_memory: List[Conversation] = []

        self.long_memory: Dict[str, MemoryItem] = {}

        self.task_history: List[TaskHistory] = []

        self.goals: List[Goal] = []

        self.profile = UserProfile()

        self.max_short_memory = 50

        self.auto_save = True

        self._load()

    # -------------------------------------------------

    def remember(self,
                 key: str,
                 value: Any,
                 category="general",
                 importance=1,
                 tags=None):

        with self.lock:

            item = MemoryItem(

                key=key,

                value=value,

                category=category,

                importance=importance,

                tags=tags or []

            )

            self.long_memory[key] = item

            if self.auto_save:

                self.save()

            return item

    # -------------------------------------------------

    def recall(self,
               key: str):

        with self.lock:

            item = self.long_memory.get(key)

            if item:

                item.access_count += 1

                item.updated = time.time()

                return item.value

            return None

    # -------------------------------------------------

    def forget(self,
               key: str):

        with self.lock:

            if key in self.long_memory:

                del self.long_memory[key]

                self.save()

                return True

            return False    # -------------------------------------------------
    # Conversation Memory
    # -------------------------------------------------

    def add_conversation(self,
                         role: str,
                         message: str):

        with self.lock:

            self.short_memory.append(

                Conversation(

                    role=role,

                    message=message

                )

            )

            if len(self.short_memory) > self.max_short_memory:

                self.short_memory.pop(0)

            if self.auto_save:

                self.save()

    # -------------------------------------------------

    def get_conversation(self,
                         limit: int = 20):

        with self.lock:

            return self.short_memory[-limit:]

    # -------------------------------------------------

    def clear_conversation(self):

        with self.lock:

            self.short_memory.clear()

            self.save()

    # -------------------------------------------------
    # Task History
    # -------------------------------------------------

    def add_task(self,
                 task: str,
                 success: bool,
                 result=None):

        with self.lock:

            self.task_history.append(

                TaskHistory(

                    task=task,

                    success=success,

                    result=result or {}

                )

            )

            self.save()

    # -------------------------------------------------

    def last_tasks(self,
                   limit=20):

        return self.task_history[-limit:]

    # -------------------------------------------------
    # Goals
    # -------------------------------------------------

    def add_goal(self,
                 title: str):

        goal = Goal(

            title=title

        )

        self.goals.append(goal)

        self.save()

        return goal

    # -------------------------------------------------

    def complete_goal(self,
                      goal_id: str):

        for goal in self.goals:

            if goal.id == goal_id:

                goal.status = "completed"

                goal.completed = time.time()

                self.save()

                return True

        return False

    # -------------------------------------------------

    def pending_goals(self):

        return [

            g

            for g in self.goals

            if g.status == "pending"

        ]

    # -------------------------------------------------
    # User Profile
    # -------------------------------------------------

    def set_name(self,
                 name):

        self.profile.name = name

        self.save()

    # -------------------------------------------------

    def set_language(self,
                     language):

        self.profile.language = language

        self.save()

    # -------------------------------------------------

    def add_preference(self,
                       key,
                       value):

        self.profile.preferences[key] = value

        self.save()

    # -------------------------------------------------

    def add_favorite_app(self,
                         app):

        if app not in self.profile.favorite_apps:

            self.profile.favorite_apps.append(app)

            self.save()

    # -------------------------------------------------

    def add_project(self,
                    project):

        if project not in self.profile.projects:

            self.profile.projects.append(project)

            self.save()

    # -------------------------------------------------
    # Search
    # -------------------------------------------------

    def search(self,
               keyword):

        result = []

        keyword = keyword.lower()

        for item in self.long_memory.values():

            if (

                keyword in item.key.lower()

                or

                keyword in str(item.value).lower()

            ):

                result.append(item)

        return result

    # -------------------------------------------------

    def exists(self,
               key):

        return key in self.long_memory

    # -------------------------------------------------

    def update(self,
               key,
               value):

        if key not in self.long_memory:

            return False

        item = self.long_memory[key]

        item.value = value

        item.updated = time.time()

        self.save()

        return True    # -------------------------------------------------
    # Save Database
    # -------------------------------------------------

    def save(self):

        with self.lock:

            self.db_path.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            data = {

                "profile": asdict(self.profile),

                "memory": {

                    key: asdict(value)

                    for key, value in self.long_memory.items()

                },

                "conversation": [

                    asdict(x)

                    for x in self.short_memory

                ],

                "tasks": [

                    asdict(x)

                    for x in self.task_history

                ],

                "goals": [

                    asdict(x)

                    for x in self.goals

                ]

            }

            with open(

                self.db_path,

                "w",

                encoding="utf-8"

            ) as f:

                json.dump(

                    data,

                    f,

                    indent=4,

                    ensure_ascii=False

                )

    # -------------------------------------------------
    # Load Database
    # -------------------------------------------------

    def _load(self):

        if not self.db_path.exists():

            return

        try:

            with open(

                self.db_path,

                "r",

                encoding="utf-8"

            ) as f:

                data = json.load(f)

        except Exception:

            return

        profile = data.get("profile", {})

        self.profile = UserProfile(**profile)

        self.long_memory.clear()

        for key, value in data.get("memory", {}).items():

            self.long_memory[key] = MemoryItem(**value)

        self.short_memory = [

            Conversation(**x)

            for x in data.get(

                "conversation",

                []

            )

        ]

        self.task_history = [

            TaskHistory(**x)

            for x in data.get(

                "tasks",

                []

            )

        ]

        self.goals = [

            Goal(**x)

            for x in data.get(

                "goals",

                []

            )

        ]

    # -------------------------------------------------
    # Export
    # -------------------------------------------------

    def export(self, path):

        self.save()

        import shutil

        shutil.copy(

            self.db_path,

            path

        )

    # -------------------------------------------------
    # Import
    # -------------------------------------------------

    def import_file(self, path):

        import shutil

        shutil.copy(

            path,

            self.db_path

        )

        self._load()

    # -------------------------------------------------
    # Statistics
    # -------------------------------------------------

    def statistics(self):

        return {

            "memory_items": len(

                self.long_memory

            ),

            "conversation": len(

                self.short_memory

            ),

            "goals": len(

                self.goals

            ),

            "completed_goals":

                len(

                    [

                        g

                        for g in self.goals

                        if g.status == "completed"

                    ]

                ),

            "tasks": len(

                self.task_history

            ),

            "favorite_apps":

                len(

                    self.profile.favorite_apps

                ),

            "projects":

                len(

                    self.profile.projects

                )

        }

    # -------------------------------------------------
    # Clear
    # -------------------------------------------------

    def clear_all(self):

        with self.lock:

            self.long_memory.clear()

            self.short_memory.clear()

            self.task_history.clear()

            self.goals.clear()

            self.profile = UserProfile()

            self.save()

    # -------------------------------------------------

    def status(self):

        return {

            "module": "MemoryManager",

            "database": str(

                self.db_path

            ),

            "loaded":

                self.db_path.exists(),

            "statistics":

                self.statistics(),

            "ready": True

        }


memory = MemoryManager()