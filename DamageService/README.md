
## ✨DAMAGESERVICE ✨

Ports:
```
   ports:
      - "5002:5002"  // - så port 5002 både localt og med docker (via API GATEWAY)
```   
## Endpoints:
- ` POST  /damage` - tilføjer ny skaderapport (rolle = "damage" har adgang)
- ` GET /damge/all - henter alle skaderapporter (rolle = "damage") har adgang
- ` GET  /damage/{licens_plate} - henter alle skaderapporter fra en bil via nummerplade (rolle = "damage") har adgang

---
## Funktionalitet:
damageservice bygger og fylder skaderapport-databasen damage.db, samt damage_levels.db, 
som er en lille tabel der bruges til at håndtere grad af skader og tilhørende pris for fix
Servicen indeholder flere endpoints til håndtering af databaserne og håndterer også hvilken medabejderrolle der har adgang til at tilgå endpoints'ne. 


## Databasedesign
- Databasen bruger SQLite
- Indeholder **6** skaderapporter ved applikationsstart på hver sin bil
- Der kan af bob tilføjes flere skaderapporter på samme bil

### Entiteter :

        CREATE TABLE IF NOT EXISTS damage_levels (
            level_id INTEGER PRIMARY KEY AUTOINCREMENT,
            level_name TEXT UNIQUE NOT NULL,
            price INT NOT NULL
        )

og
    
        CREATE TABLE IF NOT EXISTS damage (
            damage_report_id INTEGER PRIMARY KEY AUTOINCREMENT,
            damage_level_id INTEGER NOT NULL,
            damage_description TEXT,
            damage_price INT,
            licensplate TEXT NOT NULL,
            order_id INT,
            created_at DATETIME DEFAULT current_timestamp,
            FOREIGN KEY (damage_level_id) REFERENCES damage_levels(level_id)
        )
```
