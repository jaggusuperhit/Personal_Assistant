import os
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from pydantic import SecretStr
import gdown

# Download .env file from gdrive
file_id = "1OU7xpnpHyCDFQUJc2f9cGFiDE2Plek6E"
url = f"https://drive.google.com/uc?id={file_id}"
output = ".env"
gdown.download(url, output, quiet=False)

# Load environment variables
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "db")

# Use HuggingFace for embeddings (local, no API key needed)
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={'device': 'cpu'}
)

# Load stored vector database
vector_db = Chroma(
    persist_directory=CHROMA_DB_PATH,
    embedding_function=embeddings
)
retriever = vector_db.as_retriever()

# Use Groq for chat
llm = ChatOpenAI(
    api_key=SecretStr(GROQ_API_KEY),
    model="llama3-70b-8192",  # You can change to another Groq-supported model
    base_url="https://api.groq.com/openai/v1"
)

# Create RetrievalQA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True
)

def get_response(query: str):
    result = qa_chain.invoke({"query": query})
    # Convert Document objects to dicts for JSON serialization
    source_docs = result.get("source_documents", [])
    source_docs_serializable = []
    for doc in source_docs:
        # Each doc is a langchain Document object
        source_doc = {
            "page_content": getattr(doc, "page_content", str(doc)),
            "metadata": getattr(doc, "metadata", {})
        }
        source_docs_serializable.append(source_doc)
    return {
        "response": result["result"],
        "source_documents": source_docs_serializable
    }