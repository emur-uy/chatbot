from flask import Flask, request, abort, jsonify
import os
from dotenv import load_dotenv
from chatbot import get_answer
from flasgger import Swagger
from gevent.pywsgi import WSGIServer

# Load the environment variables from the .env file
load_dotenv()

# Create a new Flask app
app = Flask(__name__)

#doc for api
template = {
  "swagger": "2.0",
  "info": {
    "title": "EMUR Chatbot",
    "description": "API for CHATBOT",
    "contact": {
      "responsibleOrganization": "EMUR",
      "responsibleDeveloper": "fabian.delgado@outlook.com",
      "email": "fabian.delgado@outlook.com",
    },
    "version": "0.0.1"
  },
  "operationId": "getmyData"
}
swagger = Swagger(app, template=template)

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
    """
    This is the chat API
    Call this api passing a question and get an answer
    ---
    tags:
      - Chat API
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
        description: The API key
      - name: body
        in: body
        required: true
        schema:
          id: data
          required:
            - question
          properties:
            question:
              type: string
              description: The question for the chatbot
    responses:
      200:
        description: The answer to the question
        schema:
          id: return
          properties:
            answer:
              type: string
              description: The answer from the chatbot
      401:
        description: The request is not authenticated
    """
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

if __name__ == '__main__':
    # Use the 'PORT' environment variable if it's set, otherwise default to 80
    port = int(os.environ.get('PORT', 80))

    # Run the app with Gunicorn
    http_server = WSGIServer(('', port), app)
    http_server.serve_forever()
