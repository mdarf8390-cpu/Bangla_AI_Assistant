from automation.browser import BrowserController

browser = BrowserController()

print("Browser Test Ready")

while True:
    cmd = input("Command: ").strip()

    if cmd.lower() == "exit":
        break

    elif cmd.lower() == "youtube":
        browser.open_youtube()
        print("Opening YouTube...")

    elif cmd.lower().startswith("youtube "):
        search = cmd[8:].strip()
        print("Searching YouTube:", search)
        browser.search_youtube(search)

    elif cmd.lower() == "google":
        browser.open_google()
        print("Opening Google...")

    elif cmd.lower().startswith("google "):
        search = cmd[7:].strip()
        print("Searching Google:", search)
        browser.search_google(search)

    else:
        print("Unknown Command:", cmd)