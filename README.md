# 👩🏽‍💻✨Step-by-step guide til dig der åbner for første gang✨👩🏽‍💻
 - Du **skal** oprette en fil der hedder .env i RODEN af projektet. I den skal du skrive KEY= og så et eller andet sammenhængende
 - Sørg for at du har docker desktop åbn
 - Så skal du åbne terminalen og skrive: `docker-compose up --build`
 - **Gå ind på localhost:8501 for at se vores frontend**
 - Du **skal** logge ind som en medarbejder. **Se login olysninger i README.md i AccountService**
***

## How to run the app with docker
```
 docker-compose up -d --build

 or
 
 docker-compose up --build
 (✨✨✨  when you wanna see logs (you do under develepment))

```
## How to shut down
```
 ✨✨✨  docker-compose down

```
*Du behøves altså ikke at opsætte .venv eller downloade noget spicy requirements, det er docker der kører det hele ;)*


## Wanna develop with us ?
✨UNDER UDVIKLING HVOR DU VIL KØRE EN APP.PY LOKALT, LAV EN VENV I HVER MICROSERVICE MAPPE
SØRG FOR AT GÅ IND I HVER MAPPE (cd navnPåService) OG SKRIV

        python -m venv venv
        source venv/Scripts/activate   

for at oprette og aktivere en venv
INSTALLERER DU NOGLE NYE DEPENDECIES, SÅ husk at KØRE INDE I MAPPEN
```
        pip freeze > requirements.txt
```
SÅ VORES DOCKER COMPUTER OGSÅ VED AT DINE TILFØJEDE DEPENDECIES SKAL MED
