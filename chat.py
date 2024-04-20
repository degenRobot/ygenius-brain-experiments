from helpers import *
from chatMechanics.promptBuilder import localLLMPrompt, sysPrompt
from retrival.retrivalFunctions import tools
import asyncio
import json

retrivalPrompt = configuration["retrivalPrompt"]

initialInstruction = configuration["initialInstruction"]
endInstruction = configuration["finalInstruction"]

async def chat(): 

    print("Start chatting - ask questions about Yearn Finance")
    convList = []
    conversation = ""
    while True : 

        print("Ask a question about Yearn Finance ")

        query = input()

        ### get query information
        response = await getTogetherReponseFunction(
            retrivalPrompt,
            query,
            tools=tools,
            modelName=configuration["togetherModelTools"]
        )

        tool_calls = response.choices[0].message.tool_calls

        if (tool_calls) : 
            args = json.loads(tool_calls[0].function.arguments)
            collection = args["collection"]
            query = args["query"]

            context = fetchContext(query, singleCollection=True, collectionName=collection)
            print(context)
        else : 
            context = fetchContext(query)


        print("------------------------------------")

        # Get context from the documents

        # Get response from model 
        if configuration["useOllama"] :
            prompt = localLLMPrompt.format(
                char="Assistant", 
                context=context, 
                conversation=conversation, 
                query = query, 
                initialInstruction=initialInstruction,
                endInstruction=endInstruction
            )
        else :
            prompt = sysPrompt.format(
            context=context, 
            conversation=conversation, 
            query = query, 
            initialInstruction=initialInstruction,
            endInstruction=endInstruction
        )
            
        if configuration["useOllama"] :

            response = getOllamaResponse(prompt)
        else : 
            response = await getTogetherResponse(prompt, query)


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
