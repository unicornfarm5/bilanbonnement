import streamlit as st
import requests 
import jwt  # pip install PyJWT

#this is not sure lol
APIGATEWAY = "http://apigateway:8000"

# Fra Claus
# gemmer variabler mellem re-runs så brugeren kan forblive logget ind selvom appen reloader
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
                        f"{APIGATEWAY}/login",
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
                            st.session_state.role = user_role
                            st.success("Login successful!")
                            st.rerun()
                        else:
                            st.error("Invalid token received from server")
                    else:
                        st.error(response.json().get('message', 'Login failed'))
                except Exception as e:
                    st.error(f"Error connecting to account service: {str(e)}")

 
# Main content
st.title("her vises noget der ændres efter hvilken rolle du har")

if st.session_state.role == "admin":
    st.button("Delete record")
elif st.session_state.role == "editor":
    st.button("Edit record")
else:  # reader
    st.write("Read-only view")


