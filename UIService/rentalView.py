from config import RENTALSERVICE
import streamlit as st
import requests

def show_rental_page(session_state_from_ui):    
    TOKEN = session_state_from_ui.token
    headers = {"Authorization": f"Bearer {TOKEN}"} if TOKEN else {}

    st.title("Dataregistrering")
    # --- Get all_rentals
    with st.expander("Vis hele rental-databasen"):
        if not session_state_from_ui.role: 
            st.error("Du er ikke logget ind")
        else:
            try:
                response = requests.get(f"{RENTALSERVICE}/all_rentals", headers=headers)
                if response.status_code == 200:
                    st.dataframe(response.json())
                elif response.status_code in (401, 403):
                    st.error("Du har ikke tilladelse til at se denne data...")
                else:
                     st.error(f"Fejl: {response.status_code} - {response.text}")
            except Exception as e:
                        st.error(f"Kunne ikke forbinde til API: {str(e)}")

    # --- Søg efter bestemt lejeaftale
    with st.expander("Søg: Find lejeaftale eller kunde"):
        st.write("Der burde bare være et søgefelt, burder der ikke ? ")

    # --- Opret ny lejeaftale + post til db ---
    with st.expander("Opret ny kunde"):
        st.header("Opret ny kunde")
        st.write("Kundeinfo")
        #Ting der skal i customer.db kommer her
        navn = st.text_input("Kunde navn")
        email = st.text_input("Email")


    #Felter til lejeaftale - rental.db
    with st.expander("Opret ny lejeaftale"):
        st.header("Opret ny lejeaftale")
        customer_id = st.text_input("Customer ID")
        license_plate = st.text_input("Nummerplade")
        rental_start = st.date_input("Startdato")
        rental_end = st.date_input("Slutdato")
        rental_type = st.selectbox("Type", ["leasing", "abonnement"])
        price_per_month = st.number_input("Pris pr. måned", min_value=2000.0, step=500)
                
        #Postes når knap trykkes        
        if st.button("Gem", key="create_rental_btn"):
            payload = {
                        "customer_id": customer_id,
                        "license_plate": license_plate,
                        "rental_start": str(rental_start),
                        "rental_end": str(rental_end),
                        "rental_type": rental_type,
                        "price_per_month": price_per_month
                    }
            try:
                response = requests.post(f"{RENTALSERVICE}/all_rentals", headers=headers, json=payload)
                if response.status_code == 200:
                    st.success("Lejeaftalen er gemt ")
                else:
                    st.error("Øv, noget gik galt: " + response.text)
                    st.error("Husk at id skal være unikt :) ")
            except Exception as e:
                    st.error(f"Hent IT-servicedesk, den er helt gal: {str(e)}")

    with st.expander("Slet lejeaftale"):
        st.write("funktion not added yet")

