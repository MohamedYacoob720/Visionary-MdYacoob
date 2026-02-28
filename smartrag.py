import os
import pandas as pd
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
from langchain_core.language_models.llms import LLM
from langchain_core.callbacks import CallbackManagerForLLMRun
#from langchain_groq import ChatGroq  # for chat/completions
from groq import Groq
from langchain_community.document_loaders import (
    PyPDFLoader, 
    Docx2txtLoader, 
    UnstructuredWordDocumentLoader,
    UnstructuredExcelLoader, 
    WebBaseLoader
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
#from langchain_openai import ChatOpenAI
from langchain_classic.chains import RetrievalQA

from dotenv import load_dotenv
from typing import Optional, List, Any

load_dotenv()  # Load environment variables from .env file

# 1. SETUP - Configure your API Key if using OpenAI, or use a local LLM
api_key = os.getenv("GROQ_API_KEY") or ""

class GroqLLM(LLM):
    api_key: str
    model: str = "openai/gpt-oss-120b"
    prompt: str = "Answer the question based on the retrieved documents."

    @property
    def _llm_type(self) -> str:
        return "groq"

    def _call(self, prompt: str, stop: Optional[List[str]] = None, run_manager: Optional[CallbackManagerForLLMRun] = None,**kwargs: Any) -> str:
        return self.llmf(prompt)

    def llmf(self, prompt):
        a=[]
        client = Groq(api_key=self.api_key)
        completion = client.chat.completions.create(
            model=self.model,
            messages=[
            {
                "role": "system",
                "content": "You are a precise assistant. Use ONLY the context below.If answer is not found, say 'Not found in documents.'"
            },
            {
                "role": "user",
                "content": prompt
            }
            ],
            temperature=1,
            max_completion_tokens=300,
            top_p=1,
            reasoning_effort="medium",
            stream=True,
            stop=None
        )   
        for chunk in completion:
            a.append(chunk.choices[0].delta.content or "")
        
        return " ".join(a)
    
llm = GroqLLM(api_key=api_key)

def load_data(inputs):
    """Loads data from multiple sources: PDF, Word, Excel, and Web URLs."""
    documents = []
    for source in inputs:
        if source.endswith(".pdf"):
            loader = PyPDFLoader(source)
        elif source.endswith(".docx"):
            loader = Docx2txtLoader(source)
        elif source.endswith(".doc"):
            loader = UnstructuredWordDocumentLoader(source)
        elif source.endswith(".xlsx") or source.endswith(".xls"):
            # Excel is often handled better as a CSV or specific loader
            loader = UnstructuredExcelLoader(source)
        elif source.startswith("http"):
            loader = WebBaseLoader(source)
        else:
            print(f"Unsupported format: {source}")
            continue
        
        documents.extend(loader.load())
    return documents

def build_rag_system(file_list,qru):
    # 2. LOAD & SPLIT
    raw_docs = load_data(file_list)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = text_splitter.split_documents(raw_docs)
    
    # 3. EMBEDDINGS (using all-MiniLM-L6-v2 as requested)
    # This runs locally on your CPU/GPU
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # 4. VECTOR STORE (Chroma DB)
    vector_db = Chroma.from_documents(
        documents=docs, 
        embedding=embeddings,
        persist_directory="./chroma_db"
    )

    # 5. GROQ LLM RETRIEVAL & LLM CHAIN
    # Popular models: "llama-3.3-70b-versatile" or "mixtral-8x7b-32768"
    # llm = ChatGroq(
    #     model_name="llama-3.3-70b-versatile",
    #     temperature=0.1
    # )
    
    qa_chain = RetrievalQA.from_chain_type(
        llm = GroqLLM(api_key=api_key,prompt=qru),
        chain_type="stuff",
        retriever=vector_db.as_retriever()
    )
    
    return qa_chain

if __name__ == "__main__":
    my_sources = [
        "data/Agentic AI Internship for 6 months_.pdf",
        "data/Questionaire.doc",
        "data/Excel-Project.xlsx",
        "https://python.langchain.com/docs/get_started/introduction"
    ]
    
    print("Initializing RAG System...")
    rag_bot = build_rag_system(my_sources,"Answer the question based on the retrieved documents.")
    
    # 6. CHAT LOOP
    while True:
        query = input("\nAsk a question about your documents (or 'exit'): ")
        if query.lower() == 'exit':
            break
        
        response = rag_bot.invoke(query)
        print(f"\nAI Summary Output: {response['result']}")