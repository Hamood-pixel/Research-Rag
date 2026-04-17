from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def process_pdf(file_path: str): #defining a function that converts a pdf to string and then make chunks, these chunks would be sent to vector DB
    loader = PyPDFLoader(file_path) #load the pdf file 
    pages = loader.load() #using .load() since this not only saves the raw text but also the metadata (citation feature later)
    
    full_text = " ".join([page.page_content for page in pages]) #combined the content of all the pages into a single, massive string 

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000 ,
        chunk_overlap = 100,
        length_function = len
    ) #initializing the text_splitter 

    chunks = text_splitter.split_text(full_text) #takes in the fulltext created using the join method above and then use split_text using the method text_splitter defined above
    return chunks