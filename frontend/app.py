import streamlit as st 
import requests 

st.set_page_config(page_title="Research Rag", layout= "wide")

st.title("Research Paper AI Assistant")
st.markdown("----")

#sidebar layout for document upload

with st.sidebar:
    st.header("Upload your research paper")

    uploaded_file = st.file_uploader("Choose a research paper (PDF)" , type = "pdf")

    #create the trigger button 
    if st.button("Process Document"):
        if uploaded_file:
            with st.spinner("Processing the document..."):
              try:
                  files =  {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                  #make a call to the backend API to process the document 
                  response = requests.post("http://localhost:8000/upload", files=files)
                  if response.status_code == 200:
                      st.success(f"{uploaded_file.name} processed successfully!")
                  else:
                      st.error(f"Failed to process the document. Backend error: {response.status_code}")
              except Exception as e:
                   st.error(f"Could not connect to backend : {str(e)}")
        else:
            st.warning("Please upload a research paper before processing.")
    # Main chat interface 

    st.subheader("Ask questions about your research paper")
    user_query = st.chat_input("e.g., What is the main methodology used in this paper?")

    if user_query:
        with st.chat_message("user"):
            st.markdown(user_query)
        with st.chat_message("assistant"):
            st.markdown("Pipeline handshake complete! Next, we link our local LLM framework.")
        

