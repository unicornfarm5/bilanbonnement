# 👩🏽‍💻✨Step-by-step guide til dig der åbner for første gang✨👩🏽‍💻
 - Fork projektet
 - Du **skal** oprette en fil der hedder .env i RODEN af projektet. I den skal du skrive KEY= og så et eller andet sammenhængende
 - Sørg for at du har docker desktop åbn
 - Så skal du åbne terminalen og skrive: `docker-compose up --build`
 - **Gå ind på localhost:8501 for at se vores landingpage frontend**
 - Du **skal** logge ind som en medarbejder for tilgå funktionaliteter og views. **Se login olysninger i README.md i AccountService**
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
✨Under udvikling hvor du vil køre en app.py lokalt, lav et virtuelt miljø ( .venv ) i hver microservice mappe
Guide:
- sørg for at gå ind i hver mappe (cd navnpåservice) og skriv for at oprette og aktivere en venv: 

        python -m venv venv
        source venv/Scripts/activate   


- INSTALLERER DU NOGLE NYE DEPENDECIES, SÅ husk at KØRE INDE I MAPPEN
```
        pip freeze > requirements.txt
```
- Så vores docker computer også ved at dine tilføjede dependecies skal med
