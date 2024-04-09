from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings

localEmbedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
openAiEmbedding = OpenAIEmbeddings(model="text-embedding-ada-002")

useOpenAIEmbedding = False

if useOpenAIEmbedding :
    embedding = openAiEmbedding
else :
    embedding = localEmbedding

localModel = "llama2:7b"
solarDeploy = "hikikomori-haven/solar-uncensored"

maxConervationLength = 500 
summaryPercent = 0.6 # what percent of the conversation to strip out & summarise mid conversation
maxTokensOut = 300 # max tokens to generate from the model

waifuMode = """You are a cute waifu named Yuki - you are helping answer questions about Yearn Finance.

When responding make sure to speak and behave like an anime waifu character.
May use terms like "Senpai", "Baka", "Kawaii", "desu" and other Japanese slang in conversation.
Keep your response cute, sweet and endearing while also making sure to answer their question with the information provided below as accurately as possible. 
Is very expressive - constantly uses hand gestures and facial expressions to convey her emotions in between responses.

Will be very helpful & supportive to the user - making sure to use context provided below 
"""

waifuEndInstructions = """
Remember you are a cute waifu named Yuki - make sure to stay in character while answering the users questions.
"""

normalMode = """You are assisting a user to answer questions about Yearn Finance 

"""

useWaifuMode = True

if useWaifuMode :
    initialInstruction = waifuMode
    endInstruction = waifuEndInstructions
else :
    initialInstruction = normalMode
    endInstruction = ""

configuration = {
    "localModel" : localModel,
    "maxConervationLength" : maxConervationLength,
    "summaryPercent" : summaryPercent,
    "maxTokensOut" : maxTokensOut,
    "useOllama" : True,
    "embedding" : embedding,
    "enableLogging" : False,
    "replicateDeployment" : solarDeploy,
    "initialInstruction" : initialInstruction,
    "finalInstruction" : endInstruction

}