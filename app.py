# Bring in deps
from http.client import responses
import streamlit as st
from streamlit_extras.stylable_container import stylable_container
from streamlit_text_rating.st_text_rater import st_text_rater
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
import pandas as pd


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

@st.cache_data
def llm_inference(url):
    response = requests.get(url)
    return response

# Query through LLM    
ngrok_url = "https://065e-81-67-151-153.ngrok-free.app"
question = st.text_input("Ask something from the file")    
if question:
    url = f'{ngrok_url}/search?query={question}'
    response = llm_inference(url)
    toc = time.perf_counter()
    st.info(response.text)
 
if question:
    if response:
        evaluation = st_text_rater(text='Is this reponse relevant ?')   
        if evaluation:
            if evaluation != None:
                score_dict = {'liked':1,'disliked':0}
                score = score_dict[evaluation]
                st.write(score)
                df = pd.read_csv('./evaluate.csv')
                temp = pd.DataFrame({'question':[question],'response':[response.text],'evaluation':[score]})
                new_df = pd.concat([df,temp])[['question','response','evaluation']]
                new_df.to_csv('./evaluate.csv')
                st.dataframe(df)
                st.dataframe(new_df)
    