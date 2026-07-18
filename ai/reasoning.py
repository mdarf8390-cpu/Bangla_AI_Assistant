from dataclasses import dataclass
from typing import List


@dataclass
class Task:
    step: int
    action: str
    status: str = "Pending"


class Reasoning:

    def __init__(self):
        self.tasks: List[Task] = []

    def clear(self):
        self.tasks.clear()

    def plan(self, command: str):

        self.clear()

        cmd = command.lower()

        # -------- YouTube --------

        if "youtube" in cmd:

            self.tasks.append(Task(1, "Open Chrome"))
            self.tasks.append(Task(2, "Open YouTube"))
            self.tasks.append(Task(3, "Search requested video"))

        # -------- Google --------

        elif "google" in cmd:

            self.tasks.append(Task(1, "Open Browser"))
            self.tasks.append(Task(2, "Open Google"))
            self.tasks.append(Task(3, "Search"))

        # -------- VS Code --------

        elif "vs code" in cmd:

            self.tasks.append(Task(1, "Open VS Code"))

        # -------- Screenshot --------

        elif "screenshot" in cmd:

            self.tasks.append(Task(1, "Take Screenshot"))

        else:

            self.tasks.append(Task(1, "Think"))
            self.tasks.append(Task(2, "Generate Response"))

        return self.tasks


if __name__ == "__main__":

    ai = Reasoning()

    tasks = ai.plan(
        "Open YouTube and search Python tutorial"
    )

    for task in tasks:

        print(f"{task.step}. {task.action} [{task.status}]")