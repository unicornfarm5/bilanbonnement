


## How to run

```
 docker-compose up -d --build

 eller
 
 docker-compose up --build
 (hvis du gerne vil se logs)

```
## How to shut down
```
 docker-compose down

```


UNDER UDVIKLING SKAL DU LAVE EN VENV I HVER MICROSERVICE MAPPE

SØRG FOR AT GÅ IND I HVER MAPPE OG SKRIV
BRUG 
python -m venv venv
source venv/Scripts/activate   # Bash

INSTALLERER DU NOGLE NYE DEPENDECIES, SÅ KØR INDE I MAPPEN

pip freeze > requirements.txt


SÅ VORES DOCKER COMPUTER OGSÅ VED AT DE SKAL MED