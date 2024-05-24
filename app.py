import streamlit as st
import requests  # Assuming the device is a web service

# Title of the Streamlit app
st.title("Device Controller")

# Input fields for IP address, username, and password
ip_address = st.text_input("IP Address", value="10.101.247.225")
username = st.text_input("Username")
password = st.text_input("Password", type="password")

# Button to connect to the device
if st.button("Connect"):
    # Example connection logic
    try:
        # Example of sending a request to the device (replace with actual logic)
        response = requests.get(f"http://{ip_address}", auth=(username, password))
        if response.status_code == 200:
            st.success("Successfully connected to the device")
            # Display some information about the device
            st.write(response.json())  # Assuming the device returns JSON data
        else:
            st.error(f"Failed to connect: {response.status_code}")
    except Exception as e:
        st.error(f"Error: {e}")

# Additional functionality can be added here (e.g., sending commands to the device, fetching data, etc.)
