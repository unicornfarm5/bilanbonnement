from config import RENTALSERVICE
import streamlit as st
import requests

def show_rental_page(session_state_from_ui):    
    TOKEN = session_state_from_ui.token
    headers = {"Authorization": f"Bearer {TOKEN}"} if TOKEN else {}
    if st.button("Vis hele rental-databasen"):
                if not session_state_from_ui.role: 
                    st.error("Du er ikke logget ind ordenligt tror vi")
                else:
                    try:
                        response = requests.get(f"{RENTALSERVICE}/all_rentals", headers=headers)

                        if response.status_code == 200:
                            st.write(response.json())
                        elif response.status_code in (401, 403):
                            st.error("Du har ikke tilladelse til at se denne data... ")
                        else:
                            st.error(f"Fejl: {response.status_code} - {response.text}")

                    except Exception as e:
                        st.error(f"Kunne ikke forbinde til API: {str(e)}")