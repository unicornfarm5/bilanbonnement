## How to run the app with docker
```
 docker-compose up -d --build

 or
 
 docker-compose up --build
 (when you wanna see logs (you do))

```
## How to shut down
```
 docker-compose down

```
Du behøves altså ikke at downloade noget spicy, det er docker der kører det hele :)



Guide til dig der åbner for første gang
 - Du skal oprette en fil der hedder .env i RODEN af projektet. I den skal du skrive KEY= og så et eller andet sammenhængende
 - Så skal du åbne terminalen og skrive:        docker-compose up --build
 - Gå ind på localhost/8501 for at se vores frontend
 - Nu kan du logge ind som en af medarbejderene. Se mere herom i README.md i AccountService




UNDER UDVIKLING SKAL DU LAVE EN VENV I HVER MICROSERVICE MAPPE (lige nu har vi dog glemt at sætte dem i .gitignore så er ikke sikker på om i behøves det. Det fikses senere)
SØRG FOR AT GÅ IND I HVER MAPPE (cd navnPåService) OG SKRIV

        python -m venv venv
        source venv/Scripts/activate   

for at oprette og aktivere en venv
INSTALLERER DU NOGLE NYE DEPENDECIES, SÅ husk at KØRE INDE I MAPPEN
        pip freeze > requirements.txt

SÅ VORES DOCKER COMPUTER OGSÅ VED AT DINE TILFØJEDE DEPENDECIES SKAL MED