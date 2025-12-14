from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.security import HTTPBearer
from dotenv import load_dotenv
from database import init_db, seed_customers, get_all_customers_db, get_all_customer_id_db
import os
import jwt
#Loader .env, KEY til jwt-token
load_dotenv()
SECRET_KEY = os.getenv("KEY")
#JWT_ALGORITHM = "HS256"

DATABASE = "rental.db"
app = FastAPI() #initialize FASTAPI app
#load database og fyld den med default data
init_db()
seed_customers()



# --- Rolle tjekker --- # 
    #Prcæs som rolle checkeren fra RentalService
# til brug i endpoints for at styre adgang
#Funktion fra ChatGPT
def get_role_from_token(token: str):
    """Dekoder JWT-token og returnerer brugerens rolle"""
    if not token:
        return None, "Missing token"
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded.get("role"), None
    except jwt.ExpiredSignatureError:
        return None, "Token expired"
    except jwt.InvalidTokenError:
        return None, "Invalid_token"
    

#Struktur efterabet fra RentalService
@app.get("/all_customers")
def get_all_customers(
    authorization: str = Header(None)
):
    if authorization is None:
        return {"message": "Missing Authorization header"}, 401

    # Fjern 'Bearer ' prefix
    if authorization.startswith("Bearer "):
        auth_token = authorization[7:]
    else:
        auth_token = authorization
    role, err = get_role_from_token(auth_token)
    if err:
        return {"message": err}, 401
    if role != "rental":  #VIGTIGT: kun rental-medarbejdere i rental har adgang til alt kunde-data
        return {"message": f"Din rolle: {role} har ikke adgang til denne information"}, 403

    rentals = get_all_customers_db()
    return rentals


#get only customer id
@app.get("/all_customer_id")
def get_all_customer_id(
    authorization: str = Header(None)
):
    if authorization is None:
        return {"message": "Missing Authorization header"}, 401

    # Fjern 'Bearer ' prefix
    if authorization.startswith("Bearer "):
        auth_token = authorization[7:]
    else:
        auth_token = authorization
    role, err = get_role_from_token(auth_token)
    if err:
        return {"message": err}, 401
    if role != "business":  #VIGTIGT: kun business behøves bruge dette endpoint - det er så de ikke kan få personlig data som tlf og mail på kunder. men kun id
        return {"message": f"Din rolle: {role} har ikke adgang til denne information"}, 403

    rentals = get_all_customer_id_db()
    return rentals
