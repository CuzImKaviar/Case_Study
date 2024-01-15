import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_calendar import calendar
import roman
import datetime
from users import User

# -------------- SETTINGS --------------
page_title = "Benutzerverwaltung"
page_icon = ":woman_and_man_holding_hands:"  # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
layout = "centered"

# --------------------------------------

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


# --- NAVIGATION MENU ---
selected = option_menu(
    menu_title=None,
    options=["Benutzer verwalten", "Benutzer anzeigen"],
    icons=["pencil-fill", "bar-chart-fill"],  # https://icons.getbootstrap.com/
    orientation="horizontal",
)
#Benutzer

# --- MANAGE DEVICES ---
if selected == "Benutzer verwalten":

    manage_selected = option_menu(
        menu_title=None,
        options=["Benutzer hinzufügen", "Benutzer bearbeiten", "Benutzer entfernen"],
        icons=["plus-square", "wrench", "dash-square"],  # https://icons.getbootstrap.com/
        orientation="horizontal",
    )

    # --- ADD Benutzer ---
    if manage_selected == "Benutzer hinzufügen":
        st.header(f"Anlegen eines neuen Benutzers")
        with st.form("entry_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            User.location = col1.selectbox("MCI:", list(map(roman.toRoman,range(1,7))), key="mci")
            tool_types = ["Student", "Mitarbeiter", "Professor", "Diverses"]
            User.job = col2.selectbox(" Tätigkeit am MCI oder so:", tool_types, key="type")
            User.name =st.text_input("Name", max_chars=64, placeholder="Name hier einfügen ...", key="Name")
            User.id = st.text_input("E-mail", max_chars=64, placeholder="E-mail hier einfügen ...", key="E-mail")

            submitted = st.form_submit_button("Neuen Benutzer anlegen")
            if submitted:
                st.success("Neuen Benutzer erfolgreich anlegen!")

    # --- MANAGE DEVICE ---               
    if manage_selected == "Benutzer bearbeiten":
        manage = False
        st.header(f"Geräte bearbeiten")
        with st.form("select_form", clear_on_submit=True):
            current_device_example = st.selectbox(
                'Benutzer auswählen',
                options = [User.name], key="user")
            submitted = st.form_submit_button("Gerät bearbeiten")
            if submitted:
                user_name = st.session_state["user"]
                manage = True
        
        if manage:
            with st.form("edit_form", clear_on_submit=True):
                st.header("Benutzer bearbeiten")
                col1, col2 = st.columns(2)
                User.location = col1.selectbox("MCI:", list(map(roman.toRoman,range(1,7))), key="mci")
                tool_types = ["Student", "Mitarbeiter", "Professor", "Diverses"]
                User.job = col2.selectbox(" Tätigkeit am MCI oder so:", tool_types, key="type")
                User.name =st.text_input("Name", max_chars=64, placeholder="Name hier einfügen ...", key="Name")
                User.id = st.text_input("E-mail", max_chars=64, placeholder="E-mail hier einfügen ...", key="E-mail")

                "---"

                save = st.form_submit_button("Änderungen speichern")
                if save:
                    st.success("Änderungen erfolgreich gespeichert!")
            
    # --- REMOVE DEVICES ---
    if manage_selected == "Benutzer entfernen":
        st.header(f"Geräte entfernen")
        with st.form("delete_form", clear_on_submit=True):
            device = st.selectbox(
                'Gerät auswählen',
                options = ["Gerät_A", "Gerät_B"], key="device")
            submitted = st.form_submit_button("Gerät löschen")
            if submitted:
                st.success("Gerät erfolgreich gelöscht!")


# --- SHOW USERS ---
if selected == "Benutzer anzeigen":
    pass