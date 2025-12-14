## ✨ACCOUNTSERVICE✨

Ports:
```
   ports:
      - "5010:5000"  // - så port 5010 localt og med docker 5000 (via API GATEWAY)
```

Preedefinerede medarbejdere:
| Afdeling | Rolle - gemmes i JWT | username | password |
| ----------- | ----------- | ----------- | ----------- |
| Dataregistrering | rental | alice | password123 |
| Skaderapportering | damage | bob | password123 |
| Forretningsudvikling | business | carla | password123 |

## Endpoints:
- `post /login` - logger brugere ind og svarer med JWT

## Funktionalitet:
Man kan logge ind som følgende medarbejdere, med tilhørende roller. Rollerne determinerer hvilken frontend der vises, og hvilke funktionaliteter de har adgang til


## Databasedesign
- Databasen bruger SQLite
- Indeholder **3 predefinerede medarbejdere** ved applikationsstart
- Funktionalitet til på nogen måde at ændre i databasen er ikke implementeret.
  
### Entiteter :
```
CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL 
        )
```

### Noter:
- Framework: bruger FLASK
- Grundkoden er fra Claus eksempel - Shopping side microservicecs
- accountservice bruges i frontend:
  - ` POST /login fra app.py` i UIService

    
- Docker klarer selv dependencies fra requirements.txt, så det skal du ikke tænke på
- **Deployment:** the service starts with docker alongside all other services during `docker-compose up`
  - but you can start customerservice as single with `docker-compose up accountservice `

## Filstruktur i accountservice
```
/apigateway
│
├─.gitgnore               # Git notes to not send any .venvs
├─ app.py                 # seeding the database, JWT management, endpoint for login
├─ database.py            # database created and data insert (SQLite)
├─ Dockerfile             # Docker image setup
├─ requirements.txt       # Dependencies & imports til container
└─ README.md              # Documentation
