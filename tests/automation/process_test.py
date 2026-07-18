from automation.process import process_manager


print(
    "System Usage:"
)

print(
    process_manager.system_usage()
)


print(
    "\nChrome Running:"
)

print(
    process_manager.is_running(
        "chrome"
    )
)


print(
    "\nProcess List:"
)

for item in process_manager.list_processes(5):

    print(item)