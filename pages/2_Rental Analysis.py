import streamlit as st
from streamlit_extras.app_logo import add_logo

for k, v in st.session_state.items():
    st.session_state[k] = v
# hide_st_style = """
#             <style>
#             #MainMenu {visibility: hidden;}
#             footer {visibility: hidden;}
#             header {visibility: hidden;}
#             </style>
#             """
# st.markdown(hide_st_style, unsafe_allow_html=True)

key_list = [
    "SYNC_annual_rent",
    "SYNC_loan_amount",
    "SYNC_purchase_price",
    "initial_cash_invested",
    "monthly_payment",
    "operating_expense",
    "operating_revenue",
    "currency",
]

for key in key_list:
    if key not in st.session_state:
        st.session_state[key] = float(0)

add_logo("logo@0.1x.png")

currency = st.session_state["currency"]

st.title("Rental Analysis")
purchase_price = st.session_state.SYNC_purchase_price

noi = st.session_state["noi"] = (
    st.session_state["operating_revenue"]
    - st.session_state["operating_expense"]
)


monthly_payment = st.session_state["monthly_payment"]
cash_flow = st.session_state["cash_flow"] = noi - (monthly_payment * 12)
cash_flow_month = round(cash_flow / 12, 2)

if cash_flow > 0:
    cf_str = f":green[{currency}]" + " " + f":green[{cash_flow}]"
    cfm_str = f":green[{currency}]" + " " + f":green[{cash_flow_month}]"
else:
    cf_str = f":red[{currency}]" + " " + f":red[{cash_flow}]"
    cfm_str = f":red[{currency}]" + " " + f":red[{cash_flow_month}]"


body1 = """
Net Operating Income: Property's income after expenses (excluding debt and taxes).

Cash Flow: Remaining money after all expenses (including debt and taxes) are deducted from income.
"""

np_body = f"""
|                      |      Monthly      |         Annual         |
|----------------------|:-----------------:|:----------------------:|
| Net Operating Income | {round(noi/12,2)} |          {noi}         |
| (-) Loan Repayment   | {monthly_payment} | {monthly_payment * 12} |
| Cash Flow            |     {cfm_str}     |        {cf_str}        |
"""
st.subheader("Net Performance")
st.write(np_body)
st.write("")
st.write("")
st.write(body1)

try:
    dcr = st.session_state["debt_coverage_ratio"] = round(
        noi / (monthly_payment * 12), 2
    )
except ZeroDivisionError:
    dcr = 0

try:
    rtv = st.session_state["rent_to_value"] = round(
        (st.session_state.SYNC_annual_rent / purchase_price) * 100, 2
    )

except ZeroDivisionError:
    rtv = 0

try:
    cap_rate = st.session_state["cap_rate"] = round(
        (noi / purchase_price) * 100, 2
    )
except ZeroDivisionError:
    cap_rate = 0

try:
    coc_return = st.session_state["cash_on_cash_return"] = round(
        (cash_flow / st.session_state["initial_cash_invested"]) * 100, 2
    )
except ZeroDivisionError:
    coc_return = 0

try:
    ltv = (
        round(
            st.session_state.SYNC_loan_amount
            / st.session_state.SYNC_purchase_price,
            4,
        )
        * 100
    )
except ZeroDivisionError:
    ltv = 0


if dcr > 1.2:
    dcr_str = f":green[{dcr}]"
elif dcr > 1:
    dcr_str = f":yellow[{dcr}]"
else:
    dcr_str = f":red[{dcr}]"

if rtv > 1.5:
    rtv_str = f":green[{rtv}%]"
elif rtv > 1:
    rtv_str = f":yellow[{rtv}%]"
else:
    rtv_str = f":red[{rtv}%]"

if cap_rate > 8:
    cap_rate_str = f":green[{cap_rate}%]"
elif cap_rate > 4:
    cap_rate_str = f":yellow[{cap_rate}%]"
else:
    cap_rate_str = f":red[{cap_rate}%]"

if coc_return > 10:
    coc_return_str = f":green[{coc_return}%]"
elif coc_return > 5:
    coc_return_str = f":yellow[{coc_return}%]"
else:
    coc_return_str = f":red[{coc_return}%]"

if ltv > 80:
    ltv_str = f":red[{ltv}%]"
elif ltv > 60:
    ltv_str = f":yellow[{ltv}%]"
else:
    ltv_str = f":green[{ltv}%]"

body2 = """
Debt Coverage Ratio (DCR): Measures property's ability to cover debt payments.

Rent-to-Value Ratio: Compares annual rental income to property value as a percentage.

Capitalization Rate (Cap Rate): Evaluates property profitability based on income and value.

Cash on Cash Return: Assesses ROI by comparing cash flow to initial investment.

Loan-to-Value (LTV) is the ratio between the loan amount and the appraised value or purchase price of an asset, expressed as a percentage.
"""

fi_body = f"""
|                     |       Value      |
|:-------------------:|:----------------:|
| Debt Coverage Ratio |     {dcr_str}    |
| Rent To Value       |     {rtv_str}    |
| Capitalization Rate |  {cap_rate_str}  |
| Cash on Cash Return | {coc_return_str} |
| Loan To Value       |     {ltv_str}    |
"""
st.write("")
st.write("")
st.subheader("Financial Indicators")
st.write(fi_body)
st.write("")
st.write("")
st.write(body2)


## Year wise Ammorization chart
# def plot_amortization_chart(principal, interest_rate, loan_term):
#     # Calculate annual interest rate and number of payments
#     annual_interest_rate = interest_rate
#     num_payments = loan_term

#     # Calculate annual payment amount
#     annual_payment = (principal * annual_interest_rate) / (
#         1 - (1 + annual_interest_rate) ** -num_payments
#     )

#     # Create arrays to store data for the chart
#     remaining_balances = [principal]
#     interest_payments = []
#     principal_payments = []
#     cumulative_interest = 0

#     # Calculate the remaining balances, interest payments, and principal payments for each payment period
#     for _ in range(num_payments):
#         interest_payment = remaining_balances[-1] * annual_interest_rate
#         principal_payment = annual_payment - interest_payment
#         remaining_balance = remaining_balances[-1] - principal_payment
#         cumulative_interest += interest_payment

#         interest_payments.append(round(interest_payment, 0))
#         principal_payments.append(round(principal_payment, 0))
#         remaining_balances.append(round(remaining_balance, 0))

#     # Create the amortization chart
#     fig = go.Figure()

#     # Plot remaining balances on the left y-axis
#     fig.add_trace(
#         go.Scatter(
#             x=list(range(1, num_payments + 1)),
#             y=remaining_balances[:-1],
#             mode="lines",
#             name="Remaining Balances",
#         )
#     )

#     # Create a second y-axis for interest payments and principal payments
#     fig.update_layout(
#         yaxis=dict(title="Remaining Balance"),
#         yaxis2=dict(
#             title="Interest/Principal Payments",
#             side="right",
#             overlaying="y",
#             showgrid=False,
#         ),
#     )

#     # Plot interest payments and principal payments on the right y-axis
#     fig.add_trace(
#         go.Scatter(
#             x=list(range(1, num_payments + 1)),
#             y=interest_payments,
#             mode="lines",
#             name="Interest Payments",
#             yaxis="y2",
#         )
#     )
#     fig.add_trace(
#         go.Scatter(
#             x=list(range(1, num_payments + 1)),
#             y=principal_payments,
#             mode="lines",
#             name="Principal Payments",
#             yaxis="y2",
#         )
#     )

#     fig.update_layout(
#         title="Amortization Chart",
#         xaxis_title="Payment Period (Years)",
#         legend_title="Payment Type",
#         showlegend=True,
#         height=600,
#         width=850,
#         modebar={"remove": ["toImage"]},
#         hovermode="x",
#     )

#     fig.update_yaxes(automargin=True)
#     st.plotly_chart(fig)
