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











