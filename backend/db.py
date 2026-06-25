import os 
from langchain_community.vectorstores import Chroma 
from langchain_huggingface import HuggingFaceEmbeddings

db_directory = os.path.join(os.path.dirname(__file__), "chroma_db") #place where the database would exist 

embeddings = HuggingFaceEmbeddings(model_name = "all-MiniLM-L6-v2")

def create_embeddings(chunks, db_path = db_directory):
    """
    Takes in chunks, create vector embeddings and stores them in the vector database whose path is defined in the arguments
    """  
    vector_db = Chroma.from_documents(documents = chunks, embedding = embeddings, persist_directory = db_path) #use chroma class to create vector embeddings

    return vector_db

def get_retriever(db_path = db_directory):
    """
    Takes in the path to the vector database and returns a retriever object that can be used to retrieve relevant chunks based on a query
    """
    vector_db = Chroma(persist_directory = db_path, embedding_function = embeddings)

    return vector_db.as_retriever(search_kwargs = {"k": 4}) #returns 4 relevant chunks based on the query 




