from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain.vectorstores import Chroma
from langchain.docstore.document import Document

### Which collections to load & what Chroma collection to save them to 
collections = {
    'articles' : {
        'collection_name' : 'articles',
        'description' : 'Articles about Yearn Finance',
        'directory' : './training-data/articles',
        'glob' : '*.md',
    },
    'docs' : {
        'collection_name' : 'docs',
        'description' : 'Yearn documentation',
        'directory' : './training-data/docs',
        'glob' : '*.md',
    },
    'yips' : {
        'collection_name' : 'yips',
        'description' : 'Yearn Improvement Proposals',
        'directory' : './training-data/YIPS',
        'glob' : '*.md',
    },
}

# Option to load from a directory of PDFs & get text to feed into DB 
def processDocs(embedding, persist_directory = 'chroma'  ) : 

    for collection in collections.keys() : 
        dir = collections[collection]['directory']
        collection_name = collections[collection]['collection_name']

        # loop through subdirectories & load all .md files

        

        loader = DirectoryLoader(dir, glob="**/*.md", loader_cls=TextLoader)
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        texts = text_splitter.split_documents(documents)

        if (len(texts) > 0) :
            vectordb = Chroma.from_documents(documents=texts, 
                                            embedding=embedding,
                                            collection_name = collection_name,
                                            persist_directory=persist_directory,
                                            )

