
## ✨API GATEWAY ✨

Ports:
```
   ports:
      - "8000:5000"  // - så port 8000 localt - port 5000 med docker
```   
## Endpoints:
- ` "GET", "POST", "PUT", "DELETE"  /<service>/<path:path> ` - alle services kan kalde  `apiGateWay(service, path): `
---
## Funktionalitet:
API Gateway **håndterer alt kommunikation mellem services** og bruges ved hjælp af funktionen der tager imod service + path. 

*`apiGateway(service, path):` tager ikke imod UIService, da UI kun sender requests og ikke selv indeholder nogen endpoints.*
Listen over services der kan bruge apiGateway er predefineret i service-mappet herunder. Det gør funktionen simpel at kalde uden at man skal huske nogen porte og giver ensformighed. 
```
services = {
    "accountservice": "http://accountservice:5000",
    "rentalservice": "http://rentalservice:5000",
    "customerservice": "http://customerservice:5000",
    "damageservice": "http://customerservice:5002"
}
```

### Noter:
- Framework: API Gateway bruger Flask
- Docker klarer selv dependencies fra requirements.txt, så det skal du ikke tænke på
- **Deployment:** the service starts with docker alongside all other services during `docker-compose up`
- - but you can start API Gateway as single with `docker-compose up apigateway`


## Filstruktur i API Gateway
```
/apigateway
│
├─.gitgnore               # Git notes to not send any .venvs
├─ app.py                 # funktionality and the gateway
├─ Dockerfile             # Docker image setup
├─ requirements.txt       # Dependencies & imports til container
└─ README.md              # Documentation
```
