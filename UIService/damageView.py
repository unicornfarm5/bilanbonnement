import streamlit as st
import pandas as pd
import json
import requests
from config import DAMAGESERVICE

def show_damage_page(session_state_from_ui):
    TOKEN = session_state_from_ui.token
    headers = {"Authorization": f"Bearer {TOKEN}"} if TOKEN else {}

    if "reload_rentals" not in st.session_state: # genindlæsning af data efter opdatering
        st.session_state.reload_damage = False

    st.title("Skaderapportering og udbedring")

    with st.expander("Se alle rapporter"):
        try:
            response = requests.get(
            f"{DAMAGESERVICE}/damage/all", 
            headers=headers
            )
            if response.status_code == 200:
                data = response.json()  # dette er en dict med 'damages'-key
                
                if 'damages' in data and data['damages']:
                    df = pd.DataFrame(data['damages'])
                    st.dataframe(df)  # viser tabel
                else:
                    st.info("Ingen skader fundet.")

            elif response.status_code in (401, 403):
                st.error("Du har ikke tilladelse til at se denne data...")
            else:
                st.error(f"Fejl: {response.status_code} - {response.text}")
        except Exception as e:
                                st.error(f"Kunne ikke forbinde til API: {str(e)}")
    

    # --- Get all_damage rapports from licens plate
    with st.expander("Find skaderapporter på bil"):
        licens_plate = st.text_input("Indtast nummerplade", key="nummerplade_input1")
        if st.button("Hent alle skaderapporter på bil", key="hent_skaderapport") or st.session_state.reload_damage:
                    try:
                        response = requests.get(
                            f"{DAMAGESERVICE}/damage/{licens_plate}", 
                            headers=headers
                            )
                        if response.status_code == 200:
                            data = response.json()  # dette er en dict med 'damages'-key
                            if 'damages' in data and data['damages']:
                                df = pd.DataFrame(data['damages'])
                                st.dataframe(df)  # viser tabel
                            else:
                                st.info("Ingen skader fundet på denne bil")
                    

                        elif response.status_code in (401, 403):
                            st.error("Du har ikke tilladelse til at se denne data...")
                        else:
                            st.error(f"Fejl: {response.status_code} - {response.text}")
                    except Exception as e:
                                st.error(f"Kunne ikke forbinde til API: {str(e)}")
    
    with st.expander("Opret ny skaderapport på bil"):
        licens_plate = st.text_input("Indtast nummerplade", key="nummerplade_input2")
        damage_level= st.selectbox("Skade niveau", ["ingen", "let", "middel", "svær", "kritisk"])
        damge_description_input = st.text_input("Beskriv skaden", key="skade_input")

        #Fra chatten til billeder
        uploaded_file = st.file_uploader("Upload billede af skade", type=["jpg", "jpeg", "png"], key="damage_image")

        #Får damage_level_id ud fra brugerindtastninger så data er på korrekt form når det sendes til db
        damage_levels_map = {
                    "ingen": 1,
                    "let": 2,
                    "middel": 3,
                    "svær": 4,
                    "kritisk": 5
                }
        damage_level_id = damage_levels_map[damage_level]

        #Postes når knap trykkes        
        if st.button("Gem rapport", key="create_damage_rapport"):
            files = {}
            if uploaded_file is not None:
                  files["image"] = (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)
            data = {
                        "damage_level_id" : damage_level_id,
                        "damage_description" : damge_description_input, 
                        "licensplate" : licens_plate
                    }

            try:
                response = requests.post(
                     f"{DAMAGESERVICE}/damage", 
                     headers=headers, 
                     json=data,
                     files=files if files else None
                     )
                if response.status_code == 200: #vi har 200 ok i back for oprettet, selvom man normalt ville have 201 for created. Småting :)
                    st.session_state.reload_rentals = True # genindlæser state for at kunne vise de nye opdateringer
                    st.badge("Skaderapport er gemt", icon=":material/check:", color="green")
                else:
                    st.error("Øv, noget gik galt: " + response.text)
                    #st.error("Tip: Husk at id skal være unikt :) ")
            except Exception as e:
                    st.error(f"Hent IT-servicedesk, den er helt gal: {str(e)}")
