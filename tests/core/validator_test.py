from core.validator import validator


tests = [

    "youtube open koro",

    "",

    "a",

    "delete system32",

    "open calculator"

]


for command in tests:

    result, message = validator.validate(
        command
    )

    print(
        command,
        "=>",
        result,
        "|",
        message
    )