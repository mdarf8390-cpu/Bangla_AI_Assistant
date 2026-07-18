"""
=========================================================
AYESHA AI
Goal Manager
Version : 3.0
=========================================================
"""

from __future__ import annotations

import uuid
import time
import threading

from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional

from core.memory import memory
from core.context_manager import context


# ==========================================================
# Goal
# ==========================================================

@dataclass
class Goal:

    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    title: str = ""

    description: str = ""

    priority: int = 1

    status: str = "pending"

    progress: float = 0.0

    created: float = field(default_factory=time.time)

    updated: float = field(default_factory=time.time)

    completed: Optional[float] = None

    parent: Optional[str] = None

    metadata: Dict = field(default_factory=dict)


# ==========================================================
# Goal Manager
# ==========================================================

class GoalManager:

    def __init__(self):

        self.lock = threading.RLock()

        self.goals: Dict[str, Goal] = {}

    # --------------------------------------------------

    def create_goal(

            self,

            title,

            description="",

            priority=1,

            parent=None

    ):

        with self.lock:

            goal = Goal(

                title=title,

                description=description,

                priority=priority,

                parent=parent

            )

            self.goals[goal.id] = goal

            memory.add_goal(title)

            context.set_goal(title)

            return goal

    # --------------------------------------------------

    def get_goal(self, goal_id):

        return self.goals.get(goal_id)

    # --------------------------------------------------

    def current_goal(self):

        pending = [

            g

            for g in self.goals.values()

            if g.status == "pending"

        ]

        if not pending:

            return None

        pending.sort(

            key=lambda x: x.priority,

            reverse=True

        )

        return pending[0]

    # --------------------------------------------------

    def update_progress(

            self,

            goal_id,

            progress

    ):

        goal = self.goals.get(goal_id)

        if not goal:

            return False

        goal.progress = progress

        goal.updated = time.time()

        return True    # --------------------------------------------------
    # Complete Goal
    # --------------------------------------------------

    def complete_goal(self, goal_id):

        with self.lock:

            goal = self.goals.get(goal_id)

            if goal is None:

                return False

            goal.status = "completed"

            goal.progress = 100.0

            goal.updated = time.time()

            goal.completed = time.time()

            return True

    # --------------------------------------------------
    # Fail Goal
    # --------------------------------------------------

    def fail_goal(self, goal_id):

        with self.lock:

            goal = self.goals.get(goal_id)

            if goal is None:

                return False

            goal.status = "failed"

            goal.updated = time.time()

            return True

    # --------------------------------------------------
    # Cancel Goal
    # --------------------------------------------------

    def cancel_goal(self, goal_id):

        with self.lock:

            goal = self.goals.get(goal_id)

            if goal is None:

                return False

            goal.status = "cancelled"

            goal.updated = time.time()

            return True

    # --------------------------------------------------
    # Remove Goal
    # --------------------------------------------------

    def remove_goal(self, goal_id):

        with self.lock:

            if goal_id in self.goals:

                del self.goals[goal_id]

                return True

            return False

    # --------------------------------------------------
    # List Goals
    # --------------------------------------------------

    def all_goals(self):

        return list(self.goals.values())

    # --------------------------------------------------

    def pending_goals(self):

        return [

            g

            for g in self.goals.values()

            if g.status == "pending"

        ]

    # --------------------------------------------------

    def completed_goals(self):

        return [

            g

            for g in self.goals.values()

            if g.status == "completed"

        ]

    # --------------------------------------------------
    # Search
    # --------------------------------------------------

    def search(self, keyword):

        keyword = keyword.lower()

        result = []

        for goal in self.goals.values():

            if keyword in goal.title.lower():

                result.append(goal)

                continue

            if keyword in goal.description.lower():

                result.append(goal)

                continue

        return result

    # --------------------------------------------------
    # Statistics
    # --------------------------------------------------

    def statistics(self):

        return {

            "total": len(self.goals),

            "pending":

                len(self.pending_goals()),

            "completed":

                len(self.completed_goals()),

            "failed":

                len(

                    [

                        g

                        for g in self.goals.values()

                        if g.status == "failed"

                    ]

                ),

            "cancelled":

                len(

                    [

                        g

                        for g in self.goals.values()

                        if g.status == "cancelled"

                    ]

                )

        }

    # --------------------------------------------------
    # Status
    # --------------------------------------------------

    def status(self):

        current = self.current_goal()

        return {

            "module": "GoalManager",

            "current":

                current.title if current else None,

            "statistics":

                self.statistics(),

            "ready": True

        }


goal_manager = GoalManager()