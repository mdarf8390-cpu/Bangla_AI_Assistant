from automation.ui_controller import ui_controller


print(
    "Screen:",
    ui_controller.screen_size()
)


print(
    "Moving Mouse..."
)

ui_controller.move_mouse(
    500,
    500
)


print(
    "Typing Test..."
)

ui_controller.type_text(
    "Hello AYESHA"
)