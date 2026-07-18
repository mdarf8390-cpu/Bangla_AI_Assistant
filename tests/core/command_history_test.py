from core.command_history import command_history


record = command_history.add(
    "youtube open koro"
)


print(record)


command_history.update_status(
    record.id,
    "success",
    "YouTube opened"
)


print("\nALL HISTORY:")
print(
    command_history.get_all()
)


print("\nLAST:")
print(
    command_history.last()
)