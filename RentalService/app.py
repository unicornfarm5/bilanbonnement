from urllib import request
from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.security import HTTPBearer
from dotenv import load_dotenv
from flask import jsonify, request, make_response
from flask_jwt_extended import jwt_required
from pydantic import BaseModel
from rentalDatabase import init_db, get_all_rentals_db, seed_rentals, add_rentals_db, update_rentals_db
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



# --- Basemodel for rentals, der gør det lettere at holde styr på alle entiteter i databasen
# Ide fra chatGPT

class RentalInput(BaseModel):
    customer_id: str
    license_plate: str
    rental_start: str
    rental_end: str
    rental_type: str
    price_per_month: float

# --- Basemodel til opdatering - note that ikke alle entiteter i en rental skal kunne opdateres
# Denne er klar til at disse felter ville kunne opdateres, hvis vi vil tilføje den funktion,
# Bygget fleksibel så vi kan bruge basemodel'en ligemeget hvilket/hvilke felter vi vil opdatere

class UpdateRentalInput(BaseModel):
    license_plate: str | None = None
    rental_end: str | None = None
    rental_type: str | None = None
    price_per_month: float | None = None




# --- Endpoints --- #

#Kode lavet med hjælp fra ChatGPT
@app.get("/all_rentals")
def get_all_rentals(
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
    if role not in ["rental", "business"]: #VIGTIGT: kun rental-medarbejdere og business har adgang til den fulde database
        return {"message": f"Din rolle: {role} har ikke adgang til denne information"}, 403

    rentals = get_all_rentals_db()
    return rentals


#Endpoint til tilføjelse af ny lejeaftale
@app.post("/all_rentals")
def post_to_all_rentals(
    rental: RentalInput,  # <-- Her modtages alle felter udfra klasen
    authorization: str = Header(None)
):
    if authorization is None:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    # Fjern 'Bearer ' prefix
    if authorization.startswith("Bearer "):
        auth_token = authorization[7:]
    else:
        auth_token = authorization
    role, err = get_role_from_token(auth_token)
    if err:
        raise HTTPException(status_code=401, detail=err)

    if role != "rental":
        raise HTTPException(status_code=403, detail=f"Din rolle: {role} har ikke adgang")

    # Kald databasefunktion og bruger basemodel
    rentals = add_rentals_db(
        rental.customer_id,
        rental.license_plate,
        rental.rental_start,
        rental.rental_end,
        rental.rental_type,
        rental.price_per_month,
    )

    return rentals



#Endpoint til opdatering af lejeaftale
@app.put("/all_rentals/update/{order_id}")
def update_rental(
    order_id: int, 
    rental_update: UpdateRentalInput, #Fra class'en
    authorization: str = Header(None)
):
    if authorization is None:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    # Fjern 'Bearer ' prefix
    if authorization.startswith("Bearer "):
        auth_token = authorization[7:]
    else:
        auth_token = authorization
    role, err = get_role_from_token(auth_token)
    if err:
        raise HTTPException(status_code=401, detail=err)

    if role != "rental": # KUN medarbejdere i rental kan opdatgere
        raise HTTPException(status_code=403, detail=f"Din rolle: {role} har ikke adgang")

    # Kald databasefunktion og bruger basemodel
    updated = update_rentals_db(order_id, {"rental_end": rental_update.rental_end})


    if updated is None:
        raise HTTPException(status_code=404, detail="Order ID findes ikke")

    return updated


#Endpoint til sletning af lejeaftale - har lav priotet