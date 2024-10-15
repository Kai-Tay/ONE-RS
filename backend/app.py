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



