from flask import Flask, request, jsonify
import os
import firebase_admin
from firebase_admin import credentials, firestore

print("this is a change!")
app = Flask(__name__)

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
cred = credentials.Certificate("/backend/credentials.json")
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
if __name__ == '__main__':
    app.run(port=5001, debug=True)


