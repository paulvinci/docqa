# Bring in deps
import streamlit as st
from streamlit_extras.stylable_container import stylable_container
from streamlit_star_rating import st_star_rating
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
st.set_page_config(page_title="RuLLM", page_icon="👑", layout="wide") 
st.markdown(f"""
            <style>
            .stApp {{background-image: url("https://images.unsplash.com/photo-1691466065738-1abe6adbbdd5?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1887&q=80"); 
                     background-attachment: fixed;
                     background-size: cover}}
         </style>
         """, unsafe_allow_html=True)

def stream_example(response_text):
    for word in response_text.split():
        yield word + " "
        time.sleep(0.1)

# Query through LLM    
ngrok_url = "https://5ad1-81-67-151-153.ngrok-free.app/"
question = st.text_input("Ask something from the file")    
if question:
    tic = time.perf_counter()
    url = f'{ngrok_url}search?query={question}'
    response = requests.get(url)
    toc = time.perf_counter()
    exec_time = time.strftime("%M:%S", time.gmtime(toc - tic))
    #st.info(response.text)
    with stylable_container(
        key="container_with_border",
        css_styles="""
            {
                background-color: lightgrey;
                color: black;
                border: 1px solid rgba(239,239,240,0.3);
                border-radius: 0.5rem;
                padding: calc(1em - 1px)
            }
            """):
        st.markdown(response.text)
    st.info(f'Execution time: {exec_time} minutes')
    st_star_rating(label="Please rate the relevance of the answer", maxValue=4, defaultValue=0, key="rating", dark_theme=True)