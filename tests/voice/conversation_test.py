from ai.conversation import ConversationMemory

memory = ConversationMemory()


memory.remember({

    "action": "open",

    "app": "youtube"

})

print(memory.get_last_app())



cmd = {

    "action": "search",

    "query": "cats"

}

cmd = memory.resolve_context(cmd)

print(cmd)