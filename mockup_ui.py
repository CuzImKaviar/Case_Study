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

    user_name = st.text_input("Username:")
    device_name = st.selectbox("Device:", Devices)


def reservation_system():
    st.title("Reservation System")

    device_name = st.selectbox("Device:", Devices)
    col1, col2 = st.columns(2)
    device_reservation_start = col1.date_input("Start of reservation:")
    device_reservation_end = col2.date_input("End of reservation:")
    user_email = st.text_input("User email:")

    if st.button("Create/Change Reservation"):
        if device_reservation_start > device_reservation_end:
            st.error("The start date must not be after the end date.")
        else:
            new_device = Device(device_name=device_name, managed_by_user_id=user_email,reservation_start=device_reservation_start, reservation_end=device_reservation_end)
            st.success(f"Device '{new_device.device_name}' was reservated from '{new_device.reservation_start}' to '{new_device.reservation_end}' by '{user_email}'.")


def maintenance_management():
    st.title("Maintenance Management")

    device_name = st.selectbox("Device:", Devices)
    col1, col2 = st.columns(2)
    device_reservation_start = col1.date_input("Start of maintenance interval:")
    device_reservation_end = col2.date_input("End of maintenance interval:")
    user_email = st.text_input("User email:")

    if st.button("Create/Change maintenance interval"):
        if device_reservation_start > device_reservation_end:
            st.error("The start date must not be after the end date.")
        else:
            new_device = Device(device_name=device_name, managed_by_user_id=user_email,reservation_start=device_reservation_start, reservation_end=device_reservation_end)
            st.success(f"Device '{new_device.device_name}' was reservated from '{new_device.reservation_start}' to '{new_device.reservation_end}' by '{user_email}'.")
    # Implementiere hier die Wartungsmanagementfunktionalität...

selection = st.sidebar.selectbox("Choose an option:", ["User Management", "Device Management", "Reservation System","Maintenance Management"])

if selection == "User Management":
    user_management()
elif selection == "Device Management":
    device_management()
elif selection == "Reservation System":
    reservation_system()
elif selection == "Maintenance Management":
    maintenance_management()