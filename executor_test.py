from core.planner import Planner
from core.executor import Executor


planner = Planner()
executor = Executor()


data = {
    "action": "youtube",
    "query": "gta 6 trailer"
}


plan = planner.create_plan(data)


print("PLAN:")
print(plan)


result = executor.execute(plan)


print("RESULT:")
print(result)