from flask import Flask, request, render_template, jsonify
import requests
import os
import json

app = Flask(__name__)

# Using a completely free API that doesn't require authentication
API_URL = "https://api.freeapi.app/api/v1/public/quotes/quote/random"

def get_ai_response(question):
    # Simple rule-based responses + random quote for demo
    question_lower = question.lower()
    
    if "hello" in question_lower or "hi" in question_lower:
        return "Hello! I'm your AI assistant. Ask me anything!"
    elif "how are you" in question_lower:
        return "I'm doing great! Thanks for asking. How can I help you today?"
    elif "weather" in question_lower:
        return "I don't have access to real-time weather data, but I hope it's nice where you are!"
    elif "time" in question_lower:
        return "I don't have access to real-time data, but you can check your system clock!"
    else:
        # Get a random inspirational quote as a fallback
        try:
            response = requests.get(API_URL, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if 'data' in data and 'content' in data['data']:
                    quote = data['data']['content']
                    author = data['data'].get('author', 'Unknown')
                    return f"Here's some wisdom for you: \"{quote}\" - {author}"
        except:
            pass
        
        return f"That's an interesting question about '{question}'. I'm a simple demo bot, but I'd love to help you explore that topic further!"

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