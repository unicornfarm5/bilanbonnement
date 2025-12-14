
## ✨RENTALSERVICE ✨

Ports:
```
   ports:
      - "5000:5000"  // - så port 5000 både localt og med docker (via API GATEWAY)
```   
## Endpoints:
- ` GET  /all_rentals` - henter alle lejeaftaler (rolle in ["rental", "business"]) har adgang)
- ` POST /all_rentals - opretter en ny lejeaftale (rolle = "rental") har adgang
- ` PUT  /all_rentals/update/{order_id} - opdatering af lejeaftale udfra order_id.(rolle = "rental") har adgang

---
## Funktionalitet:
rentalservice bygger og fylder kundedatabasen retal.db. Servicen indeholder flere endpoints til håndtering af databasen og håndterer også hvilke medabejderroller der har adgang til at tilgå endpoints'ne. 
### Note til basemodeller i app.py
Klassen RentalInput er en Basemodel for lejeaftaler (rentals), der gør det lettere at holde styr på alle entiteter i databasen. 
```   
class RentalInput(BaseModel):
    customer_id: str
    license_plate: str
    rental_start: str
    rental_end: str
    rental_type: str
    price_per_month: float
```   
Den bruges her i 
```
@app.post("/all_rentals")
      def post_to_all_rentals(
      rental: RentalInput,  # <-- Her modtages alle felter udfra klasen RentalInput
      authorization: str = Header(None)
      ):
```
og sørger altså for at alle entiteter kommer med på en let og overskuelig måde, hvor vi slipper for at sende hver entitet gennem systemet som argument. Det skaber struktur. 


Til opdatering er det ikke alle entiteter i en rental, der skal kunne opdateres. Vi har valgt at customer_id og rental_start ikke skal kunne opdateres, så det ikke kan ændres når først der er indgået en lejeaftale. 
Vi byggede kun en BaseModel til opdatering af hvilket som helst af de mulige felter, derfor ses at alle felter i teorien kan være tomme. Klassen UpdateRetalInput bruges i `PUT /all_rentals/update/{order_id}`
```   
class UpdateRentalInput(BaseModel):
    license_plate: str | None = None
    rental_end: str | None = None
    rental_type: str | None = None
    price_per_month: float | None = None
```   


## Databasedesign
- Databasen bruger SQLite
- Indeholder **150** lejeaftaler ved applikationsstart
- Funktionalitet til sletning af lejeaftaler er ikke implementeret i MVP
### Entiteter :
```
 CREATE TABLE rental (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id TEXT UNIQUE NOT NULL,
            license_plate TEXT NOT NULL,
            rental_start DATE NOT NULL,
            rental_end DATE NOT NULL,
            rental_type TEXT NOT NULL CHECK (rental_type IN ('leasing', 'abonnement')),
            price_per_month REAL NOT NULL
        )
```

### Noter:
- Framework: bruger FASTapi
- Dataen fremvises i frontend og servicen kaldes med og fra:
  - ` GET /all_rentals fra rentalView.py `i UIService
  - ` GET /all_rentals fra businessView.py `i UIService
  - ` POST /all_rentals fra rentalView.py` i UIService
  - ` PUT /all_rentals/update/{order_id} fra rentalView.py` i UIService

    
- Docker klarer selv dependencies fra requirements.txt, så det skal du ikke tænke på
- **Deployment:** the service starts with docker alongside all other services during `docker-compose up`
  - but you can start customerservice as single with `docker-compose up rentalservice `

## Filstruktur i rentalservice
```
/apigateway
│
├─.gitgnore               # Git notes to not send any .venvs
├─ app.py                 # seeding the database, endpoints and BaseModels for rentals
├─ rentalDatabase.py      # database created and data insert (SQLite)
├─ Dockerfile             # Docker image setup
├─ requirements.txt       # Dependencies & imports til container
└─ README.md              # Documentation
