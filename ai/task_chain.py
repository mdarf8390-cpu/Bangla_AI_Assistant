# ai/task_chain.py

from dataclasses import dataclass, field
from typing import List, Callable
import uuid


# ==========================================
# Task
# ==========================================

@dataclass
class Task:

    name: str

    action: Callable = None

    priority: int = 5

    retry: int = 0

    completed: bool = False

    failed: bool = False

    id: str = field(

        default_factory=lambda: str(uuid.uuid4())[:8]

    )


# ==========================================
# Task Chain
# ==========================================

class TaskChain:

    def __init__(self):

        self.tasks: List[Task] = []


    # -------------------------------

    def add(

        self,

        name,

        action=None,

        priority=5,

        retry=0

    ):

        self.tasks.append(

            Task(

                name=name,

                action=action,

                priority=priority,

                retry=retry

            )

        )


    # -------------------------------

    def clear(self):

        self.tasks.clear()


    # -------------------------------

    def sort(self):

        self.tasks.sort(

            key=lambda x: x.priority

        )


    # -------------------------------

    def pending(self):

        return [

            t

            for t in self.tasks

            if not t.completed

        ]


    # -------------------------------

    def execute(self):

        self.sort()

        print()

        print("========== TASK CHAIN ==========")

        for task in self.tasks:

            print()

            print("▶", task.name)

            success = False

            attempts = 0

            while attempts <= task.retry:

                try:

                    if task.action:

                        task.action()

                    success = True

                    break

                except Exception as e:

                    attempts += 1

                    print(

                        "Retry",

                        attempts,

                        e

                    )

            if success:

                task.completed = True

                print("✔ Done")

            else:

                task.failed = True

                print("❌ Failed")

        print()

        print("===============================")


    # -------------------------------

    def progress(self):

        total = len(self.tasks)

        done = len(

            [

                t

                for t in self.tasks

                if t.completed

            ]

        )

        return done, total


    # -------------------------------

    def summary(self):

        print()

        print("===== SUMMARY =====")

        for t in self.tasks:

            status = "DONE"

            if t.failed:

                status = "FAILED"

            elif not t.completed:

                status = "WAITING"

            print(

                status,

                "-",

                t.name

            )

        print()
