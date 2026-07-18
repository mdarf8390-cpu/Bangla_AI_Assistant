from core.context_manager import context

context.set_goal("Build AYESHA")

context.set_task("Create Memory")

context.set_user_input("Open Chrome")

context.set_ai_response("Opening Chrome")

context.save()

print(context.status())

print()

print(context.prompt_context())

print()

print(context.build_context())