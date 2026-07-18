from automation.explorer import explorer


print(
    "Explorer Test:"
)


print(
    explorer.open_explorer()
)


print(
    "Current Folder Exists:",
    explorer.exists(".")
)


print(
    "Create Test Folder:"
)


print(
    explorer.create_folder(
        "AYESHA_TEST_FOLDER"
    )
)