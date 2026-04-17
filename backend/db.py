import os 
from langchain_community.vectorstores import Chroma 
from langchain_huggingface import HuggingFaceEmbeddings

db_directory = os.path.join(os.path.dirname(__file__), "chroma_db") #place where the database would exist 

embeddings = HuggingFaceEmbeddings(model_name = "all-MiniLM-L6-v2")

def create_embeddings(chunks, db_path = db_directory):
    """
    Takes in chunks, create vector embeddings and stores them in the vector database whose path is defined in the arguments
    """  
    return 




