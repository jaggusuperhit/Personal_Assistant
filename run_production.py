# Use a production WSGI server
from waitress import serve
from app import app
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=5000)
