retrivalFunction ={
    "name": "retrival", ## Function name referenced in function_call
    "description": "Determining which vector database to search to pull additional context in required to answer a users question about Yearn Finance", ## Function description
    "parameters": {
        "type": "object",
        "properties": { ## Structure of the properties you expect to return as an object
            "query": {
                "title": "query", 
                "description": """The query used to search the DB for relevant context 
note this is used to search for whichever string best answers this question. 
Queries should be short and to the point and formatted to clearly focus on what information is needed""", 
            "type": "string"},
            "collection": {
                "title": "collection",
                "description": """You may search the following collections (this is the collection you want to search for context)
articles (this collection contains various articles about Yearn Finance - this includes information about the project, the team, and other relevant information)
docs (this collection contains documentation about Yearn Finance with more detailed technical information about the project and how it works)
yips (this collection contain information about Yearn Improvement Proposals - these are proposals for changes to the Yearn ecosystem and how it operates)                
apyData (this is collection provides APY data for various Yearn products - primarily used if users are asking about the APY of a specific product)
""",
                "type": "string",
            },
        },
    "required": ["query", "collection"]
    }
}

tools = [
  {
    "type": "function",
    "function": retrivalFunction
    }    
]