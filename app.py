import os
import logging
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from backend.model import get_response  # Import the function from model.py


# Load environment variables
load_dotenv()

os.system("python backend/ingest_data.py")  # Ensure the database is up to date

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    query = data.get('query')
    
    if not query:
        return jsonify({"error": "No query provided"}), 400
    
    try:
        result = get_response(query)
        # Log the result for debugging
        logging.info("get_response result: %s", result)
        # If result is a dict, return as is (for response + source_documents)
        if isinstance(result, dict):
            return jsonify(result)
        # Otherwise, wrap in expected structure
        return jsonify({"response": result})
    except Exception as e:
        logging.error("Error in /ask: %s", e, exc_info=True)
        return jsonify({"error": str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
