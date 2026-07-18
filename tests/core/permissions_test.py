from core.permissions import permissions


tests = [

    "browser.open",

    "file.delete",

    "system.shutdown",

    "unknown.action"

]


for action in tests:

    print(
        action,
        "=>",
        permissions.check(action)
    )


print("\nGrant file.delete")

permissions.grant(
    "file.delete"
)


print(
    "file.delete =>",
    permissions.check("file.delete")
)