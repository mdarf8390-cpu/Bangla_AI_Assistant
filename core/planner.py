from dataclasses import dataclass, field
from enum import Enum
import uuid
import time


class TaskStatus(str, Enum):

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"



class Priority(int, Enum):

    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4



@dataclass
class Task:

    name: str

    arguments: dict = field(default_factory=dict)

    priority: Priority = Priority.NORMAL

    depends_on: list = field(default_factory=list)

    retries: int = 2

    id: str = field(
        default_factory=lambda: str(uuid.uuid4())
    )

    status: TaskStatus = TaskStatus.PENDING

    created: float = field(
        default_factory=time.time
    )



@dataclass
class Plan:

    tasks: list = field(default_factory=list)

    id: str = field(
        default_factory=lambda: str(uuid.uuid4())
    )

    created: float = field(
        default_factory=time.time
    )



class Planner:


    def create_plan(self, action):

        plan = Plan()


        # =====================================
        # Normalize Action
        # =====================================

        act = action.get(
            "action",
            ""
        )


        mapping = {

            "chrome":
                "open_chrome",

            "google":
                "open_google",

            "youtube":
                "open_youtube",

            "open_browser":
                "open_youtube",

            "youtube_close":
                "close_youtube"

        }



        # =====================================
        # Browser Tasks
        # =====================================

        if act in mapping:


            plan.tasks.append(

                Task(

                    name=mapping[act],

                    arguments={

                        "query":
                        action.get("query")

                        or action.get("params")

                    }

                )

            )



        # =====================================
        # Skill System
        # =====================================

        elif act in {

            "open",
            "close",
            "activate",
            "search",
            "write",
            "play"

        }:


            plan.tasks.append(

                Task(

                    name="skill",

                    arguments={

                        "command": action

                    }

                )

            )



        # =====================================
        # AI Answer
        # =====================================

        elif act == "chat":


            plan.tasks.append(

                Task(

                    name="answer",

                    arguments={

                        "text":
                        action.get(
                            "answer",
                            ""
                        )

                    }

                )

            )



        # =====================================
        # Unknown
        # =====================================

        else:


            plan.tasks.append(

                Task(

                    name="unknown",

                    arguments={

                        "raw": action

                    }

                )

            )


        return plan



planner = Planner()