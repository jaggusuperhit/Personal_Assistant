import os
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
import gdown
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Download .env file from gdrive
file_id = "1OU7xpnpHyCDFQUJc2f9cGFiDE2Plek6E"
url = f"https://drive.google.com/uc?id={file_id}"
output = ".env"
gdown.download(url, output, quiet=False)

# Load environment variables
load_dotenv()
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "db")

# Use local embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={'device': 'cpu'}
)

# Load Documents
documents = [
    Document(page_content="Meeting notes: Discuss project X deliverables."),
    Document(page_content="Reminder: Submit report by Friday."),
    Document(page_content="Upcoming event: Tech conference next Wednesday")
]

# Split text
text_splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=50)
docs = text_splitter.split_documents(documents)

# Create vector store
vector_db = Chroma.from_documents(
    docs, 
    embedding=embeddings, 
    persist_directory=CHROMA_DB_PATH
)
vector_db.persist()

print("Documents successfully indexed!")