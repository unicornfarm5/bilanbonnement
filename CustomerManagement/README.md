
## ✨CUSTOMER MANAGEMENT - in docker: customerservice ✨

Ports:
```
   ports:
      - "5001:5000"  // - så port 5001 localt - port 5000 med docker
```   
## Endpoints:
- ` GET  /all_customers` - henter alt kundedata. Kun dataregistrering (rolle = "rental") har adgang
- ` GET  /all_customers_id` - henter kun customer_id og order_id fra databasen (rolle = "business") har adgang

---
## Funktionalitet:
customerservice indeholder kundedatabasen og endpoints til at tilgå denne. Kun `GET /all_customers` giver adgang til alt kundedata, så personlige oplysninger beskyttes. 

## Databasedesign
- Databasen bruger SQLite
- Indeholder 18 kunder ved applikationsstart
- Funktionalitet til tilføjelse, rettelse eller sletning af kunder er ikke implementeret i MVP
### Entiteter :
```
CREATE TABLE customer (
            customer_id TEXT PRIMARY KEY,
            customer_name TEXT NOT NULL,
            customer_email TEXT NOT NULL,
            customer_phone INTEGER,
            order_id INTEGER,
            FOREIGN KEY(order_id) REFERENCES rental(order_id)
        )
```

### Noter:
- Framework: bruger FASTapi
- Dataen fremvises i frontend og servicen kaldes med og fra:
  - ` GET /all_customers_id  ` i `businesView.py` i UIService
  - ` GET /all_customers  ` i `rentalView.py` i UIService
    
- Docker klarer selv dependencies fra requirements.txt, så det skal du ikke tænke på
- **Deployment:** the service starts with docker alongside all other services during `docker-compose up`
  - but you can start customerservice as single with `docker-compose up customerservice`

## Filstruktur i customerservice
```
/apigateway
│
├─.gitgnore               # Git notes to not send any .venvs
├─ app.py                 # seeding the database, endpoints
├─ database.py            # database created and data insert (SQLite)
├─ Dockerfile             # Docker image setup
├─ requirements.txt       # Dependencies & imports til container
└─ README.md              # Documentation
