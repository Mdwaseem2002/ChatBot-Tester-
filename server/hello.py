from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv, find_dotenv
import requests
import flask_cors
from flask_cors import CORS

# Load environment variables from .env file
load_dotenv(find_dotenv())

# Set the API key
api_key = os.environ.get('')

# Set the API endpoint
endpoint = "https://generativelanguage.googleapis.com/v1beta"

app = Flask(__name__)
CORS(app)

@app.route('/generate_content', methods=['POST'])
def generate_content():
    try:
        # Get data from the request body
        data = request.json
        
        # Check if 'text' key exists in the request data
        if 'text' in data:
            # Prepare the request body
            request_body = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": data["text"]
                            }
                        ]
                    }
                ]
            }

            # Make the request to the Generative Language API
            response = requests.post(
                f"{endpoint}/models/gemini-pro:generateContent?key={''}",
                json=request_body,
            )

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
        else:
            return jsonify({"message": "Missing 'text' key in request data"}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
