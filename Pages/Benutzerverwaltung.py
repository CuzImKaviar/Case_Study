import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_calendar import calendar
import roman
import pandas as pd
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
    icons=["pencil-fill", "bi bi-eye"],  # https://icons.getbootstrap.com/
    orientation="horizontal",
)

# --- MANAGE USERS ---
if selected == "Benutzer verwalten":

    manage_selected = option_menu(
        menu_title=None,
        options=["Benutzer hinzufügen", "Benutzer bearbeiten", "Benutzer entfernen"],
        icons=["plus-square", "wrench", "dash-square"],  # https://icons.getbootstrap.com/
        orientation="horizontal",
    )

    # --- ADD USER ---
    if manage_selected == "Benutzer hinzufügen":
        st.header(f"Anlegen eines neuen Benutzers")
        with st.form("entry_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            location = col1.selectbox("MCI:", list(map(roman.toRoman,range(1,7))), key="mci")
            tool_types = ["Student", "Mitarbeiter", "Professor", "Diverses"]
            job = col2.selectbox(" Tätigkeit am MCI oder so:", tool_types, key="type")
            name = st.text_input("Name", max_chars=64, placeholder="Name hier einfügen ...", key="Name")
            id = st.text_input("E-mail", max_chars=64, placeholder="E-mail hier einfügen ...", key="E-mail")

            submitted = st.form_submit_button("Neuen Benutzer anlegen")
            if submitted:
                User(id, name, location, job)
                st.success("Neuen Benutzer erfolgreich anlegen!")

    # --- EDIT USER ---               
    if manage_selected == "Benutzer bearbeiten":
        manage = False
        st.header(f"Benutzer bearbeiten")

        
        with st.form("select_form", clear_on_submit=False):
            current_user = st.selectbox(
                'Benutzer auswählen',
                options = User._list, format_func=lambda user: user.name, key="user"
            )
            submitted = st.form_submit_button("Benutzer bearbeiten")
            if submitted:
                user_to_edit = next((user for user in User._list if user.name == current_user), None)
                manage = True
        
        if manage:
            with st.form("edit_form", clear_on_submit=True):
                col1, col2 = st.columns(2)
                user_to_edit.location = col1.selectbox("MCI:", list(map(roman.toRoman,range(1,7))), key="mci")
                tool_types = ["Student", "Mitarbeiter", "Professor", "Diverses"]
                user_to_edit.job = col2.selectbox(" Tätigkeit am MCI oder so:", tool_types, key="type")
                user_to_edit.name =st.text_input("Name", max_chars=64, placeholder="Name hier einfügen ...", key="Name")
                user_to_edit.id = st.text_input("E-mail", max_chars=64, placeholder="E-mail hier einfügen ...", key="E-mail")

                "---"

                save = st.form_submit_button("Änderungen speichern")
                if save:
                    st.success("Änderungen erfolgreich gespeichert!")

    # --- REMOVE USERS ---                
    if manage_selected == "Benutzer entfernen":
        user_options = [user.name for user in User._list]

        with st.form("delete_form", clear_on_submit=True):
            user = st.selectbox(
                'Benutzer auswählen',
                options = user_options, key="user"
            )
            submitted = st.form_submit_button("Benutzer löschen")
            if submitted:
                if User.remove(user):
                    st.success("Benutzer erfolgreich gelöscht!")
                else:
                    st.error("Benutzer konnte nicht gelöscht werden!")
        

# --- SHOW USERS ---
if selected == "Benutzer anzeigen":  
    if len(User._list) != 0:
        user_data = [{"Name": user.name, "E-Mail": user.id} for user in User._list]
        df = pd.DataFrame(user_data)
        df.index = df.index + 1
        st.table(df)
    else:
        st.error("Keine Benutzer vorhanden!")