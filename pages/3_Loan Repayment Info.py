import io

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
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
    "SYNC_interest_rate",
    "SYNC_loan_amount",
    "SYNC_loan_term",
]

for key in key_list:
    if key not in st.session_state:
        st.session_state[key] = float(0)

add_logo("logo@0.1x.png")

# @st.cache_data
def generate_amortization_table(principal, interest_rate, num_payments):
    table = pd.DataFrame(
        columns=[
            "Payment Period",
            "Remaining Balance",
            "Monthly Interest Payment",
            "Monthly Principal Payment",
            "Monthly Payment",
        ]
    )

    try:
        monthly_interest_rate = interest_rate / 12 / 100
        monthly_payment = (
            principal
            * monthly_interest_rate
            / (1 - (1 + monthly_interest_rate) ** -num_payments)
        )

        remaining_balance = principal

        for period in range(1, num_payments + 1):
            monthly_interest_payment = (
                remaining_balance * monthly_interest_rate
            )

            monthly_principal_payment = (
                monthly_payment - monthly_interest_payment
            )

            remaining_balance = remaining_balance - monthly_principal_payment

            row = {
                "Payment Period": period,
                "Remaining Balance": remaining_balance,
                "Monthly Interest Payment": monthly_interest_payment,
                "Monthly Principal Payment": monthly_principal_payment,
                "Monthly Payment": monthly_payment,
            }

            table = pd.concat(
                [table, pd.DataFrame(row, index=[0])], ignore_index=True
            ).round(2)

    except ZeroDivisionError:
        # st.info("Empty Table")
        return table

    return table


def plot_amortization_chart(dataframe):
    # Extract data from the dataframe
    payment_periods = dataframe["Payment Period"]
    remaining_balances = dataframe["Remaining Balance"]
    interest_payments = dataframe["Monthly Interest Payment"]
    principal_payments = dataframe["Monthly Principal Payment"]
    # num_payments = len(payment_periods)
    # Create the amortization chart
    fig = go.Figure()

    # Plot remaining balances on the left y-axis
    fig.add_trace(
        go.Scatter(
            x=payment_periods,
            y=remaining_balances,
            mode="lines",
            name="Remaining Balances",
        )
    )

    # Create a second y-axis for interest payments and principal payments
    fig.update_layout(
        yaxis=dict(title="Remaining Balance"),
        yaxis2=dict(
            title="Interest/Principal Payments",
            side="right",
            overlaying="y",
            showgrid=False,
        ),
    )

    # Plot interest payments and principal payments on the right y-axis
    fig.add_trace(
        go.Scatter(
            x=payment_periods,
            y=interest_payments,
            mode="lines",
            name="Interest Payments",
            yaxis="y2",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=payment_periods,
            y=principal_payments,
            mode="lines",
            name="Principal Payments",
            yaxis="y2",
        )
    )

    fig.update_layout(
        xaxis_title="Payment Period (Months)",
        legend_title="Payment Type",
        showlegend=True,
        height=600,
        width=850,
        modebar={"remove": ["toImage"]},
        hovermode="x",
        colorway=['#1f77b4', '#ff7f0e', '#2ca02c']
    )

    fig.update_yaxes(automargin=True)
    st.plotly_chart(fig)

    return fig


st.title("Loan Repayment Info")


st.write("")

if "login" in st.session_state:
    # st.write(st.session_state["login"])
    if st.session_state["login"] == 1:
        st.write("Logged In")


table = generate_amortization_table(
    st.session_state.SYNC_loan_amount,
    st.session_state.SYNC_interest_rate,
    int(st.session_state.SYNC_loan_term) * 12,
)
st.subheader("Amortization Chart")
fig = plot_amortization_chart(table.reset_index())

# Create an in-memory buffer
buffer = io.BytesIO()
fig.write_image(file=buffer, format="png")

st.download_button(
    label="Download Image",
    data=buffer,
    file_name="Amortization Chart.png",
)


st.subheader("Amortization Table")
st.write("")
st.dataframe(table.set_index("Payment Period"))


st.download_button(
    label="Download data as CSV",
    data=table.to_csv(index=False),
    file_name="Amortization Table.csv",
)
