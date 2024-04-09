from retrival.processDocs import processDocs
from config import embedding

processDocs(embedding=embedding, persist_directory='chroma')
