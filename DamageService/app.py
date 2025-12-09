from rental_search_api import RentalCheck
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS

# opret klientinstans
rental_check = RentalCheck()

app = Flask(__name__)
CORS(app)
load_dotenv()

#POST route



#GET route





