import os 
from fastapi import FastAPI, UploadFile, File #acts as chef working with backend 
import uvicorn #handles the server routing, acts as waiter

from langchain_ollama import OllamaLLM
from db import get_retriever  #retriever is the function we created in db.py to get the retriever object which would be used to fetch relevant chunks

#importing the functions from the files we made in backend
from processor import process_pdf
from db import create_embeddings, get_retriever

app = FastAPI() #initialize the fastapi app

UPLOAD_DIRECTORY = os.path.join(os.path.dirname(__file__), "uploads") #place where the uploaded files would be stored
os.makedirs(UPLOAD_DIRECTORY, exist_ok = True) #create the uploads directory if it doesn't exist

@app.get("/")
def home():
    return {"status: online", "message: Research Rag is up and running!"}

@app.post("/upload") #API endpoints to upload the file, this would be called by the frontend when the user uploads a file
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIRECTORY, file.filename) #create the file path where the uploaded file would be stored
    
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())#write the uploaded file to the file path created above
    try:
        chunks = process_pdf(file_path)
        create_embeddings(chunks) #create embeddings for the chunks and store them in the vector database

        return {"status" : "success", "message": f"Sucessfully processed {file.filename}", "chunks created": len(chunks)}
    except Exception as e:
        return {"Status" : "error", "message" : str(e)}
    finally:
        if os.path.exists(file_path):   
            os.remove(file_path) #delete the uploaded file after processing to prevent ssd overloading 

if __name__ == "__main__":
    uvicorn.run(app, host = "0.0.0.0", port = 8000) #run the app on localhost:8000

@app.post("/query") #API endpoint to handle user queries, this would be called by the frontend to talk to the backend and get answers from the LLM
async def query_paper(payload: dict): #payload is the actual data to be sent to the LLM
    """
    Takes user query, converts it to embeddings, retrieves relevant chunks and generate response using LLM. 
    """
    user_question = payload.get("question") 

    if not user_question: 
        return {"status": "error", "message": "No question provided."}
    
    try: 
        retriver = get_retriever() #get the retriever object from the db.py file
        relevant_chunks = get_retriever.invoke(user_question)
        
        #combine the relevant chunks into a single string to send to the LLM
        context = " ".join([chunk.page_content for chunk in relevant_chunks])

        #create a prompt for the LLM 
        prompt = f"You are a Research Assistant. Answer the User's question using ONLY the provided context from the research paper. If the answer is not in the context or you dont know the answer, say 'I don't know'. Donot make things up. \n\nContext: {context}\n\nUser's Question: {user_question}\n\nAnswer:"

        #initiliaze LLM model 
        llm = OllamaLLM(model = "llama3")

        #run model on GPU
        response = llm.invoke(prompt)

        return {"status": "success", "answer": response}
    except Exception as e:
        {"status": "error", "message": str(e)}
        