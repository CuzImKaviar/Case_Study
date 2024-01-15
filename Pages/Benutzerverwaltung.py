import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_calendar import calendar
import roman
import datetime

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
    options=["Benutzer verwalten", "Geräte resvieren", "Benutzer anzeigen"],
    icons=["pencil-fill", "clock-history", "bar-chart-fill"],  # https://icons.getbootstrap.com/
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
            col1.selectbox("MCI:", list(map(roman.toRoman,range(1,7))), key="mci")
            tool_types = ["Student", "Mitarbeiter", "Professor", "Diverses"]
            col2.selectbox(" Tätigkeit am MCI oder so:", tool_types, key="type")
            st.text_input("E-mail", max_chars=64, placeholder="E-mail hier einfügen ...", key="E-mail")



            submitted = st.form_submit_button("Neuen Benutzer anlegen")
            if submitted:
                st.success("Neuen Benutzer erfolgreich anlegen!")

    # --- MANAGE Benutzer ---               
    if manage_selected == "Benutzer bearbeiten":
        manage = False
        st.header(f"Benutzer bearbeiten")
        with st.form("select_form", clear_on_submit=True):
            current_device_example = st.selectbox(
                'Benutzer auswählen',
                options = ["Gerät_A", "Gerät_B"], key="Benutzer")
            submitted = st.form_submit_button("Benutzer bearbeiten")
            if submitted:
                device_name = st.session_state["Benutzer"]
                manage = True
        
        if manage:
            with st.form("edit_form", clear_on_submit=True):
                st.header(str(device_name))
                
                #Hier müssten die Werte bereits eingefüllt sein
                col1, col2 = st.columns(2)
                col1.selectbox("MCI:", list(map(roman.toRoman,range(1,7))), key="mci")
                tool_types = ["Student", "Mitarbeiter", "Professor", "Diverses"]
                col2.selectbox(" Tätigkeit am MCI oder so:", tool_types, key="type")
                st.text_input("E-mail", max_chars=64, placeholder="E-mail hier einfügen ...", key="E-mail")


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


# --- SHOW DEVICES ---
if selected == "Geräte anzeigen":

    show_selected = option_menu(
        menu_title=None,
        options=["Geräte Anzeigen", "Wartungen Anzeigen"],
        icons=["search", "tools"],  # https://icons.getbootstrap.com/
        orientation="horizontal",
    )

    # --- SHOW DEVICE ---
    if show_selected == "Geräte Anzeigen":
        st.header(f"Geräteanzeige")
        calendar_options = {
            **calendar_options,
            "headerToolbar": {
                "left": "today prev,next",
                "center": "title",
                "right": "resourceTimelineDay,resourceTimelineWeek,resourceTimelineMonth",
            },
            "initialDate": "2023-07-01",
            "initialView": "resourceTimelineMonth",
            "resourceGroupField": "building",
        }

    # --- SHOW MAINTENANCE ---
    if show_selected == "Wartungen Anzeigen":
        st.header(f"Gerätewartungen")
        calendar_options = {
            **calendar_options,
            "headerToolbar": {
                "left": "today prev,next",
                "center": "title",
                "right": "dayGridDay,dayGridWeek,dayGridMonth",
            },
            "initialDate": "2023-07-01",
            "initialView": "dayGridMonth",
        }

    calendar(
        events=events,
        options=calendar_options,
        custom_css="""
        .fc-event-past {
            opacity: 0.8;
        }
        .fc-event-time {
            font-style: italic;
        }
        .fc-event-title {
            font-weight: 700;
        }
        .fc-toolbar-title {
            font-size: 2rem;
        }
        """,
        key=show_selected,
    )