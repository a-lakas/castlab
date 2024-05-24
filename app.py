import streamlit as st
import subprocess

def check_connectivity(ip, port):
    try:
        # Run the netcat command to check connectivity
        result = subprocess.run(['nc', '-zv', ip, str(port)], capture_output=True, text=True, timeout=10)
        return result.stdout if result.returncode == 0 else result.stderr
    except Exception as e:
        return str(e)

# Streamlit app title
st.title("Device Connectivity Checker")

# Input fields for IP address and port
ip_address = st.text_input("IP Address", value="10.101.247.225")
port = st.number_input("Port", value=80, min_value=1, max_value=65535)

# Button to check connectivity
if st.button("Check Connectivity"):
    output = check_connectivity(ip_address, port)
    st.text(output)

# Input fields for username and password
username = st.text_input("Username")
password = st.text_input("Password", type="password")

# Button to connect to the device (for example, via HTTP)
if st.button("Connect"):
    try:
        response = requests.get(f"http://{ip_address}", auth=(username, password), timeout=10)
        if response.status_code == 200:
            st.success("Successfully connected to the device")
            st.write(response.json())  # Assuming the device returns JSON data
        else:
            st.error(f"Failed to connect: {response.status_code}")
    except requests.ConnectionError as ce:
        st.error(f"Connection error: {ce}")
    except requests.Timeout as te:
        st.error(f"Connection timed out: {te}")
    except Exception as e:
        st.error(f"An error occurred: {e}")
