import numpy as np
import numpy_financial as npf
import pandas as pd
import streamlit as st
import streamlit_ext as ste
from streamlit_extras.app_logo import add_logo

for k, v in st.session_state.items():
    st.session_state[k] = v

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

key_list = [
    "SYNC_annual_rent",
    "SYNC_purchase_price",
]

for key in key_list:
    if key not in st.session_state:
        st.session_state[key] = float(0)

add_logo("logo@0.1x.png")

# @st.cache_data
def calculate_npv(
    annual_rental_income,
    initial_investment,
    discount_rate,
    rent_increase_percentage,
    year,
):
    npv = 0
    annual_rent = annual_rental_income
    data = []

    for i in range(year + 1):
        if i == 0:
            npv -= initial_investment
        else:
            annual_rent += annual_rent * (rent_increase_percentage / 100)
            npv += annual_rent / ((1 + discount_rate) ** i)
        data.append([i, annual_rent, npv])

    df = pd.DataFrame(data, columns=["Year", "Annual Rent", "NPV"])
    return df.round(2)


# @st.cache_data
def calculate_npv_positive_year(
    annual_rental_income,
    initial_investment,
    discount_rate,
    rent_increase_percentage,
):
    npv = -initial_investment
    annual_rent = annual_rental_income
    data = []

    year = 0
    while npv < 0:
        data.append([year, annual_rent, npv])
        annual_rent += annual_rent * (rent_increase_percentage / 100)
        npv += annual_rent / (1 + discount_rate) ** (year + 1)
        year += 1

    data.append([year, annual_rent, npv])

    df = pd.DataFrame(data, columns=["Year", "Annual Rent", "NPV"])
    return year, df.round(2)


# @st.cache_data
def calculate_irr_percentage(
    annual_rental_income, initial_investment, rent_increase_percentage, years
):
    cash_flows = [-initial_investment]
    annual_rent = 0

    for year in range(1, years + 1):
        if year == 1:
            annual_rent = annual_rental_income
        else:
            annual_rent += annual_rent * (rent_increase_percentage / 100)
        cash_flows.append(annual_rent)

    cash_flows = np.array(cash_flows)
    irr = npf.irr(cash_flows) * 100

    data = []
    for year in range(years + 1):
        data.append(
            [
                year,
                cash_flows[year],
                npf.irr(cash_flows[: year + 1]) * 100,
            ]
        )

    df = pd.DataFrame(data, columns=["Year", "Annual Rent", "IRR"]).iloc[1:, :]
    return irr, df.round(2)


st.title("NPV and IRR")

ste.number_input(
    label="Estimated Rent Increase (Eg. If rent increases by 10% enter 10)",
    key="rent_increase_percentage",
    step=1e-2,
)

ste.number_input(
    label="""Risk Free Rate
    (1 Year T-Bill yield, Eg. If the yield is 5% enter 5)""",
    key="risk_free_rate",
    step=1e-2,
    format="%f",
)

ste.number_input(
    label="Number of Years",
    key="npv_year",
    step=1,
)


menu = [
    "Net Present Value",
    "Internal Rate of Return",
    "Year in Which NPV > 0 and IRR ≈ Discount Rate",
]

choice = st.selectbox("Options", menu, index=0)

if choice == menu[0]:
    npv_df = calculate_npv(
        st.session_state.SYNC_annual_rent,
        st.session_state.SYNC_purchase_price,
        st.session_state.SYNC_risk_free_rate / 100,
        st.session_state.SYNC_rent_increase_percentage,
        st.session_state.SYNC_npv_year,
    )

    st.dataframe(npv_df.set_index("Year"), use_container_width=True)

    st.download_button(
        label="Download data as CSV",
        data=npv_df.to_csv(index=False),
        file_name="Net Present Value.csv",
    )

elif choice == menu[1]:
    irr, irr_df = calculate_irr_percentage(
        st.session_state.SYNC_annual_rent,
        st.session_state.SYNC_purchase_price,
        st.session_state.SYNC_rent_increase_percentage,
        st.session_state.SYNC_npv_year,
    )

    st.dataframe(irr_df.set_index("Year"), use_container_width=True)

    st.download_button(
        label="Download data as CSV",
        data=irr_df.to_csv(index=False),
        file_name="Internal Rate of Return.csv",
    )

else:
    year, positive_df = calculate_npv_positive_year(
        st.session_state.SYNC_annual_rent,
        st.session_state.SYNC_purchase_price,
        st.session_state.SYNC_risk_free_rate / 100,
        st.session_state.SYNC_rent_increase_percentage,
    )

    temp, irr_df_positive = calculate_irr_percentage(
        st.session_state.SYNC_annual_rent,
        st.session_state.SYNC_purchase_price,
        st.session_state.SYNC_rent_increase_percentage,
        year + 1,
    )

    irr_df_positive["Year"] = irr_df_positive["Year"] - 1
    irr_df_positive.drop(columns=["Annual Rent"], inplace=True)
    final_df = pd.merge(positive_df, irr_df_positive, on="Year", how="left")
    st.metric("Year in Which NPV > 0 and IRR ≈ Discount Rate", year)
    st.dataframe(final_df.set_index("Year"), use_container_width=True)

    st.download_button(
        label="Download data as CSV",
        data=final_df.to_csv(index=False),
        file_name="Positive NPV Year Calc.csv",
    )
