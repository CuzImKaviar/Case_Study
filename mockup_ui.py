import streamlit as st

from devices import Device
from users import User

Devices = ["Oszilloskop", "CNC-Fräse", "CNC-Drehbank", "Multimeter", "Laser-Cutter", "Schweißgerät", "3D-Drucker", "Bandsäge", "Lötkolben", "Stichsäge", "Kreissäge"]

def user_management():
    st.title("User Management")

    user_name = st.text_input("Username:")
    user_email = st.text_input("Email:")

    if st.button("Create user"):
        new_user = User(id=user_email, name=user_name)
        st.success(f"User '{new_user.name}' with email '{new_user.id}' was created.")

def device_management():
    st.title("Device Management")

    device_name = st.selectbox("Device:", Devices)
    device_reservation_start = st.date_input("Start of reservation:")
    device_reservation_end = st.date_input("End of reservation:")

    if st.button("Create/Change device"):
        if device_reservation_start > device_reservation_end:
            st.error("The start date must not be after the end date.")
        else:
            new_device = Device(name=device_name, reservation_start=device_reservation_start, reservation_end=device_reservation_end)
            st.success(f"Device '{new_device.name}' was created/changed with reservation from '{new_device.reservation_start}' to '{new_device.reservation_end}'.")

selection = st.sidebar.selectbox("Choose an option:", ["User Management", "Device Management"])

if selection == "User Management":
    user_management()
elif selection == "Device Management":
    device_management()