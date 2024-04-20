from config import configuration
import ollama
from retrival.processDocs import collections
from langchain.vectorstores import Chroma
import chromadb

import replicate
from transformers import AutoModelForCausalLM, AutoTokenizer

import os
from together import Together

client = Together(api_key=os.environ.get("TOGETHER_API_KEY"))

async def getTogetherResponse(
    sysPrompt, query, modelName=configuration["togetherModel"]
):
    response = client.chat.completions.create(
        model=modelName,
        messages=[{"role": "system", "content": sysPrompt},
                  {"role": "user", "content": query},
        ]
    )
    return response.choices[0].message.content


async def getTogetherReponseFunction(
    sysPrompt, query, tools, modelName=configuration["togetherModelTools"], 
):
    messages = [
        {"role": "system", "content": sysPrompt},
        {"role": "user", "content": query},
    ]
    response = client.chat.completions.create(
        model=modelName,
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )
    return response


tokenizer = AutoTokenizer.from_pretrained("Upstage/SOLAR-10.7B-Instruct-v1.0")

persistent_client = chromadb.PersistentClient()


def countTokens(text) : 
    tokens = tokenizer(text)
    return len(tokens['input_ids'])


def getOllamaResponse(
    prompt, modelName="", trackTime=True, model=configuration["localModel"]
):
    _out = ollama.generate(model=model, prompt=prompt)
    _response = _out["response"]
    return _response

def convSizeManager(convList, maxConvLength=configuration["maxConervationLength"]):
    # Check the size of the conversation
    # If the conversation is too long, remove the first element
    # This is to prevent the conversation from growing too large
    # and to keep the conversation manageable
    conversation = ""
    for i in range(len(convList)) :
        conversation += convList[i]
    n = len(convList)
    if (countTokens(conversation) > maxConvLength):
        newConversation = ""

        newLen = int(n * 0.6) 
        convList = convList[-newLen:]


    return convList



"""
async def getReplicateResponse(
    prompt, modelName="", deployment=configuration["replicateDeployment"], temperature=0.5, topP=0.96
):

    deployment = replicate.deployments.get(deployment)
    prediction = deployment.predictions.create(
        input={
            "prompt": prompt,
            "max_tokens": configuration["maxTokensOut"],
            "temperature": temperature,
            "top_p": topP,
        },
        stream=True,
    )
    #output = prediction.wait()
    await prediction.async_wait()
    #output = prediction.output()
    #print(prediction)
    out = ""
    for item in prediction.output:
        # item is generator object -> can be streamed to UI
        out += str(item)
    return out
"""

def fetchContext(query, singleCollection = False, collectionName = "") : 

    # Start with empty string & query all collections
    context = ""
    maxDocsIn = 3
    
    if singleCollection : 
        _chromaCollection = Chroma(
            client = persistent_client,
            collection_name = collectionName,
            embedding_function = configuration["embedding"]
        )
        _retriveDocs = _chromaCollection.similarity_search(query)

        if len(_retriveDocs) > 0 :
            context += "Retrived from " + collections[collectionName]['description'] + "\n"
            n = min(len(_retriveDocs), maxDocsIn)
            for i in range(n) : 
                context += _retriveDocs[i].page_content + "\n"
        return context

    for collection in collections.keys() : 
        
        _chromaCollection = Chroma(
            client = persistent_client,
            collection_name = collections[collection]['collection_name'],
            embedding_function = configuration["embedding"]
        )
        _retriveDocs = _chromaCollection.similarity_search(query)

        if len(_retriveDocs) > 0 :
            context += "Retrived from " + collections[collection]['description'] + "\n"
            n = min(len(_retriveDocs), maxDocsIn)
            for i in range(n) : 
                context += _retriveDocs[i].page_content + "\n"

    if configuration["enableLogging"] : 
        print("Fetched Context : " + context)

    return context
    