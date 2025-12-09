import requests
import os
from dotenv import load_dotenv

# Klienten der taler til RentalService (laver HTTP-kald og tjekker om order/plade findes).

class RentalCheck:
    def __init__(self):
         #Fra chatten: Hent URL fra miljøvariabel eller default til localhost
        self.base_url = os.getenv('RENTAL_SERVICE_URL', 'http://localhost:5001')
        self.timeout = 2  # timeout på 2 sekunder

    """Tjekker om order_id findes i RentalService"""
    def validate_order_id(self, order_id):
        try:
            response = requests.get(
                f"{self.base_url}/rentals/{order_id}",
                timeout=self.timeout
            )
            if response.status_code == 200: #Hvis order_id findes
                return True
            elif response.status_code == 404: #Hvis order_id ikke findes
                return False
            else:
                raise Exception(f"RentalService fejl: {response.status_code}")
        except requests.Timeout:
            raise Exception("RentalService timeout")
        except requests.RequestException as e:
            raise Exception(f"Kunne ikke nå RentalService: {str(e)}")
    
    def validate_license_plate(self, licens_plate):
        try:
            response = requests.get(
               f"{self.base_url}/rentals/",
               params={'licens_plate': licens_plate}, #???
               timeout=self.timeout 
            )
            if response.status_code == 200: #Hvis licens_plate findes
                data = response.json()
                # tjek hvis der er mindst én rental med denne nummerplade
                if isinstance(data, list) and len(data) > 0: #Hvis licens_plate ikke findes
                    return True
                return False
            elif response.status_code == 404:
                return False
            else:
                 raise Exception(f"RentalService fejl: {response.status_code}")
        except requests.Timeout:
            raise Exception("RentalService timeout")
        except requests.RequestException as e:
            raise Exception(f"Kunne ikke nå RentalService: {str(e)}")










