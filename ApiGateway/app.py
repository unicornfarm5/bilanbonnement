from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

### ----  Account Service ---- ###
ACCOUNT_SERVICE_URL = "http://accountservice:5000"

#ENDPOINT -- login
@app.route('/api/account/login', methods=['POST'])
def login():
    response = requests.post(
        f"{ACCOUNT_SERVICE_URL}/login",
        json=request.get_json()
    )
      # ide fra chatGPT
      # Forward JSON respons og status code
    try:
        gateway_response = jsonify(response.json())
    except Exception:
        gateway_response = jsonify({"message": "Invalid response from account service"})

    # Finder og forwarder Authorization header hvis den findes
    headers = {}
    if 'Authorization' in response.headers:
        headers['Authorization'] = response.headers['Authorization']

    return gateway_response, response.status_code, headers

#ENDPOINT -- get profile
@app.route('/api/account/profile', methods=['GET'])
def view_profile():
    auth_header = request.headers.get('Authorization')
    headers = {'Authorization': auth_header} if auth_header else {}
    response = requests.get(f"{ACCOUNT_SERVICE_URL}/profile", headers=headers)
    return jsonify(response.json()), response.status_code



### ----  Rental Service ---- ###
RENTAL_SERVICE_URL = "http://rentalservice:5000"

#ENDPOINT -- get all rentals
@app.route('/api/rental/all_rentals', methods=['GET'])
def get_rentals():
    response = requests.get(f"{RENTAL_SERVICE_URL}/rental")
    return jsonify(response.json()), response.status_code





#vigtigt for at skarte flask og køre apppen 
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
