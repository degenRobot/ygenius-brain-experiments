from helpers import *
from chatMechanics.promptBuilder import localLLMPrompt
import asyncio

initialInstruction = configuration["initialInstruction"]
endInstruction = configuration["finalInstruction"]

async def chat(): 

    print("Start chatting - ask questions about Yearn Finance")
    convList = []
    conversation = ""
    while True : 

        query = input("Ask a question: ")

        # Get context from the documents
        context = fetchContext(query)

        # Get response from model 
        prompt = localLLMPrompt.format(
            char="Assistant", 
            context=context, 
            conversation=conversation, 
            query = query, 
            initialInstruction=initialInstruction,
            endInstruction=endInstruction
        )
        if configuration["useOllama"] :

            response = getOllamaResponse(prompt)
        else : 
            response = await getReplicateResponse(prompt)


        print(response)

        
        convList.append("User: " + query + "\n")
        convList.append("Assistant: " + response + "\n")
        convList = convSizeManager(convList)
        conversation = ""
        for i in range(len(convList)) :
            conversation += convList[i]
        #conversation = convList.join("")

        # should have some logic to manage 
loop = asyncio.get_event_loop()

# Use the event loop to run _testChat
loop.run_until_complete(chat())
