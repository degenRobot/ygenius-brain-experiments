from helpers import *
from chatMechanics.promptBuilder import localLLMPrompt
import asyncio

async def chat(): 

    print("Start chatting - ask questions about Yearn Finance")
    conversation = ""
    while True : 

        query = input("Ask a question: ")

        # Get context from the documents
        context = fetchContext(query)

        # Get response from model 
        prompt = localLLMPrompt.format(char="Assistant", context=context, conversation=conversation, query = query)
        if configuration["useOllama"] :

            response = getOllamaResponse(prompt)
        else : 
            response = await getReplicateResponse(prompt, )


        print(response)

        conversation += "User: " + query + "\n"
        conversation += "Assistant: " + response + "\n"

        # should have some logic to manage 
loop = asyncio.get_event_loop()

# Use the event loop to run _testChat
loop.run_until_complete(chat())
