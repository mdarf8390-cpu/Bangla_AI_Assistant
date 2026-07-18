from automation.engine import AutomationEngine


engine = AutomationEngine()


tests = [

    {
        "name": "YouTube",
        "command": {
            "action": "open",
            "app": "youtube"
        }
    },

    {
        "name": "Google",
        "command": {
            "action": "open",
            "app": "google"
        }
    },

    {
        "name": "Notepad",
        "command": {
            "action": "open",
            "app": "notepad"
        }
    },

    {
        "name": "VSCode",
        "command": {
            "action": "open",
            "app": "vscode"
        }
    },

    {
        "name": "WhatsApp",
        "command": {
            "action": "open",
            "app": "whatsapp"
        }
    },

    {
        "name": "Telegram",
        "command": {
            "action": "open",
            "app": "telegram"
        }
    },

    {
        "name": "Discord",
        "command": {
            "action": "open",
            "app": "discord"
        }
    },

    {
        "name": "Spotify",
        "command": {
            "action": "open",
            "app": "spotify"
        }
    }

]


for test in tests:

    print("\nTesting:", test["name"])

    result = engine.execute(
        test["command"]
    )

    print("Result:", result)