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
col1, col2 = st.columns(2)
benutzerverwaltung = col1.button("Benutzerverwaltung:woman_and_man_holding_hands:", use_container_width=True)
geraeteverwaltung = col2.button("Geräteverwaltung:books:", use_container_width=True)
if benutzerverwaltung:
    nav_page("Benutzerverwaltung")
if geraeteverwaltung:
    nav_page("Geraeteverwaltung")    