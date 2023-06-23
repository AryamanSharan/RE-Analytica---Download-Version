import streamlit as st
from streamlit_player import st_player

for k, v in st.session_state.items():
    st.session_state[k] = v
    # st.write(k)

hide_st_style = """
            <style>
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.image("logo@0.1x.png")

st_player("https://youtu.be/Y9i7LN2zxaA")