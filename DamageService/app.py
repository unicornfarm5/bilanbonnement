import uvicorn
import os
import shutil
from pathlib import Path
from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from dotenv import load_dotenv
from damageDatabase import init_db, get_price_from_level, insert_damage, get_damage_history, seed_damages, get_all_damages
from rental_search_api import RentalCheck
from datetime import datetime
from typing import Optional

load_dotenv() # Load miljøvariabler
rental_check = RentalCheck() # opret klientinstans
app = FastAPI() # Opret FastApi app
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

init_db() # Initialiser database ved app-start
seed_damages()  # Fyld med test-data


# ============ Health Check (Fra chatten) ============
@app.get("/health")
def health():
    """Health check endpoint"""
    return {"status": "ok"}

# ============= POST route ================  (Billede delen er taget direkte fra chatten)
@app.post("/damage")
async def create_damage_report(
    licensplate: str = Form(...),
    damage_level_id: int = Form(...),
    damage_description: str = Form(""),
    order_id: int = Form(None),
    image: UploadFile = File(None)
):
    try:
        #Gem billede hvis uploaded
        image_path = None
        if image and image.filename:
            file_path = UPLOAD_DIR / image.filename
    
            # Gem filen
            with file_path.open("wb") as buffer:
                shutil.copyfileobj(image.file, buffer)
    
            image_path = f"uploads/{image.filename}"
        
        # Find pris ud fra damage_levels
        damage_price = get_price_from_level(damage_level_id)
        if damage_price is None:
            raise HTTPException(status_code=400, detail=f"damage_level_id {damage_level_id} findes ikke"
            )
        
        # Indsæt i database
        damage_id = insert_damage( # hvad sker der her??
            damage_level_id=damage_level_id,
            damage_description=damage_description,
            damage_price=damage_price,
            licensplate=licensplate,
            order_id=order_id,
            image_path=image_path
        )

        return{ # og her??
            'damage_report_id': damage_id,
            'damage_price': damage_price,
            'licensplate': licensplate,
            'image_path': image_path,
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
