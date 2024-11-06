import json
import os
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv
import stripe

# VERTEX AI
import vertexai
from google.oauth2 import service_account
from vertexai.generative_models import GenerativeModel, Part, SafetySetting


app = Flask(__name__)
CORS(app, origins="http://localhost:5173")


@app.route('/')
def hello_world():
    return jsonify({"working!": "hello world"}), 200


# START FROM HERE!!!!!!!
stripe.api_key = os.getenv("STRIPE_SECRET")
gcloud_credentials = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# Initialize Vertex AI with service account credentials
credentials = service_account.Credentials.from_service_account_file("./serviceAccountKey.json")
vertexai.init(
    project="one-rs",
    location="asia-southeast1",
    credentials=credentials
)

@app.route('/search-ai', methods=['OPTIONS', 'POST'])
@cross_origin(origin='http://localhost:5173')
def generate_ingredients():
    # Get JSON data from the request
    data = request.get_json()
    user_input = data.get("data")
    if not user_input:
            return jsonify({"error": "No prompt provided"}), 400

    # System context or instruction - set the behavior for the model
    instruction = """You are required to find out what food item the user is referring to and provide a list of ingredients to make that food item.

                    Keep the list to less than 5 ingredients and are relevant for suppliers.
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
    

@app.route('/create-checkout', methods=['POST'])
def create_payment_intent():
    try:
        # Retrieve data from the request body
        data = request.get_json()
        # Get payment amount
        amount = data.get("amount") 


        # Create a payment intent
        payment_intent = stripe.PaymentIntent.create(
            amount=amount,  # Amount in cents
            currency="sgd"
        )

        # Send the client secret back to the frontend
        return jsonify({"clientSecret": payment_intent.client_secret})
    
    except Exception as e:
        # Handle exceptions
        return jsonify({"error": str(e)}), 500

    

# Initialise server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)


