import streamlit as st
import requests
from config import DAMAGESERVICE

def show_damage_page(session_state_from_ui):
    TOKEN = session_state_from_ui.token
    headers = {"Authorization": f"Bearer {TOKEN}"} if TOKEN else {}

    if "reload_rentals" not in st.session_state: # genindlæsning af data efter opdatering
        st.session_state.reload_rentals = False

    st.title("Dataregistrering")

    licens_plate = st.text_input("Angiv licensplate")
    # --- Get all_rentals
    if st.button("Vis alle lejeaftaler", key="hent_ny_data") or st.session_state.reload_rentals:
                try:
                    response = requests.get(
                        f"{DAMAGESERVICE}/damage/{licens_plate}", 
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