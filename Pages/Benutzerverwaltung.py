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
    if manage_selected == "Geräte bearbeiten":
        manage = False
        st.header(f"Geräte bearbeiten")
        with st.form("select_form", clear_on_submit=True):
            current_device_example = st.selectbox(
                'Gerät auswählen',
                options = ["Gerät_A", "Gerät_B"], key="device")
            submitted = st.form_submit_button("Gerät bearbeiten")
            if submitted:
                device_name = st.session_state["device"]
                manage = True
        
        if manage:
            with st.form("edit_form", clear_on_submit=True):
                st.header(str(device_name))
                col1, col2 = st.columns(2)
                col1.selectbox("MCI:", list(map(roman.toRoman,range(1,7))), key="mci")
                tool_types = ["Office", "EDV", "Labore", "Diverses"]
                col2.selectbox("Geräte Art:", tool_types, key="type")

                "---"

                with st.expander("Geräteeigenschaften"):
                    st.number_input("Preis:", min_value=0, format="%i", step=10, key="cost")
                    st.selectbox("Verantwortlicher:", ["Person A", "Person B"], key="person")
                    st.radio("Beweglichkeit:", ["Feststehend", "Beweglich"], horizontal=True, key="mobility")
                with st.expander("Wartung und Reservierung"):
                    st.radio(
                        "Wartungsabstände:",
                        options=["keine Wartung notwendig", "täglich", "wöchentlich", "monatlich", "jährlich"],
                        key="intervals")
                    st.number_input("Kosten pro Wartung:", min_value=0, format="%i", step=1, key="maintenancecost")
                    st.radio("Resavierbarkeit:", ["Resavierbar", "Nicht resavierbar"], horizontal=True, key="resavable")
                with st.expander("Kommentar"):
                    comment = st.text_area("Kommentarfeld", placeholder="Kommentar hier einfügen ...", label_visibility="collapsed")

                "---"

                save = st.form_submit_button("Änderungen speichern")
                if save:
                    st.success("Änderungen erfolgreich gespeichert!")
            
    # --- REMOVE DEVICES ---
    if manage_selected == "Geräte entfernen":
        st.header(f"Geräte entfernen")
        with st.form("delete_form", clear_on_submit=True):
            device = st.selectbox(
                'Gerät auswählen',
                options = ["Gerät_A", "Gerät_B"], key="device")
            submitted = st.form_submit_button("Gerät löschen")
            if submitted:
                st.success("Gerät erfolgreich gelöscht!")


# --- RESERVE DEVICES ---
if selected == "Geräte resvieren":
    st.header(f"Anlegen eines neuem Gerät")
    with st.form("entry_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        col1.selectbox(
                'Gerät auswählen',
                options = ["Gerät_A", "Gerät_B"], key="device")
        reason_types = ["Wartung", "Lehrveranstaltung", "Forschungsprojekt", "Privatgebruach"]
        col2.selectbox("Resvierungsgrund:", reason_types, key="reason")

        "---"

        st.date_input(
            "Resvierungszeitraum auswählen:",
            (datetime.datetime.now(), datetime.datetime.now()),
            datetime.datetime.now(),
            format="DD-MM-YYYY",
        )

        "---"

        with st.expander("Kommentar"):
            comment = st.text_area("Kommentarfeld", placeholder="Kommentar hier einfügen ...", label_visibility="collapsed")

        "---"

        submitted = st.form_submit_button("Gerät resvieren")
        if submitted:
            st.success("Gerät erfolgreich resviert!")


# --- SHOW USERS ---
if selected == "Benutzer anzeigen":
    pass