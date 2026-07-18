# ai/goal_manager.py

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
import uuid


# ==========================================
# Goal
# ==========================================

@dataclass
class Goal:

    id: str = field(
        default_factory=lambda: str(uuid.uuid4())[:8]
    )

    title: str = ""

    description: str = ""

    priority: int = 5

    parent: Optional[str] = None

    children: List[str] = field(default_factory=list)

    status: str = "pending"

    progress: int = 0

    created = datetime.now()

    completed = None

    data: dict = field(default_factory=dict)


# ==========================================
# Goal Manager
# ==========================================

class GoalManager:

    def __init__(self):

        self.goals = {}

    # ------------------------------

    # Create Goal

    # ------------------------------

    def create(

        self,

        title,

        description="",

        priority=5,

        parent=None,

        data=None

    ):

        goal = Goal(

            title=title,

            description=description,

            priority=priority,

            parent=parent,

            data=data or {}

        )

        self.goals[goal.id] = goal

        if parent:

            if parent in self.goals:

                self.goals[parent].children.append(

                    goal.id

                )

        return goal.id

    # ------------------------------

    # Find

    # ------------------------------

    def get(self, goal_id):

        return self.goals.get(goal_id)

    # ------------------------------

    # All

    # ------------------------------

    def all(self):

        return list(self.goals.values())

    # ------------------------------

    # Update Status

    # ------------------------------

    def set_status(

        self,

        goal_id,

        status

    ):

        goal = self.get(goal_id)

        if not goal:

            return

        goal.status = status

        if status == "completed":

            goal.progress = 100

            goal.completed = datetime.now()

    # ------------------------------

    # Progress

    # ------------------------------

    def update_progress(

        self,

        goal_id,

        progress

    ):

        goal = self.get(goal_id)

        if not goal:

            return

        goal.progress = progress

    # ------------------------------

    # Remove

    # ------------------------------

    def remove(

        self,

        goal_id

    ):

        if goal_id in self.goals:

            del self.goals[goal_id]

    # ------------------------------

    # Pending

    # ------------------------------

    def pending(self):

        return [

            g

            for g in self.goals.values()

            if g.status == "pending"

        ]

    # ------------------------------

    # Running

    # ------------------------------

    def running(self):

        return [

            g

            for g in self.goals.values()

            if g.status == "running"

        ]

    # ------------------------------

    # Completed

    # ------------------------------

    def completed(self):

        return [

            g

            for g in self.goals.values()

            if g.status == "completed"

        ]

    # ------------------------------

    # Highest Priority

    # ------------------------------

    def next_goal(self):

        pending = self.pending()

        if not pending:

            return None

        pending.sort(

            key=lambda g: g.priority

        )

        return pending[0]

    # ------------------------------

    # Print

    # ------------------------------

    def summary(self):

        print()

        print("========== GOALS ==========")

        for goal in self.goals.values():

            print(

                goal.id,

                "|",

                goal.title,

                "|",

                goal.status,

                "|",

                str(goal.progress) + "%"

            )

        print()
