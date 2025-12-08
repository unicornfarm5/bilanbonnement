from flask import Flask, request, jsonify, Response
from flask_jwt_extended import JWTManager, jwt_required
import requests
import os
from dotenv import load_dotenv


load_dotenv()  

#ide til opsætning fra Christian 
# Service URLs (internal Docker network)

app = Flask(__name__)

# 
app.config['JWT_SECRET_KEY'] = os.getenv("KEY")
app.config['JWT_ALGORITHM'] = "HS256"

jwt = JWTManager(app)

services = {
    "accountservice": "http://accountservice:5000",
    "rentalservice": "http://rentalservice:5000"
}

@app.route('/<service>/<path:path>', methods=["GET", "POST", "PUT", "DELETE"])
@jwt_required(optional=True)
def apiGateWay(service, path):

    if service not in services:
        return jsonify(msg="no service with that name"), 404

    url = f"{services[service]}/{path}"

    headers = {k: v for k, v in request.headers.items()}
    serviceResponse = requests.request(
        method=request.method,
        url=url,
        headers=headers,
        params=request.args,
        data=request.get_data(),
    )

    return Response(
        response=serviceResponse.content,
        status=serviceResponse.status_code,
        headers=dict(serviceResponse.headers)
    )




#vigtigt for at skarte flask og køre apppen 
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
