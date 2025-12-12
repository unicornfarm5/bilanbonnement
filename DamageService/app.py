import uvicorn
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from damageDatabase import init_db, get_price_from_level, insert_damage, get_damage_history, seed_damages, get_all_damages
from rental_search_api import RentalCheck
from datetime import datetime
from typing import Optional

load_dotenv() # Load miljøvariabler
rental_check = RentalCheck() # opret klientinstans
app = FastAPI() # Opret FastApi app
init_db() # Initialiser database ved app-start
seed_damages()  # Fyld med test-data


# ============ Health Check (Fra chatten) ============
@app.get("/health")
def health():
    """Health check endpoint"""
    return {"status": "ok"}

# ============= POST route ================
@app.post("/damage")
def create_damage_report(data: dict):
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
@app.get("/damage/all")
def get_all():
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
@app.get("/damage/{licens_plate}")
def get_history(licens_plate: str): #Henter alle skadehistorik for licensplate
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
