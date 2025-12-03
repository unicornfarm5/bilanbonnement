from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer
from dotenv import load_dotenv
import sqlite3
import os
import jwt
from rentalDatabase import init_db, get_all_rentals_db, seed_rentals

#Load envirement varables, KEY til jwt-token
load_dotenv()
SECRET_KEY = os.getenv("KEY")
JWT_ALGORITHM = "HS256"

DATABASE = "rentals.db"
app = FastAPI() #initialize FASTAPI app
#load database og fyld den med defaul data
init_db()
seed_rentals()

security = HTTPBearer()

######### -- JWT VALITATION -- ############
##læser bearer token og validerer den + returner rolle (som er en del af payload)
#Funktion fra ChatGPT
def verify_jwt(credentials=Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

#Rolle-checker
#Funktion fra ChatGPT
def require_role(allowed_roles: list):
    def role_checker(user=Depends(verify_jwt)):
        role = user.get("role", None)
        if role not in allowed_roles:
            raise HTTPException(status_code=403, detail="Not enough permissions")
        return user
    return role_checker



######### -- Endpoints -- ############
#Select all rentals - alle roller har adgang
@app.get("/all_rentals")
def get_all_rentals(user = Depends(require_role(["rental","damage", "business"]))):
    return get_all_rentals_db()