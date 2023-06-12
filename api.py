from flask import Flask, request, abort, jsonify
import os
from dotenv import load_dotenv
from chatbot import get_answer

# Load the environment variables from the .env file
load_dotenv()

# Create a new Flask app
app = Flask(__name__)

# Set configuration parameters
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # Disable caching of static files
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')  # Secret key for sessions


# Function to authenticate API requests
def auth(key):
    # The secret API key is stored in an environment variable
    key_storage = os.getenv('API_KEY')

    # If the provided key matches the stored key, the request is authenticated
    if key_storage == key:
        return True
    else:
        return False

# Route for the API endpoint
@app.route('/api/v1/chat', methods=['POST'])
def api():
    # Authenticate the request using the 'Authorization' header
    if auth(request.headers.get('Authorization')):
        # Get the question from the request body
        data = request.get_json()
        question = data.get('question')

        # Get the answer from the chatbot script
        answer = get_answer(question)

        # Return the answer as a JSON response
        return jsonify({'answer': answer})
    else:
        # If the request is not authenticated, return a 401 error
        abort(401)

# Run the app
if __name__ == '__main__':
    # Use the 'PORT' environment variable if it's set, otherwise default to 80
    port = int(os.environ.get('PORT', 80))

    # Run the app in debug mode, listening on all IP addresses
    app.run(debug=True, host='0.0.0.0', port=port)