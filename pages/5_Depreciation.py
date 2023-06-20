import streamlit as st
import streamlit_ext as ste
from streamlit_extras.app_logo import add_logo

for k, v in st.session_state.items():
    st.session_state[k] = v

key_list = [
    "currency",
]

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

for key in key_list:
    if key not in st.session_state:
        st.session_state[key] = "₹"

st.title("Depreciation")

add_logo("logo@0.1x.png")

if st.session_state["currency"] == "$":
    tab1, tab2 = st.tabs(["Residential", "Commercial"])

    with tab1:
        ste.number_input(
            "Property Basis = Property Value - Land Value",
            key="property_basis_r",
            min_value=0.00,
            format="%f",
        )
        st.metric(
            "Depreciation per annum",
            "$" + str(round(st.session_state.SYNC_property_basis_r / 27.5, 2)),
        )

    with tab2:
        ste.number_input(
            "Property Basis = Property Value - Land Value",
            key="property_basis_c",
            min_value=0.00,
            format="%f",
        )
        st.metric(
            "Depreciation per annum",
            "$" + str(round(st.session_state.SYNC_property_basis_c / 39, 2)),
        )

elif st.session_state["currency"] == "₹":
    tab1, tab2 = st.tabs(["Residential", "Commercial"])

    with tab1:
        ste.number_input(
            "Property Basis = Property Value - Land Value",
            key="property_basis_r",
            min_value=0.00,
            format="%f",
        )
        st.metric(
            "Depreciation per annum",
            "₹" + str(round(st.session_state.SYNC_property_basis_r * 0.05, 2)),
        )

    with tab2:
        ste.number_input(
            "Property Basis = Property Value - Land Value",
            key="property_basis_c",
            min_value=0.00,
            format="%f",
        )
        st.metric(
            "Depreciation per annum",
            "₹" + str(round(st.session_state.SYNC_property_basis_c * 0.10, 2)),
        )

else:
    st.header("Not Supported for your country")