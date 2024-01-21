import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_calendar import calendar
import roman
import pandas as pd
import datetime
import time
from users import User

# -------------- SETTINGS --------------
page_title = "Benutzerverwaltung"
page_icon = ":woman_and_man_holding_hands:"  # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
layout = "centered"

# --------------------------------------

st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.title(page_title + " " + page_icon)

# --- SESSION STATES ---
if "manage" not in st.session_state:
    st.session_state["manage"] = False
if "success" not in st.session_state:
    st.session_state["success"] = ""

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

    # --- ADD USERS ---
    if manage_selected == "Benutzer hinzufügen":

        if st.session_state["success"] != "" and st.session_state["success"] != "Benutzer erfolgreich angelegt!":
            st.session_state["success"] = ""

        with st.form("entry_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            location = col1.selectbox("MCI:", list(map(roman.toRoman,range(1,7))), key="mci")
            tool_types = ["Student", "Mitarbeiter", "Professor", "Diverses"]
            job = col2.selectbox("Tätigkeit am MCI:", tool_types, key="type")
            name = st.text_input("Name", max_chars=64, placeholder="Name hier einfügen ...", key="Name")
            id = st.text_input("E-mail", max_chars=64, placeholder="E-mail hier einfügen ...", key="E-mail")

            submitted = st.form_submit_button("Neuen Benutzer anlegen")
            if submitted:
                User(id, name, location, job)
                st.session_state["success"] = "Benutzer erfolgreich angelegt!"
                st.balloons()

    # --- EDIT USERS ---               
    if manage_selected == "Benutzer bearbeiten":

        if st.session_state["success"] != "" and st.session_state["success"] != "Änderungen erfolgreich gespeichert!":
            st.session_state["success"] = ""

        user_options = [user.name for user in User._list]
        

        with st.form("select_form", clear_on_submit=True):
            user = st.selectbox(
                'Benutzer auswählen',
                options = user_options, key="user"
            )
            submitted = st.form_submit_button("Benutzer bearbeiten")
            if submitted:
                st.session_state["manage"] = True
        
            
        
        if st.session_state["manage"]:    
            user_to_edit = next((current_user for current_user in User._list if current_user.name == user), None)
            if user_to_edit is not None:
                with st.form("edit_form", clear_on_submit=False):
                    col1, col2 = st.columns(2)
                    location = col1.selectbox("MCI:", list(map(roman.toRoman,range(1,7))), key="mci", index=roman.fromRoman(user_to_edit.location)-1)
                    tool_types = ["Student", "Mitarbeiter", "Professor", "Diverses"]
                    job = col2.selectbox("Tätigkeit am MCI:", tool_types, key="type", index=tool_types.index(user_to_edit.job))
                    name = st.text_input("Name", value=user_to_edit.name, max_chars=64, placeholder="Name hier einfügen ...", key="Name")
                    id = st.text_input("E-mail", value=user_to_edit.id, max_chars=64, placeholder="E-mail hier einfügen ...", key="E-mail")
                    "---"
                    save = st.form_submit_button("Änderungen speichern")
                    if save:
                        st.write(User.update(user_to_edit.name, id, name, location, job))
                        st.session_state["manage"] = False
                        st.session_state["success"] = "Änderungen erfolgreich gespeichert!"
                        st.rerun()
                        
                        

            else:
                st.error("Benutzer nicht gefunden!")
        st.write(st.session_state["manage"])
    # --- REMOVE USERS ---                      
    if manage_selected == "Benutzer entfernen":

        if st.session_state["success"] != "" and st.session_state["success"] != "Benutzer erfolgreich gelöscht!":
            st.session_state["success"] = ""

        user_options = [user.name for user in User._list]
        with st.form("delete_form", clear_on_submit=True):
            user = st.selectbox(
                'Benutzer auswählen',
                options = user_options, key="user"
            )
            submitted = st.form_submit_button("Benutzer löschen")
            if submitted:
                if User.remove(user):
                    st.session_state["success"] = "Benutzer erfolgreich gelöscht!"                  
                    st.rerun()
                else:
                    st.error("Benutzer konnte nicht gelöscht werden!")
    if st.session_state["success"] != "":        
        st.success(st.session_state["success"])       

# --- SHOW USERS ---
if selected == "Benutzer anzeigen":
    if len(User._list) != 0:
        user_data = [{"Name": user.name, "E-Mail": user.id} for user in User._list]
        df = pd.DataFrame(user_data)
        df.index = df.index + 1
        st.table(df)
    else:
        st.error("Keine Benutzer vorhanden!")