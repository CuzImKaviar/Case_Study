import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_calendar import calendar
import roman
import datetime
from users import User
from devices import Device

# -------------- SETTINGS --------------
page_title = "Geräteverwaltung"
page_icon = ":books:"  # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
layout = "centered"

# --- SESSION STATES ---
if "manage" not in st.session_state:
    st.session_state["manage"] = False
if "success" not in st.session_state:
    st.session_state["success"] = ""


calendar_resources = [
    {"id": "a", "building": "Building A", "title": "Room A"},
    {"id": "b", "building": "Building A", "title": "Room B"},
    {"id": "c", "building": "Building B", "title": "Room C"},
    {"id": "d", "building": "Building B", "title": "Room D"},
    {"id": "e", "building": "Building C", "title": "Room E"},
    {"id": "f", "building": "Building C", "title": "Room F"},
]
events = [
    {
        "title": "Event 1",
        "color": "#FF6C6C",
        "start": "2023-07-03",
        "end": "2023-07-05",
        "resourceId": "a",
    },
    {
        "title": "Event 2",
        "color": "#FFBD45",
        "start": "2023-07-01",
        "end": "2023-07-10",
        "resourceId": "b",
    },
    {
        "title": "Event 3",
        "color": "#FF4B4B",
        "start": "2023-07-20",
        "end": "2023-07-20",
        "resourceId": "c",
    },
    {
        "title": "Event 4",
        "color": "#FF6C6C",
        "start": "2023-07-23",
        "end": "2023-07-25",
        "resourceId": "d",
    },
    {
        "title": "Event 5",
        "color": "#FFBD45",
        "start": "2023-07-29",
        "end": "2023-07-30",
        "resourceId": "e",
    },
    {
        "title": "Event 6",
        "color": "#FF4B4B",
        "start": "2023-07-28",
        "end": "2023-07-20",
        "resourceId": "f",
    },
    {
        "title": "Event 7",
        "color": "#FF4B4B",
        "start": "2023-07-01T08:30:00",
        "end": "2023-07-01T10:30:00",
        "resourceId": "a",
    },
    {
        "title": "Event 8",
        "color": "#3D9DF3",
        "start": "2023-07-01T07:30:00",
        "end": "2023-07-01T10:30:00",
        "resourceId": "b",
    },
    {
        "title": "Event 9",
        "color": "#3DD56D",
        "start": "2023-07-02T10:40:00",
        "end": "2023-07-02T12:30:00",
        "resourceId": "c",
    },
    {
        "title": "Event 10",
        "color": "#FF4B4B",
        "start": "2023-07-15T08:30:00",
        "end": "2023-07-15T10:30:00",
        "resourceId": "d",
    },
    {
        "title": "Event 11",
        "color": "#3DD56D",
        "start": "2023-07-15T07:30:00",
        "end": "2023-07-15T10:30:00",
        "resourceId": "e",
    },
    {
        "title": "Event 12",
        "color": "#3D9DF3",
        "start": "2023-07-21T10:40:00",
        "end": "2023-07-21T12:30:00",
        "resourceId": "f",
    },
    {
        "title": "Event 13",
        "color": "#FF4B4B",
        "start": "2023-07-17T08:30:00",
        "end": "2023-07-17T10:30:00",
        "resourceId": "a",
    },
    {
        "title": "Event 14",
        "color": "#3D9DF3",
        "start": "2023-07-17T09:30:00",
        "end": "2023-07-17T11:30:00",
        "resourceId": "b",
    },
    {
        "title": "Event 15",
        "color": "#3DD56D",
        "start": "2023-07-17T10:30:00",
        "end": "2023-07-17T12:30:00",
        "resourceId": "c",
    },
    {
        "title": "Event 16",
        "color": "#FF6C6C",
        "start": "2023-07-17T13:30:00",
        "end": "2023-07-17T14:30:00",
        "resourceId": "d",
    },
    {
        "title": "Event 17",
        "color": "#FFBD45",
        "start": "2023-07-17T15:30:00",
        "end": "2023-07-17T16:30:00",
        "resourceId": "e",
    },
]
calendar_options = {
    "editable": "true",
    "navLinks": "true",
    "resources": calendar_resources,
    "selectable": "true",
}

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
    options=["Geräte verwalten", "Geräte reservieren", "Geräte anzeigen"],
    icons=["pencil-fill", "clock-history", "bar-chart-fill"],  # https://icons.getbootstrap.com/
    orientation="horizontal",
)


# --- MANAGE DEVICES ---
if selected == "Geräte verwalten":

    manage_selected = option_menu(
        menu_title=None,
        options=["Geräte hinzufügen", "Geräte bearbeiten", "Geräte entfernen"],
        icons=["plus-square", "wrench", "dash-square"],  # https://icons.getbootstrap.com/
        orientation="horizontal",
    )

    # --- ADD DEVICES ---
    if manage_selected == "Geräte hinzufügen":
        st.header(f"Anlegen eines neuen Gerätes")

        if st.session_state["success"] != "" and st.session_state["success"] != "Neues Gerät angelegt":
            st.session_state["success"] = ""

        with st.form("entry_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            location = col1.selectbox("MCI:", list(map(roman.toRoman,range(1,7))), key="mci")
            tool_types = ["Office", "EDV", "Labore", "Diverses"]
            tool_type = col2.selectbox("Geräte Art:", tool_types, key="type")
            id = st.text_input("Geräte ID:", max_chars=64, placeholder="Geräte ID hier einfügen ...", key="id")
            device_name = st.text_input("Gerätename:", max_chars=64, placeholder="Gerätename hier einfügen ...", key="name")
            
            
            user_options = User.get_all_ids()

            user_id = st.selectbox('Verwaltenden Benutzer auswählen',options = user_options, key="user")

            managed_by_user_id = user_id
            
            
            
            "---"

            with st.expander("Geräteeigenschaften"):
                price = st.number_input("Preis:", min_value=0, format="%i", step=10, key="cost")
                movable = st.radio("Beweglichkeit:", ["Feststehend", "Beweglich"], horizontal=True, key="mobility")
            with st.expander("Wartung und Reservierung"):
                maintanance_period = st.radio(
                    "Wartungsabstände:",
                    options=["keine Wartung notwendig", "täglich", "wöchentlich", "monatlich", "jährlich"],
                    key="intervals")
                reservable = st.radio("Reservierbarkeit:", ["Reservierbar", "Nicht reservierbar"], horizontal=True, key="reservierbar")
            with st.expander("Kommentar"):
                comment = st.text_area("Kommentarfeld", placeholder="Kommentar hier einfügen ...", label_visibility="collapsed")

            "---"

            submitted = st.form_submit_button("Neues Gerät angelegt")
            if submitted:
                new_Device = Device(id, device_name, managed_by_user_id, location, tool_type, price, movable, maintanance_period, reservable, comment)
                new_Device.store()
                st.session_state["success"] = "Neues Gerät angelegt"
                st.balloons()
            
        if st.session_state["success"] != "" :        
            st.success(st.session_state["success"])

    # --- EDIT DEVICE ---               
    if manage_selected == "Geräte bearbeiten":

        if st.session_state["success"] != "" and st.session_state["success"] != "Gerät bearbeitet":
            st.session_state["success"] = ""

        manage = False
        st.header(f"Geräte bearbeiten")

        device_options = Device.get_all_ids()
        
        with st.form("select_form", clear_on_submit=False):
            device_id = st.selectbox('Gerät auswählen',options = device_options, key="device")
            submitted = st.form_submit_button("Gerät bearbeiten")
            if submitted:
                device_name = st.session_state["device"]
                st.session_state["manage"] = True

        if st.session_state["manage"]:
            device = Device.load_data_by_id(device_id)
            with st.form("edit_form", clear_on_submit=True):
                st.header(str(device.device_name))
                
                new_device_name = st.text_input("Gerätename:",value=device.device_name, max_chars=64, placeholder="Neuen Gerätenamen hier einfügen ...", key="name")
                user_options = User.get_all_ids()
                new_managed_by_id = st.selectbox('Verwaltenden Benutzer auswählen',options = user_options, key="user")

                col1, col2 = st.columns(2)
                location = col1.selectbox("MCI:", list(map(roman.toRoman,range(1,7))), key="mci")
                tool_types = ["Office", "EDV", "Labore", "Diverses"]
                tool_type = col2.selectbox("Geräte Art:", tool_types, key="type", index=tool_types.index(device.tool_type))

                "---"

                with st.expander("Geräteeigenschaften"):
                    price = st.number_input("Preis:", min_value=0, value=device.price, format="%i", step=10, key="cost")
                    movable = st.radio("Beweglichkeit:", ["Feststehend", "Beweglich"], horizontal=True, key="mobility")
                with st.expander("Wartung und Reservierung"):
                    maintenance_period = st.radio(
                        "Wartungsabstände:",
                        options=["keine Wartung notwendig", "täglich", "wöchentlich", "monatlich", "jährlich"],
                        key="intervals")
                    reservable = st.radio("Resavierbarkeit:", ["Resavierbar", "Nicht resavierbar"], horizontal=True, key="resavable")
                with st.expander("Kommentar"):
                    comment = st.text_area("Kommentarfeld", value=device.comment, placeholder="Kommentar hier einfügen ...", label_visibility="collapsed")

                "---"

                save = st.form_submit_button("Änderungen speichern")
                if save:
                    new_Device = Device(device_id, new_device_name, new_managed_by_id, location, tool_type, price, movable, maintenance_period, reservable, comment)
                    new_Device.store()
                    st.session_state["success"] = "Gerät bearbeitet"                   
                    st.rerun()

        if st.session_state["success"] != "" :        
            st.success(st.session_state["success"])
            
    # --- REMOVE DEVICES ---
    if manage_selected == "Geräte entfernen":

        if st.session_state["success"] != "" and st.session_state["success"] != "Gerät erfolgreich gelöscht!":
            st.session_state["success"] = ""

        st.header(f"Geräte entfernen")
        with st.form("delete_form", clear_on_submit=True):

            device_options = Device.get_all_names()

            device_to_be_deleted_name = st.selectbox('Gerät auswählen',options = device_options, key="device")
            device_to_be_deleted = Device.load_data_by_id(device_to_be_deleted_name)
            submitted = st.form_submit_button("Gerät löschen")
            if submitted:
                device_to_be_deleted.delete()
                st.session_state["success"] = "Gerät erfolgreich gelöscht!"
                st.rerun()
                

        if st.session_state["success"] != "" :        
            st.success(st.session_state["success"])

# --- RESERVE DEVICES ---
if selected == "Geräte reservieren":
    st.header(f"Reservieren eines  Geräts")
    with st.form("entry_form", clear_on_submit=True):

        device_options = Device.get_all_ids()
        user_options = User.get_all_names()

        col1, col2 = st.columns(2)
        Reserved_device = col1.selectbox('Gerät auswählen',options = device_options, key="device")
        Reserved_by = col2.selectbox('User auswählen',options = user_options, key="user")
        title = st.text_input("Titel", max_chars=64, placeholder="Grund der Reservierung hier einfügen ...", key="Titel")
    

        "---"

        start_date = st.date_input("Startdatum auswählen:", datetime.datetime.now(), format="DD.MM.YYYY")
        end_date = st.date_input("Enddatum auswählen:", datetime.datetime.now(), format="DD.MM.YYYY")
        

        device = Device.load_data_by_id(Reserved_device)
        st.write(device)
        submitted = st.form_submit_button("Gerät reservieren")
        if submitted:
            
            device.add_reservations(start_date, end_date, Reserved_by, title)

            st.success("Gerät erfolgreich reserviert!")
    
    if st.session_state["success"] != "" :        
        st.success(st.session_state["success"])


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

# --- NAVIGATE PAGE ---
col1, col2 = st.columns(2)
if col1.button("Home:house:", use_container_width=True):
    st.switch_page("🏠_Home.py")
if col2.button("Benutzerverwaltung:woman_and_man_holding_hands:", use_container_width=True):
    st.switch_page("pages/2_👫_Benutzerverwaltung.py")