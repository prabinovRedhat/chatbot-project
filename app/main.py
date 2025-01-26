import os
import streamlit as st
import requests
from langchain.chains import RetrievalQA
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import PyPDFLoader

# Load environment variables
API_KEY = os.getenv("API_KEY")
ENDPOINT_URL = os.getenv("ENDPOINT_URL")

# Function to query MaaS Mistral model
def query_mistral(prompt):
    headers = {"Authorization": f"Bearer {API_KEY}"}
    payload = {"prompt": prompt, "max_tokens": 150}
    response = requests.post(ENDPOINT_URL, json=payload, headers=headers)
    return response.json()

# Initialize Streamlit app
st.title("EcoSystem QE Onboarding Chatbot")
st.write("Ask me questions about onboarding, courses, and more!")

# Document upload
uploaded_file = st.file_uploader("Upload a PDF for context", type=["pdf"])
if uploaded_file:
    st.write("Processing document...")
    loader = PyPDFLoader(uploaded_file)
    documents = loader.load()
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma.from_documents(documents, embeddings)

    # Create a RetrievalQA chain
    retriever = vectorstore.as_retriever()
    qa_chain = RetrievalQA.from_chain_type(
        llm=query_mistral,
        retriever=retriever,
        return_source_documents=True
    )
    st.write("Document indexed successfully!")

# Chat interface
user_input = st.text_input("Your Question:")
if st.button("Ask"):
    if uploaded_file:
        response = qa_chain.run(user_input)
    else:
        response = query_mistral(user_input)
    st.write(response.get("text", "No response received"))
