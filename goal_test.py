from core.goal_manager import goal_manager

goal = goal_manager.create_goal(
    "Build AYESHA",
    "Finish production AI"
)

goal_manager.update_progress(
    goal.id,
    45
)

print(goal_manager.status())

goal_manager.complete_goal(goal.id)

print(goal_manager.statistics())