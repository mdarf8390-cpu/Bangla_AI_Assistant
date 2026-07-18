from automation.clipboard import clipboard


print("Copy Test:")

clipboard.copy(
    "Hello AYESHA"
)


print(
    clipboard.paste()
)


print("\nClear Test:")

clipboard.clear()


print(
    clipboard.paste()
)