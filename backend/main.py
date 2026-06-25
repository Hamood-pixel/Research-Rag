import os 
from fastapi import FastAPI, UploadFile, File #acts as chef working with backend 
import uvicorn #handles the server routing, acts as waiter

from langchain_ollama import OllamaLLM
from db import get_retriever  #retriever is the function we created in db.py to get the retriever object which would be used to fetch relevant chunks
from langchain_core.prompts import ChatPromptTemplate

#importing the functions from the files we made in backend
from processor import process_pdf
from db import create_embeddings, get_retriever

app = FastAPI() #initialize the fastapi app

UPLOAD_DIRECTORY = os.path.join(os.path.dirname(__file__), "uploads") #place where the uploaded files would be stored
os.makedirs(UPLOAD_DIRECTORY, exist_ok = True) #create the uploads directory if it doesn't exist

@app.get("/")
def home():
    return {"status": "online", "message": "Research Rag is up and running!"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)
    
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
        
    try:
        print(f"--- Processing PDF: {file.filename} ---")
        chunks = process_pdf(file_path)
        print(f"Successfully extracted {len(chunks)} text chunks from PDF.") # <-- Add this

        if len(chunks) == 0:
            print("WARNING: Zero text chunks extracted! Check your PDF text layer.")

        print("Creating embeddings and writing to ChromaDB...")
        create_embeddings(chunks)
        print("ChromaDB successfully updated!") # <-- Add this

        return {"status" : "success", "message": f"Successfully processed {file.filename}", "chunks created": len(chunks)}
    except Exception as e:
        print(f"CRITICAL UPLOAD ERROR: {str(e)}") # <-- Add this
        return {"Status" : "error", "message" : str(e)}
    finally:
        if os.path.exists(file_path):   
            os.remove(file_path)

@app.post("/query") #API endpoint to handle user queries, this would be called by the frontend to talk to the backend and get answers from the LLM
async def query_paper(payload: dict): #payload is the actual data to be sent to the LLM
    """
    Takes user query, converts it to embeddings, retrieves relevant chunks and generate response using LLM. 
    """
    user_question = payload.get("question") 

    if not user_question: 
        return {"status": "error", "message": "No question provided."}
    
    try: 
        retriever = get_retriever() #get the retriever object from the db.py file
        relevant_chunks = retriever.invoke(user_question)
        
        #combine the relevant chunks into a single string to send to the LLM
        context = " ".join([chunk.page_content for chunk in relevant_chunks])

        #create a prompt for the LLM 
        prompt_template = ChatPromptTemplate.from_messages([
        ("system", (
         "You are an expert research assistant analyze technical documents.\n\n"
         "Answer the user's question using ONLY the provided context snippets below. "
         "Be thorough, objective, and intellectually flexible—if the context describes "
         "processes, tools, or analysis methods, use them to infer higher-level concepts "
         "like methodology or objectives even if the exact keyword isn't explicitly used.\n\n"
         "If the answer genuinely cannot be found or inferred from the context, "
         "say 'I cannot find that in the document.'\n\n"
         "Context:\n{context}"
        )),
         ("human", "{question}")
      ])

        #initiliaze LLM model 
        llm = OllamaLLM(model = "llama3")

        #run model on GPU
        # FIXED: Connected prompt_template and llm into a processing chain, then passed variables via dictionary input
        rag_chain = prompt_template | llm
        response = rag_chain.invoke({"context": context, "question": user_question})

        return {"status": "success", "answer": response}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    
if __name__ == "__main__":
    uvicorn.run(app, host = "0.0.0.0", port = 8000) #run the app on localhost:8000