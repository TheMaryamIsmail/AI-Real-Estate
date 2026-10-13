import os
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

class RAGKnowledgeAssistant:
    def __init__(self, persist_directory="vector_db"):
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.persist_directory = persist_directory
        self.vector_store = None
        self.init_vector_store()

    def init_vector_store(self):
        sample_docs = [
            "Property Buying Guide: Always inspect the roof, foundation (e.g., poured concrete vs brick tile), and plumbing before making an offer.",
            "Investment Tips: Neighborhoods like Northridge (NoRidge) and Stone Brook (StoneBr) historically offer higher appreciation rates in Ames.",
            "Legal Documents: Ensure title deeds are verified, property taxes are cleared, and zoning laws permit your intended residential alterations."
        ]
        
        if os.path.exists(self.persist_directory):
            self.vector_store = Chroma(persist_directory=self.persist_directory, embedding_function=self.embeddings)
        else:
            self.vector_store = Chroma.from_texts(sample_docs, self.embeddings, persist_directory=self.persist_directory)

    def query(self, question: str) -> str:
        docs = self.vector_store.similarity_search(question, k=2)
        context = "\n".join([doc.page_content for doc in docs])
        return f"Based on our knowledge base:\n{context}\n\nAnswer: This document provides guidance relevant to your inquiry regarding '{question}'.",