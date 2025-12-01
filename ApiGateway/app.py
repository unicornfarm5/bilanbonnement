from flask import Flask, request, jsonify
import requests

app = Flask(__name__)


#URL TIL SERVICES
ACCOUNT_SERVICE_URL = "http://accountservice:5000"


#Login
@app.route('/api/account/login', methods=['POST'])
def login():
    response = requests.post(
        "http://accountservice:5000/login",
        json=request.get_json()
    )
      # Forward JSON respons og status code
    try:
        gateway_response = jsonify(response.json())
    except Exception:
        # Hvis body ikke er JSON
        gateway_response = jsonify({"message": "Invalid response from account service"})

    # Forward Authorization header hvis den findes
    headers = {}
    if 'Authorization' in response.headers:
        headers['Authorization'] = response.headers['Authorization']

    return gateway_response, response.status_code, headers


#noget andet lol idk
@app.route('/api/account/profile', methods=['GET'])
def view_profile():
    auth_header = request.headers.get('Authorization')
    headers = {'Authorization': auth_header} if auth_header else {}
    response = requests.get(f"{ACCOUNT_SERVICE_URL}/profile", headers=headers)
    return jsonify(response.json()), response.status_code

#for at skarte flask og køre apppen 
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
