# Bring in deps
import streamlit as st 
import time
import os
import requests
from langchain.document_loaders import TextLoader, Docx2txtLoader
from langchain.vectorstores import FAISS
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain import PromptTemplate


# Customize the layout
st.set_page_config(page_title="LOM ASSISTANT", page_icon="👑", layout="wide")     
st.markdown(f"""
            <style>
            .stApp {{background-image: url("https://images.unsplash.com/photo-1682685797366-715d29e33f9d?ixlib=rb-4.0.3&ixid=M3wxMjA3fDF8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=870&q=80"); 
                     background-attachment: fixed;
                     background-size: cover}}
         </style>
         """, unsafe_allow_html=True)

# Query through LLM    
question = st.text_input("Ask something from the file")    
if question:
    tic = time.perf_counter()
    url = f'https://4c34-81-67-151-153.ngrok-free.app/search?query={question}'
    response = requests.get(url)
    toc = time.perf_counter()
    exec_time = time.strftime("%M:%S", time.gmtime(toc - tic))
    st.info(response.text)
    st.info(f'Execution time: {exec_time} minutes')
    st.slider('Evaluate answer - 5 being excellent answer',1,5)