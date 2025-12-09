from config import RENTALSERVICE, CUSTOMERSERVICE
import streamlit as st
import requests

def show_rental_page(session_state_from_ui):    
    TOKEN = session_state_from_ui.token
    headers = {"Authorization": f"Bearer {TOKEN}"} if TOKEN else {}

    if "reload_rentals" not in st.session_state: # genindlæsning af data efter opdatering
        st.session_state.reload_rentals = False

    st.title("Dataregistrering")
    
    col1, col2 = st.columns(2)

    with col1:
        # --- Get all_rentals
        if st.button("Vis alle lejeaftaler", key="hent_ny_data") or st.session_state.reload_rentals:
                try:
                    response = requests.get(
                        f"{RENTALSERVICE}/all_rentals", 
                        headers=headers
                        )
                    if response.status_code == 200:
                        st.dataframe(response.json()) #viser tabel
                    elif response.status_code in (401, 403):
                        st.error("Du har ikke tilladelse til at se denne data...")
                    else:
                        st.error(f"Fejl: {response.status_code} - {response.text}")
                except Exception as e:
                            st.error(f"Kunne ikke forbinde til API: {str(e)}")

    with col2:
        # --- Get all customers
           if st.button("Vis alle kunder", key="hent nyeste customer") or st.session_state.reload_rentals:
                try:
                    response = requests.get(
                        f"{CUSTOMERSERVICE}/all_customers", 
                        headers=headers
                        )
                    if response.status_code == 200:
                        st.dataframe(response.json()) #viser tabel
                    elif response.status_code in (401, 403):
                        st.error("Du har ikke tilladelse til at se denne data...")
                    else:
                        st.error(f"Fejl: {response.status_code} - {response.text}")
                except Exception as e:
                            st.error(f"Kunne ikke forbinde til API: {str(e)}")


    # --- Opret ny lejeaftale + post til db ---
    with st.expander("Opret ny kunde"):
        st.header("Opret ny kunde")
        st.write("Kundeinfo")
        #Ting der skal i customer.db kommer her
        navn = st.text_input("Kunde navn")
        email = st.text_input("Email")

    # --- Opret ny lejeaftale --- 
    #Felter til lejeaftale - rental.db
    with st.expander("Opret ny lejeaftale"):
        st.header("Opret ny lejeaftale")
        customer_id = st.text_input("Customer ID") # kunne laves mere brugervenlig, men det er ikke vores fokus
        license_plate = st.selectbox("Nummerplade",["AB12345", "CT82941", "FD77290", "KM44832", "RV90516"]) #i MVP har vi blot 5 nummerplader tilgængelige på ledige biler i butikken
        rental_start = st.date_input("Startdato")
        rental_end = st.date_input("Slutdato")
        rental_type = st.selectbox("Type af leje", ["leasing", "abonnement"])
        price_per_month = st.number_input("Pris pr. måned", min_value=2000, step=500)
                
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
                response = requests.post(
                     f"{RENTALSERVICE}/all_rentals", 
                     headers=headers, 
                     json=payload
                     )
                if response.status_code == 200:
                    st.session_state.reload_rentals = True # genindlæser state for at kunne vise de nye opdateringer
                    st.badge("Lejeaftalen er gemt", icon=":material/check:", color="green")
                else:
                    st.error("Øv, noget gik galt: " + response.text)
                    st.error("Tip: Husk at id skal være unikt :) ")
            except Exception as e:
                    st.error(f"Hent IT-servicedesk, den er helt gal: {str(e)}")

    # -- Opdater lejeaftale --- 
    with st.expander("Opdater lejeaftale: lejeperiode slutdato"):
         st.header("Opdater slutdato for lejeperiode i ordre") 
         order_id = st.text_input("Angiv ordre id til den ordre der skal rettes")
         new_rental_end = st.date_input("Ny slutdato")

         if st.button("Gem opdatering", key="update_rental_btn"):
                payload = {
                            "rental_end": str(new_rental_end)
                        }
                try:
                    response = requests.put(
                        f"{RENTALSERVICE}/all_rentals/update/{order_id}", 
                        headers=headers, 
                        json=payload
                        )
                    if response.status_code == 200:
                        st.badge("Opdateret slutdato er gemt", icon=":material/check:", color="green")
                        st.session_state.reload_rentals = True #så nye opdateringer kan ses på siden
                    else:
                        st.error("Øv, noget gik galt: " + response.text)
                        st.error("Tip: Har du givet det korrekte id?")
                except Exception as e:
                        st.error(f"Hent IT-servicedesk, den er helt gal: {str(e)}")


    with st.expander("Slet lejeaftale"):
        st.write("IT-afdelingen arbejder stadig på denne funktionalitet")


