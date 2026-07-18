# ai/planner.py

class Planner:


    def __init__(self):

        self.tasks = []


    def create_plan(self, decision):

        plan = {

            "action": decision.action,

            "app": decision.app,

            "query": decision.query,

            "text": decision.text,

            "target": decision.target

        }


        self.tasks.append(plan)


        return plan



    def get_tasks(self):

        return self.tasks



    def clear(self):

        self.tasks = []