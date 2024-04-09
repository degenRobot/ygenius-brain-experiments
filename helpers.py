import inquirer
import re

from config import configuration
import ollama
from retrival.processDocs import collections
from langchain.vectorstores import Chroma
import chromadb

import replicate
from transformers import AutoModelForCausalLM, AutoTokenizer
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


def fetchContext(query) : 

    # Start with empty string & query all collections
    context = ""
    maxDocsIn = 3
    
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
    