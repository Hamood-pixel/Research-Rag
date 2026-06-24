import os 
from fastapi import FastAPI, UploadFile, File #acts as chef working with backend 
import uvicorn #handles the server routing, acts as waiter

from langchain_ollama import OllamaLLM


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
