from urllib import request
from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.security import HTTPBearer
from dotenv import load_dotenv
from flask import jsonify, request, make_response
from rentalDatabase import init_db, get_all_rentals_db, seed_rentals, get_db_connection
from typing import Optional
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
seed_rentals()

security = HTTPBearer()

# --- Test af container --- #
# #ide fra ChatGPT
@app.get("/health")
def health():
    return {"status": "ok"}


# --- Rolle tjekker --- # 
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


# --- Endpoints --- #

#Kode lavet med hjælp fra ChatGPT
@app.get("/all_rentals")
def get_all_rentals(authorization: str = Header(None)):
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

    if role != "rental": #VIGTIGT: kun rental-medarbejdere har adgang pt
        return {"message": "Unauthorized"}, 403

    rentals = get_all_rentals_db()
    return rentals


@app.get("/rentals/{order_id}")
def get_rental(order_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM rental WHERE order_id = ?', (order_id,))
    rental = cursor.fetchone()
    conn.close()
    
    if not rental:
        raise HTTPException(status_code=404, detail=f"order_id {order_id} findes ikke")
    
    return dict(rental)


@app.get("/rentals")
def get_rentals_by_plate(license_plate: Optional[str] = None):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if license_plate:
        cursor.execute('SELECT * FROM rental WHERE license_plate = ?', (license_plate,))
    else:
        cursor.execute('SELECT * FROM rental')
    
    rentals = cursor.fetchall()
    conn.close()
    
    return [dict(r) for r in rentals]