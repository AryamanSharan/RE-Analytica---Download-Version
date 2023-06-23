import streamlit as st

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

st.header("Send an Email at - reanalytica@gmail.com")