import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import requests

from config import RENTALSERVICE

def show_business_page(session_state_from_ui):
    st.write("Velkommen til Business-afdelingen!")
    
    # Tabel over all_rentals
    # Lowkey hører dette til i rentals view lol
    st.dataframe(get_all_rentals(session_state_from_ui))

    st.title("Business Dashboards")
    # graf 1
        # Lav denne graf om så den rent faktisk viser noget der giver mening
    graph1 = px.bar(get_all_rentals(session_state_from_ui), 
                    x="customer_id", y="rental_start", 
                    title="Nye kunder fordelt på leje start", 
                    color_continuous_scale=px.colors.sequential.Oranges)
    st.plotly_chart(graph1)

    # graf 2
    # https://plotly.com/python/pie-charts/
        # Lav denne graf om så den rent faktisk virker lol
    graph2 = px.pie(get_all_rentals(session_state_from_ui), 
                    values='rental_type', names='rental_type',
                    color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(graph2)



# all_rentals fetch
    # Jeg forstår ikke helt om det hører med i ui service eller om det bare burde have sin egen fil her i ui / somewhere
def get_all_rentals(session_state_from_ui):
    TOKEN = session_state_from_ui.token
    headers = {"Authorization": f"Bearer {TOKEN}"} if TOKEN else {}

    if not session_state_from_ui.role: 
                    st.error("Du er ikke logget ind")
    else:
                    try:
                        response = requests.get(f"{RENTALSERVICE}/all_rentals", headers=headers)

                        if response.status_code == 200:
                            #data hapset, så du kan bruge den til noget !!
                            return response.json()
                        
                        elif response.status_code in (401, 403):
                            st.error("Du har ikke tilladelse til at se denne data... og får fejl 401 eller 403")
                        else:
                            st.error(f"Fejl: {response.status_code} - {response.text}")

                    except Exception as e:
                        st.error(f"Kunne ikke forbinde til API: {str(e)}")