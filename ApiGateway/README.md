
✨Kommunikationsvej gennem services:✨
(forklaret af chat)
UI (browser / frontend) 
   │
   │ POST /accountservice/login → får JWT token
   ▼
API Gateway (localhost:8000)
   │
   │ forward GET /rentalservice/all_rentals + Authorization header
   ▼
RentalService container (rentalservice:5000)
   │
   │ return JSON
   ▼
API Gateway returnerer JSON til UI