

localLLMPrompt = """<s> ### System:
{initialInstruction}

Note the below information about Yearn Finance which can assist you in answering the users question 
{context}

Use the above information to assist the user in responding to their question. (Note that any APY & TVL data provided above is updated every 24 hours & can be considered up to date)

Log of interaction 
{conversation}

Above is a log of the conversation you have had with the user - do not repeat yourself & help use this along with the additional context on Yearn to assist the user in their query.
{endInstruction}

### User:
{query}

### Assistant:
"""