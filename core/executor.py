from automation.browser import BrowserAutomation
from automation.engine import AutomationEngine


class Executor:

    def __init__(self):

        self.browser = BrowserAutomation()

        self.engine = AutomationEngine()


    def execute(self, plan):

        # ✅ ADD: Plan object support - plan.tasks থেকে extract করবে
        if hasattr(plan, 'tasks'):
            steps = [
                {
                    "task": task.name,
                    "query": task.arguments.get('query'),
                    "command": task.arguments.get('command'),
                    "text": task.arguments.get('text'),
                    "raw": task.arguments.get('raw')
                }
                for task in plan.tasks
            ]
        else:
            steps = plan

        results = []


        for step in steps:

            task = step.get("task")


            # ==========================================
            # Legacy Browser Commands
            # ==========================================

            if task == "open_youtube":

                query = step.get("query")

                self.browser.open_youtube(query)

                results.append(
                    f"YouTube opened: {query}"
                )


            elif task == "close_youtube":

                self.browser.close_youtube()

                results.append(
                    "YouTube closed"
                )


            elif task == "open_google":

                query = step.get("query")

                self.browser.open_google(query)

                results.append(
                    f"Google searched: {query}"
                )


            elif task == "open_chrome":

                self.browser.open_chrome()

                results.append(
                    "Chrome opened"
                )


            # ==========================================
            # New Skill System
            # ==========================================

            elif task == "skill":

                command = step.get("command")

                ok = self.engine.execute(command)

                if ok:

                    results.append(
                        f"Done : {command.get('action')} -> {command.get('app')}"
                    )

                else:

                    results.append(
                        f"Failed : {command.get('action')} -> {command.get('app')}"
                    )


            # ==========================================
            # AI Answer
            # ==========================================

            elif task == "answer":

                results.append(
                    step.get("text")
                )


            # ==========================================
            # Unknown
            # ==========================================

            else:

                results.append(
                    "Unknown task"
                )


        return results
