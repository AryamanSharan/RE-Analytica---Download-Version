import streamlit as st
import streamlit_ext as ste
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

# EMI calculation
def calculate_monthly_payment(principal, interest_rate, duration):
    if duration == 0 or interest_rate == 0:
        return 0

    monthly_interest_rate = (interest_rate / 12) / 100
    months = duration * 12
    monthly_payment = (
        principal
        * monthly_interest_rate
        * (1 + monthly_interest_rate) ** months
    ) / ((1 + monthly_interest_rate) ** months - 1)
    return round(monthly_payment, 0)


# @st.cache_data(experimental_allow_widgets=True)
def page_input(currency):
    ste.number_input(
        "Purchase Price", key="purchase_price", min_value=0.00, format="%f"
    )

    ste.number_input(
        "Down Payment", key="down_payment", min_value=0.00, format="%f"
    )

    ste.number_input(
        "Loan Origination Fees",
        key="loan_origination_fees",
        min_value=0.00,
        format="%f",
    )

    ste.number_input(
        "Other Closing Costs",
        key="other_costs",
        min_value=0.00,
        format="%f",
    )

    st.session_state["initial_cash_invested"] = (
        st.session_state.SYNC_down_payment
        + st.session_state.SYNC_loan_origination_fees
        + st.session_state.SYNC_other_costs
    )

    # st.write("Initial Cash Invested ", initial_cash_invested)
    st.metric(
        label="""Initial Cash Invested =
            Down Payment + Loan Origination Fees + Other Closing Costs""",
        value=f"{currency}" + str(st.session_state["initial_cash_invested"]),
    )

    ste.number_input(
        "Loan Amount", key="loan_amount", min_value=0.00, format="%f"
    )

    ste.number_input(
        "Loan Term/Duration in Years",
        key="loan_term",
        min_value=0.00,
        format="%f",
    )

    ste.number_input(
        "Interest Rate - Fixed (Eg Interest Rate is 5% then enter 5)",
        key="interest_rate",
        min_value=0.00,
        step=1e-2,
        format="%f",
    )

    st.session_state["monthly_payment"] = calculate_monthly_payment(
        st.session_state.SYNC_loan_amount,
        st.session_state.SYNC_interest_rate,
        st.session_state.SYNC_loan_term,
    )

    st.metric(
        "Monthly Payment",
        f"{currency}" + str(st.session_state["monthly_payment"]),
    )

    ste.number_input(
        "Annual Rent Recieved",
        key="annual_rent",
        min_value=0.00,
        format="%f",
    )

    ste.number_input(
        "Vacancy Loss", key="vacancy_loss", min_value=0.00, format="%f"
    )

    st.session_state["operating_revenue"] = (
        st.session_state.SYNC_annual_rent - st.session_state.SYNC_vacancy_loss
    )

    st.metric(
        "Operating Revenue = Rent Recieved - Vacancy Loss",
        f"{currency}" + str(st.session_state["operating_revenue"]),
    )

    ste.number_input(
        "Annual Maintenance Charge",
        key="maintenance",
        min_value=0.00,
        format="%f",
    )

    ste.number_input(
        "Annual Insurance Cost",
        key="insurance",
        min_value=0.00,
        format="%f",
    )

    ste.number_input(
        "Annual Property Tax",
        key="property_tax",
        min_value=0.00,
        format="%f",
    )

    ste.number_input(
        "Property Managment Fees",
        key="managment_fees",
        min_value=0.00,
        format="%f",
    )

    ste.number_input(
        "Other Expenses", key="other_expenses", min_value=0.00, format="%f"
    )

    st.session_state["operating_expense"] = (
        st.session_state.SYNC_maintenance
        + st.session_state.SYNC_insurance
        + st.session_state.SYNC_property_tax
        + st.session_state.SYNC_managment_fees
        + st.session_state.SYNC_other_expenses
    )

    st.metric(
        """Operating Expense = Maintenance Charge + Insurance Cost
            + Property Tax + Property Management Fees + Other Expenses""",
        f"{currency}" + str(st.session_state["operating_expense"]),
    )

    return


menu = ["EUR", "GBP", "INR", "JPY", "USD"]
choice = st.selectbox("Currency", menu, index=4)

if choice == "EUR":
    st.session_state["currency"] = "€"

if choice == "GBP":
    st.session_state["currency"] = "£"

if choice == "INR":
    st.session_state["currency"] = "₹"

if choice == "JPY":
    st.session_state["currency"] = "¥"

if choice == "USD":
    st.session_state["currency"] = "$"

add_logo("logo@0.1x.png")
page_input(st.session_state["currency"])

