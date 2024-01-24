import streamlit as st
from page_navigation import nav_page

# --- Home Page ---
page_title = "Benutzer- & Geräteverwaltung"
page_icon = ":house:"  # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
layout = "centered"
st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.title(page_title + " " + page_icon)

# --- HIDE STREAMLIT STYLE ---
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# --- NAVIGATE PAGE ---
if st.button("Benutzerverwaltung"):
    nav_page("Benutzerverwaltung")
if st.button("Geräteverwaltung"):
    nav_page("Geraeteverwaltung")    