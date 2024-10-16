import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

# FIREBASE
import firebase_admin
from firebase_admin import credentials, firestore

# VERTEX AI
import vertexai
from google.oauth2 import service_account
from vertexai.generative_models import GenerativeModel, Part, SafetySetting


app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return 'Hello, World'
# act with the flask application
# define a route: a url 
# 127.0.0.1:500/ behind is the get request 
# ? after that is specify parameters to the variable 
# post got no question mark


# START FROM HERE!!!!!!!

app = Flask(__name__)

# Connect to firebase
cred = credentials.Certificate("./credentials.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route('/')
def hello_world():
    return 'Hello, World'

@app.route('/add_supplier', methods=['POST'])
def add_supplier():
    data = request.json
    doc_ref = db.collection('suppliers').document()
    doc_ref.set(data)
    return jsonify({"message": "Supplier added successfully", "id": doc_ref.id}), 201

@app.route('/add_client', methods=['POST'])
def add_client():
    data = request.json
    doc_ref = db.collection('clients').document()
    doc_ref.set(data)
    return jsonify({"message": "Client added successfully", "id": doc_ref.id}), 201

@app.route('/get_suppliers')
def get_suppliers():
    suppliers_ref = db.collection('suppliers')
    docs = suppliers_ref.get()
    suppliers = [doc.to_dict() for doc in docs]
    return jsonify(suppliers)

@app.route('/get_clients')
def get_clients():
    clients_ref = db.collection('clients')
    docs = clients_ref.get()
    clients = [doc.to_dict() for doc in docs]
    return jsonify(clients)

# Initialize Vertex AI with service account credentials
credentials = service_account.Credentials.from_service_account_file("./serviceAccountCredentials.json")
vertexai.init(
    project="one-rs",
    location="asia-southeast1",
    credentials=credentials
)

@app.route('/search_ai', methods=['POST'])
def generate_ingredients():
    # Get JSON data from the request
    data = request.get_json()
    user_input = data.get("data")
    if not user_input:
            return jsonify({"error": "No prompt provided"}), 400

    # System context or instruction - set the behavior for the model
    instruction = """You are required to find out what food item the user is referring to and provide a list of ingredients to make that food item.

                    Keep the list to less than 20 ingredients and are relevant for suppliers.
                    Use ONLY these categories: {Poultry, Beef, Pork, Lamb, Fish, Shellfish, Vegetables, Fruits, Eggs, Milk, Cheese, Grains, Bread, Pasta}

                    Provide a generalised results of those ingredients and categories as short as possible. 

                    Return the output in list string format with the following structure:
                     [{
                         "ingredients": ["ingredient1", "ingredient2", ...],
                         "categories": ["category1", "category2", ...]
                     }]
                    DO NOT INCLUDE THE WORD JSON in the result"""

    model = GenerativeModel(
            "gemini-1.5-flash-001",
            system_instruction=[instruction]
        )
    
    responses = model.generate_content(
        [user_input],
        generation_config={
            "max_output_tokens": 150,
            "temperature": 1.0,
            "top_p": 0.95,
        },
        safety_settings= [
            SafetySetting(
                category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                threshold=SafetySetting.HarmBlockThreshold.OFF
            ),
            SafetySetting(
                category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                threshold=SafetySetting.HarmBlockThreshold.OFF
            ),
            SafetySetting(
                category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                threshold=SafetySetting.HarmBlockThreshold.OFF
            ),
            SafetySetting(
                category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
                threshold=SafetySetting.HarmBlockThreshold.OFF
            ),
        ],
        stream=True,
    )


    # Extract the model's response
    generated_text = ""
    for response in responses:
        generated_text += response.text

    try:
        # Parse the generated text as JSON
        output_json = json.loads(generated_text)
        return jsonify(output_json), 200
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON response from the model"}), 500

# Initialise server
if __name__ == '__main__':
    app.run(port=5001, debug=True)


