## ✨UISERVICE ✨

Ports:
```
   ports:
      - "8501:8501"  // - så port 8501 både localt og med docker (via API GATEWAY)
```   

## Funktionalitet:
Streamlit frontend med rollebestmete views, og login funktion. 
Hvert view (rental, damage, business) har deres egen fil til indhold på siden, der kaldes i app.py med SESSION_STATE som parameter, så disse filer kender til rolle udfra JWT


### Noter:
- Framework: bruger streamlit
- Når denne service skal finde de andre, gør den det via config.py filen
- UI kalder alle endpoints

  
- Docker klarer selv dependencies fra requirements.txt, så det skal du ikke tænke på
- **Deployment:** the service starts with docker alongside all other services during `docker-compose up`
  - but you can start customerservice as single with `docker-compose up uiservice `

## Filstruktur i uiservice
```
/apigateway
│
├─.gitgnore               # Git notes to not send any .venvs
├─ app.py                 # landingpage/baggrundsside, login frontend og sender requests til POST accountservice/login 
├─ businessView.py        # Frontend view og funktionalitet til business rolle og sender requests udfra business-rolle
├─ rentalView.py          # Frontend view og funktionalitet til rental rolle og sender requests udfra rental-rolle
├─ damageView.py          # Frontend view og funktionalitet til damge rolle og sender requests udfra damage-rolle
├─ image.pgn              # image for logo in footer
├─ config.py              # list of all services and their ports to APIGateway for easy reference when making requests
├─ Dockerfile             # Docker image setup
├─ requirements.txt       # Dependencies & imports til container
└─ README.md              # Documentation


