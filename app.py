from flask import Flask, request, render_template, jsonify
import requests
import os
import json

app = Flask(__name__)

# Using Hugging Face Inference API without authentication (rate limited but free)
API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"

def get_ai_response(question):
    try:
        # Try Hugging Face API first
        payload = {"inputs": question}
        response = requests.post(API_URL, json=payload, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                generated_text = result[0].get('generated_text', '')
                if generated_text and generated_text != question:
                    return generated_text.replace(question, '').strip()
        
        # Fallback to simple responses if API fails
        question_lower = question.lower()
        
        if "hello" in question_lower or "hi" in question_lower:
            return "Hello! I'm your AI assistant. Ask me anything!"
        elif "how are you" in question_lower:
            return "I'm doing great! Thanks for asking. How can I help you today?"
        elif "what" in question_lower and "name" in question_lower:
            return "I'm an AI assistant created for this demo. You can call me Demo Bot!"
        elif "help" in question_lower:
            return "I'm here to help! Ask me questions about anything - technology, general knowledge, or just chat!"
        else:
            return f"That's an interesting question about '{question}'. I'm still learning, but I'd be happy to discuss this topic with you!"
            
    except Exception as e:
        return f"I'm having trouble processing that right now, but I heard you ask about '{question}'. Could you try rephrasing it?"

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
        
        # Get AI response
        answer = get_ai_response(question)
        
        return jsonify({'answer': answer})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)