from ai.task_chain import TaskChain


chain = TaskChain()


def open_chrome():

    print("Chrome Opened")


def open_google():

    print("Google Opened")


def search():

    print("Searching Python")


chain.add(

    "Open Chrome",

    action=open_chrome,

    priority=1

)

chain.add(

    "Open Google",

    action=open_google,

    priority=2

)

chain.add(

    "Search Python",

    action=search,

    priority=3

)


chain.execute()

print()

print(chain.progress())

chain.summary()