from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
from dotenv import load_dotenv

# lokale moduler
from database import init_db, get_db_connection

""" Hovedapplikationen 
(Flask-serveren som modtager requests fra brugere/UI og bruger rental_client.py til validering). """


