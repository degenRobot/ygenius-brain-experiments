import requests
from langchain.vectorstores import Chroma
from langchain.docstore.document import Document

from config import embedding

# Note should delete old data before running this - otherwise won't have most up to date APY data 

def convertPoolToDoc(pool) : 
    content = ""
    content += "Current APY for Yearn Vault for " + pool['symbol'] + " on the chain " + pool['chain'] +  " is " + str(pool['apy']) + "% \n"
    content += "The pool has a total value locked (in USD value) of " + str(pool['tvlUsd']) + " \n"

    doc = Document(page_content=content)
    doc.metadata = {
        'source' : 'defillama',
        'type' : 'public'
    }
    return doc

def getApyData() :
    # API endpoint
    url = 'https://yields.llama.fi/pools'

    # Perform the GET request
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()

        # Filter pools where project is 'yearn-finance'
        
        #print(data.keys())
        data = data['data']
        #print(data[0])
        yearnPools = []
        docs = []
        for pool in data : 
            if pool['project'] == 'yearn-finance' :
                yearnPools.append(pool)
                doc = convertPoolToDoc(pool)
                docs.append(doc)

        # Save the documents to the Chroma collection
        vectordb = Chroma.from_documents(documents=docs, 
                                        embedding=embedding,
                                        collection_name = 'apyData',
                                        persist_directory='chroma',
                                        )


