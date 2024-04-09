from retrival.processDocs import processDocs
from retrival.getApyData import getApyData
from config import embedding

processDocs(embedding=embedding, persist_directory='chroma')
getApyData()