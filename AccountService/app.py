"""
    Account Service:
    login endpoint og profilvisning endpoint, 
    OBS: ingen opret bruger eller log ud version fordi MVP
    passwordhåndtering og brugerroller.
"""


from flask import Flask, jsonify, request, make_response
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from database import init_db, seed_users, find_user_by_username
from dotenv import load_dotenv
import os

load_dotenv() #henter KEY fra .env fil (den er ikke med på github btw)
#load database og default users
init_db()
seed_users()

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv('KEY')
jwt = JWTManager(app)


# Log bruger ind og returner JWT token
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Missing username or password'}), 400

    user = find_user_by_username(username)

    if not user or user['password'] != password:
        return jsonify({'message': 'Invalid username or password'}), 401

    # Laver JWT token - indeholder også brugerens rolle !
    token = create_access_token(
        identity=username, 
        additional_claims={"role": user['role']}
    )

    response = make_response(jsonify({'message': 'Login successful', 'token': token}), 200)
    response.headers['Authorization'] = f'Bearer {token}'
    return response



# Hent brugerprofil - ikke i brug endnu og ikke tilrettet til os
@app.route('/profile', methods=['GET'])
@jwt_required()
def view_profile():
    current_user = get_jwt_identity()
    claims = get_jwt()
    role = claims.get("role", "reader")

    user = find_user_by_username(current_user)              
    if not user:
        return jsonify({'message': 'User not found'}), 404

    return jsonify({
        'username': user['username'],
        'id': user['id'],
        'role': role,
    }), 200


app.run(host='0.0.0.0', port=5000)