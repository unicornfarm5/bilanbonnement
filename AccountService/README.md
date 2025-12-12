## AccountService

### Om:
Man kan logge ind som følgende medarbejdere, med tilhørende roller. Rollerne determinerer hvilken frontend der vises, og hvilke funktionaliteter de har adgang til

| Afdeling | Rolle | username | password |
| ----------- | ----------- |
| Dataregistrering | rental | alice | password123 |
| Skaderapportering | damage | bob | password123 |
| Forretningsudvikling | business | carla | password123 |

Endpoints:
- `post /login` - logger brugere ind



### Noter:
Grundkoden er fra Claus eksempel - Shopping side microservicecs