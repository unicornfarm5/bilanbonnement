import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
import requests

from config import RENTALSERVICE, CUSTOMERSERVICE


def show_business_page(session_state_from_ui):
    st.write("Velkommen til Business-afdelingen!")

    # Henter dataen en gang
    rentals_data = get_all_rentals(session_state_from_ui) #henter alle udlejninger fra RentalService-API'et

    if not rentals_data:
        st.info("Ingen udlejninger at vise endnu.")
        return

    # Laver Dataframe / data i tabelform
    df = pd.DataFrame(rentals_data)

    st.subheader("Alle udlejninger")
    st.dataframe(df)

    # Tjekker at rental_start findes
    if "rental_start" not in df.columns:
        st.error("Kolonnen 'rental_start' findes ikke i data – kan ikke lave tidsbaserede grafer.")
        return

    # Konverter dato
    df["rental_start"] = pd.to_datetime(df["rental_start"], errors="coerce")
    df = df.dropna(subset=["rental_start"])

    # Tilføjer månedskolonne til graf 2
    df["rental_month"] = df["rental_start"].dt.to_period("M").dt.to_timestamp()

    st.title("Business Dashboards")

    # KPI – Udlejninger i 2024 og valgte måned 
    st.subheader("Nøgletal for salg (udlejninger)")

    current_year = 2024        # fast år
    selected_month = 12        # fast måned her -> december

    df_2024 = df[df["rental_start"].dt.year == current_year]
    total_sales_year = len(df_2024)

    df_2024_month = df[
        (df["rental_start"].dt.year == current_year) &
        (df["rental_start"].dt.month == selected_month)
    ]
    total_sales_month = len(df_2024_month)

    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            label=f"Antal udlejninger i {current_year}",
            value=total_sales_year,
        )
    with col2:
        st.metric(
            label=f"Antal udlejninger i {selected_month:02d}/{current_year}",
            value=total_sales_month,
        )

    #  Graf 1 – Nye kunder over tid (PR. ÅR)
    if "customer_id" in df.columns:
     st.subheader("Nye kunder over tid (pr. år)")

    df_sorted = df.sort_values("rental_start")

    first_rentals = (
        df_sorted.groupby("customer_id")["rental_start"]
        .min()
        .reset_index(name="first_rental")
    )

    # konverter til int og derefter string
    first_rentals["first_year"] = first_rentals["first_rental"].dt.year.astype(str)

    yearly_new_customers = (
        first_rentals.groupby("first_year")
        .size()
        .reset_index(name="new_customers")
    )

    graph1 = px.bar(
        yearly_new_customers,
        x="first_year",
        y="new_customers",
        title="Nye kunder pr. år",
        labels={"first_year": "År", "new_customers": "Antal nye kunder"},
    )

    # tving plotly til at behandle x-aksen som kategori
    graph1.update_layout(xaxis_type='category')

    st.plotly_chart(graph1, use_container_width=True)

    # Graf 2 – Udlejninger pr. måned
    st.subheader("Antal udlejninger pr. måned")

    if "rental_id" in df.columns:
        monthly_rentals = (
            df.groupby("rental_month")["rental_id"]
            .count()
            .reset_index(name="rental_count")
        )
    else:
        monthly_rentals = (
            df.groupby("rental_month")
            .size()
            .reset_index(name="rental_count")
        )

    graph2 = px.bar(
        monthly_rentals,
        x="rental_month",
        y="rental_count",
        title="Udlejninger pr. måned",
        labels={"rental_month": "Måned", "rental_count": "Antal udlejninger"},
    )
    st.plotly_chart(graph2, use_container_width=True)


def get_all_rentals(session_state_from_ui):
    TOKEN = session_state_from_ui.token
    headers = {"Authorization": f"Bearer {TOKEN}"} if TOKEN else {}

    if not session_state_from_ui.role:
        st.error("Du er ikke logget ind")
        return None

    try:
        response = requests.get(f"{RENTALSERVICE}/all_rentals", headers=headers)

        if response.status_code == 200:
            return response.json()
        elif response.status_code in (401, 403):
            st.error("Du har ikke tilladelse til at se denne data... og får fejl 401 eller 403")
        else:
            st.error(f"Fejl: {response.status_code} - {response.text}")

    except Exception as e:
        st.error(f"Kunne ikke forbinde til API: {str(e)}")

    return None