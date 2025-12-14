import uvicorn
from fastapi import FastAPI, HTTPException, Header
from fastapi.security import HTTPBearer
from dotenv import load_dotenv
from damageDatabase import init_db, get_price_from_level, insert_damage, get_damage_history, seed_damages, get_all_damages
from datetime import datetime
from typing import Optional
import os
import jwt

load_dotenv() # Load miljøvariabler
SECRET_KEY = os.getenv("KEY")

app = FastAPI() # Opret FastApi app
init_db() # Initialiser database ved app-start
seed_damages()  # Fyld med test-data
security = HTTPBearer()

# ============ Health Check (Fra chatten) ============
@app.get("/health")
def health():
    """Health check endpoint"""
    return {"status": "ok"}



# --- Rolle tjekker --- # 
    #kopieret fra rentalService
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



# ============= POST route ================
@app.post("/damage")
def create_damage_report(
    data: dict,
    authorization: str = Header(None)
    ):
    # Sikkerhed: Rolle check
        # 1. Tjekker Authorization header
    if authorization is None:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    # 2. Fjern 'Bearer '
    if authorization.startswith("Bearer "):
        auth_token = authorization[7:]
    else:
        auth_token = authorization

    # 3. Udtræk rolle fra JWT
    role, err = get_role_from_token(auth_token)
    if err:
        raise HTTPException(status_code=401, detail=err)

    # 4. Rolle-check - kun medarbedjere i damage skal kunne poste en ny damage rapport
    if role != "damage":
        raise HTTPException(
            status_code=403,
            detail=f"Din rolle: {role} har ikke adgang"
        )

    try:
        # Find pris ud fra damage_levels
        damage_price = get_price_from_level(data['damage_level_id'])
        if damage_price is None:
            raise HTTPException(
                status_code=400,
                detail=f"damage_level_id {data['damage_level_id']} findes ikke"
            )
        
        # Indsæt i database
        damage_id = insert_damage( # hvad sker der her??
            damage_level_id=data['damage_level_id'],
            damage_description=data.get('damage_description', ''),
            damage_price=damage_price,
            licensplate=data['licensplate'],
            order_id=data.get('order_id')
        )

        return{ # og her??
            'damage_report_id': damage_id,
            'damage_price': damage_price,
            'licensplate': data['licensplate'],
            'created_at': datetime.now().isoformat()
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Server fejl: {str(e)}')


# ============= GET route ================
# Er lige nu uden rolle check og alle kan sende requests
@app.get("/damage/all")
def get_all(authorization: str = Header(None)):
        # Sikkerhed: Rolle check
        # 1. Tjekker Authorization header
    if authorization is None:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    # 2. Fjern 'Bearer '
    if authorization.startswith("Bearer "):
        auth_token = authorization[7:]
    else:
        auth_token = authorization

    # 3. Udtræk rolle fra JWT
    role, err = get_role_from_token(auth_token)
    if err:
        raise HTTPException(status_code=401, detail=err)

    # 4. Rolle-check - kun medarbedjere i damage skal kunne se alle skaderapporter
    if role != "damage":
        raise HTTPException(
            status_code=403,
            detail=f"Din rolle: {role} har ikke adgang"
        )

    try:
        damages = get_all_damages()
        if not damages:
            return {
                'message': 'Ingen skader fundet',
                'damages': []
            }
        return {'damages': damages}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Kunne ikke hente alle skader: {str(e)}')



#get damage rapport for car with licens plate
# Er lige nu uden rolle check og alle kan sende requests 
@app.get("/damage/{licens_plate}")
def get_history(
    licens_plate: str,
    authorization: str = Header(None)
    ):
# Sikkerhed: Rolle check
    if authorization is None:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    if authorization.startswith("Bearer "):
        auth_token = authorization[7:]
    else:
        auth_token = authorization
    # 3. Udtræk rolle fra JWT
    role, err = get_role_from_token(auth_token)
    if err:
        raise HTTPException(status_code=401, detail=err)
    # 4. Rolle-check - kun medarbedjere i damage har adgang til at fremsøge skaderapporter på en bestemt bil
    if role != "damage":
        raise HTTPException(
            status_code=403,
            detail=f"Din rolle: {role} har ikke adgang"
        )
    
    try:
        damages = get_damage_history(licens_plate)
        if not damages:
            return {
                'message': f'Ingen skader fundet for {licens_plate}',
                'damages': [] #??
            }
        
        return {'damages': damages} #??
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Kunne ikke hente historik: {str(e)}')

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=5002)
