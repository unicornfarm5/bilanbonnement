import streamlit as st
import requests 
import jwt  
from rentalView import show_rental_page #funktion til rental view

#Service overblik fra CONFIG FILEN HVOR LISTEN FINDES 
from config import RENTALSERVICE, ACCOUNTSERVICE


# Fra Claus
# gemmer variabler mellem re-runs så brugeren kan forblive logget ind selvom appen reloader ?

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'auth_token' not in st.session_state:
    st.session_state.auth_token = None

# login funktion sker i sidebar
with st.sidebar:
    st.title("Account")

    if not st.session_state.logged_in:
            st.subheader("Login")
            login_username = st.text_input("Username", key="login_username")
            login_password = st.text_input("Password", type="password", key="login_password")

            if st.button("Login"):
                try:
                    response = requests.post(
                        f"{ACCOUNTSERVICE}/login",
                        json={"username": login_username, "password": login_password}
                    )

                    if response.status_code == 200:
                        # Extract Bearer token from Authorization header
                        auth_header = response.headers.get('Authorization')
                        if auth_header and auth_header.startswith("Bearer "):
                            token = auth_header.split(" ")[1]
                            decoded_token = jwt.decode(token, options={"verify_signature": False})
                            user_role = decoded_token.get("role", "reader")  # default to reader if no role

                            st.session_state.logged_in = True
                            st.session_state.username = login_username
                            st.session_state.auth_token = auth_header
                            st.session_state.token = token #prøver lige at gemme token her
                            st.session_state.role = user_role
                            st.success("Login successful!")
                            st.rerun()
                        else:
                            st.error("Invalid token received from server")
                    else:
                        st.error(response.json().get('message', 'Login failed'))
                except Exception as e:
                    st.error(f"Error connecting to account service: {str(e)}")
                    #print("status kode: " + str(response.status_code))
                    #print(" response text " + response.text)

 

# Tjek af rolle, laver view efter det og sender TOKEN med (via st.session_state)
if 'role' in st.session_state:
    st.write(f"Du ser ud til at være i denne afdeling: : {st.session_state.role}")

    SESSION_STATE = st.session_state

    if st.session_state.role == "rental":
        show_rental_page(SESSION_STATE) #funktion fra rentalView.py

        """ kommer snart :) 
    #elif st.session_state.role == "damage": 
        #show_damage_page(SESSION_STATE)

    elif st.session_state.role == "business": 
            show_reader_page(SESSION_STATE)
        """
    else:
        st.write("Ingen view til din rolle endnu :( ")




#gammel måde for referance (her var det jo kun rental)
"""
    if st.session_state.role  == "rental":
        TOKEN = st.session_state.token
        headers = {"Authorization": f"Bearer {TOKEN}"} if TOKEN else {}
        if st.button("Vis hele rental-databasen"):
            if not st.session_state.role: 
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

    elif st.session_state.role == "reader":
        st.write("Du er ikke logget ind eller er ikke i en relevant afdeling")
"""