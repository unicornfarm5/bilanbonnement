import streamlit as st
import requests
from config import DAMAGESERVICE

def show_damage_page(session_state_from_ui):
    TOKEN = session_state_from_ui.token
    headers = {"Authorization": f"Bearer {TOKEN}"} if TOKEN else {}

    if "reload_rentals" not in st.session_state: # genindlæsning af data efter opdatering
        st.session_state.reload_damage = False

    st.title("Skaderapportering og udbedring")
    with st.expander("Find skaderapporter på bil"):
        licens_plate = st.text_input("Indtast nummerplade")
        # --- Get all_damage rapports from licens plate
        if st.button("Hent alle skaderapporter på bil", key="hent_skaderapport") or st.session_state.reload_damage:
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
    
    