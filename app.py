from flask import Flask, request, render_template, jsonify
import requests
import os
import json

app = Flask(__name__)

# Hugging Face API configuration (free tier)
HF_API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
HF_TOKEN = os.getenv('HUGGING_FACE_TOKEN', '')

def query_huggingface(payload):
    headers = {"Authorization": f"Bearer {HF_TOKEN}"} if HF_TOKEN else {}
    response = requests.post(HF_API_URL, headers=headers, json=payload)
    return response.json()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_question():
    try:
        data = request.get_json()
        question = data.get('question', '')
        
        if not question:
            return jsonify({'error': 'No question provided'}), 400
        
        # Query Hugging Face API
        payload = {"inputs": question}
        result = query_huggingface(payload)
        
        # Handle different response formats
        if isinstance(result, list) and len(result) > 0:
            answer = result[0].get('generated_text', 'No response generated')
        elif isinstance(result, dict):
            answer = result.get('generated_text', result.get('error', 'Unknown error'))
        else:
            answer = "Unable to process the request"
        
        return jsonify({'answer': answer})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)