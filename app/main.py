import os
import streamlit as st
from langchain.chains import RetrievalQA
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import PyPDFLoader
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

# Fetch API details from .env
API_KEY = os.getenv("API_KEY")
ENDPOINT_URL = os.getenv("ENDPOINT_URL")

if not API_KEY or not ENDPOINT_URL:
    st.error("API_KEY or ENDPOINT_URL is missing in the .env file.")

# Function to query MaaS Mistral model
def query_mistral(prompt):
    headers = {"Authorization": f"Bearer {API_KEY}"}
    payload = {"model": "mistral-7b-instruct", "prompt": prompt, "max_tokens": 200}
    response = requests.post(ENDPOINT_URL, json=payload, headers=headers)
    response.raise_for_status()  # Raise an error for bad responses
    return response.json()

# Process PDF files in the 'data' directory
def load_pdf_data(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        return []  # Return an empty list if no files are present
    documents = []
    for file in os.listdir(directory):
        if file.endswith(".pdf"):
            file_path = os.path.join(directory, file)
            loader = PyPDFLoader(file_path)
            documents.extend(loader.load())
    return documents

# Custom CSS for UI
custom_css = """
    <style>
        body {
            background-color: black;
            color: white;
        }
        .stApp {
            background-color: black;
            color: white;
        }
        h1 {
            color: #E00;
        }
        .stTextInput > div > label {
            color: white;
        }
        .stButton > button {
            background-color: #E00;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 0.5em 1em;
        }
        .stButton > button:hover {
            background-color: #C00;
        }
    </style>
"""

# Streamlit UI with customizations
st.markdown(custom_css, unsafe_allow_html=True)

# Add Red Hat logo
image_path = os.path.join("assets", "redhat-logo.png")
if not os.path.exists(image_path):
    st.error(f"Logo file not found at: {image_path}")
else:
    st.image(image_path, width=200)

st.title("EcoSystem QE Onboarding Chatbot")
st.write("Ask me questions about onboarding, courses, and more!")

# Load documents from 'data' directory
pdf_data_dir = "data"
documents = load_pdf_data(pdf_data_dir)

if documents:
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma.from_documents(documents, embeddings)

    # Create a RetrievalQA chain
    retriever = vectorstore.as_retriever()
    qa_chain = RetrievalQA.from_chain_type(
        llm=query_mistral, retriever=retriever, return_source_documents=True
    )

    st.write("PDF documents have been loaded and indexed successfully!")

    # User input
    user_input = st.text_input("Your Question:")
    if st.button("Ask"):
        if user_input:
            # Retrieve and respond
            try:
                response = qa_chain.run(user_input)
                st.write(response.get("text", "No response received"))
            except Exception as e:
                st.error(f"Error: {e}")
else:
    st.warning("No PDF files found in the data directory.")
