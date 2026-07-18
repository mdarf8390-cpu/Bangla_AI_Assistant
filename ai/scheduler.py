# ai/scheduler.py

from datetime import datetime, timedelta
import threading
import time
import uuid


class ScheduledTask:

    def __init__(
        self,
        task,
        run_at,
        callback=None,
        repeat=False,
        interval=None
    ):

        self.id = str(uuid.uuid4())[:8]

        self.task = task

        self.run_at = run_at

        self.callback = callback

        self.repeat = repeat

        self.interval = interval

        self.completed = False

        self.created = datetime.now()

    def should_run(self):

        return datetime.now() >= self.run_at

    def execute(self):

        if self.callback:

            self.callback(self.task)

        self.completed = True

        if self.repeat and self.interval:

            self.completed = False

            self.run_at = datetime.now() + timedelta(
                seconds=self.interval
            )


class Scheduler:

    def __init__(self):

        self.tasks = []

        self.running = False

        self.thread = None

    # --------------------------

    # Add Task

    # --------------------------

    def add_task(

        self,

        task,

        delay=None,

        run_at=None,

        callback=None,

        repeat=False,

        interval=None

    ):

        if run_at is None:

            run_at = datetime.now() + timedelta(

                seconds=delay or 0

            )

        item = ScheduledTask(

            task=task,

            run_at=run_at,

            callback=callback,

            repeat=repeat,

            interval=interval

        )

        self.tasks.append(item)

        return item.id

    # --------------------------

    # Remove

    # --------------------------

    def remove_task(self, task_id):

        self.tasks = [

            t

            for t in self.tasks

            if t.id != task_id

        ]

    # --------------------------

    # List

    # --------------------------

    def list_tasks(self):

        return [

            {

                "id": t.id,

                "task": t.task,

                "time": t.run_at,

                "repeat": t.repeat

            }

            for t in self.tasks

        ]

    # --------------------------

    # Clear

    # --------------------------

    def clear(self):

        self.tasks.clear()

    # --------------------------

    # Loop

    # --------------------------

    def run(self):

        self.running = True

        while self.running:

            for task in list(self.tasks):

                if task.should_run():

                    task.execute()

                    if not task.repeat:

                        self.tasks.remove(task)

            time.sleep(1)

    # --------------------------

    # Start

    # --------------------------

    def start(self):

        if self.thread:

            return

        self.thread = threading.Thread(

            target=self.run,

            daemon=True

        )

        self.thread.start()

    # --------------------------

    # Stop

    # --------------------------

    def stop(self):

        self.running = False

        self.thread = None

    # --------------------------

    # Bangla Time Parser

    # --------------------------

    def parse_time(

        self,

        text

    ):

        text = text.lower()

        if "৫ মিনিট" in text:

            return datetime.now() + timedelta(

                minutes=5

            )

        if "১০ মিনিট" in text:

            return datetime.now() + timedelta(

                minutes=10

            )

        if "১৫ মিনিট" in text:

            return datetime.now() + timedelta(

                minutes=15

            )

        if "৩০ মিনিট" in text:

            return datetime.now() + timedelta(

                minutes=30

            )

        if "১ ঘণ্টা" in text:

            return datetime.now() + timedelta(

                hours=1

            )

        return None