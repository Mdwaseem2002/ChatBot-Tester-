from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv, find_dotenv 
import flask_cors
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


# Load environment variables from .env file
load_dotenv(find_dotenv())

# Set the API key
api_key = os.environ.get('API KEY')

# Set the API endpoint
endpoint = "https://generativelanguage.googleapis.com/v1beta"

@app.route('/')
def index():
    return 'Hello, World!'


@app.route('/generate_content', methods=['POST'])
def generate_content():
    try:
        # Get data from the request
        data = request.json

        chat_conversation = data["text"]

        prompt = f"This is a chat conversation between a user and a chatbot. Design test scenarios and list comprehensive test cases for such a converstaion to identify errors and evaluate response. Please use the relevant chatbot testing guidelines. Please give the output in a properly formatted markdown. The conversation is given here {chat_conversation}"
        
        # Prepare the request body
        request_body = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ]
        }
        
        # Make the request
        response = requests.post(
            f"{endpoint}/models/gemini-pro:generateContent?key={'API KEY'}",
            json=request_body,
        )

        # Parse the response
        response_json = response.json()

       # Check if the request was successful
        if response.status_code == 200:
            # Parse the response
            response_json = response.json()

            # Check if 'candidates' key exists in the response JSON
            if 'candidates' in response_json:
                generated_content = response_json["candidates"][0]['content']['parts'][0]['text']
                return jsonify({"generated_content": generated_content}), 200
            else:
                return jsonify({"message": "No candidates found in the response."}), 404
        else:
            return jsonify({"message": "Error from Generative Language API", "status_code": response.status_code}), 500
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@app.route('/get_generated_content', methods=['GET'])
def get_generated_content():
    try:
        # Retrieve the generated content from the frontend
        # This could involve querying a database or other storage mechanism
        generated_content = "Example generated content from the server"
        
        return jsonify({"generated_content": generated_content}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
