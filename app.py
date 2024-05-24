import streamlit as st
import paramiko

# Title of the Streamlit app
st.title("Device Controller")

# Input fields for IP address, username, and password
ip_address = st.text_input("IP Address", value="10.101.247.225")
username = st.text_input("Username")
password = st.text_input("Password", type="password")

# Button to connect to the device
if st.button("Connect"):
    try:
        # Create SSH client
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip_address, username=username, password=password)

        # Execute a command (example: 'uname -a')
        stdin, stdout, stderr = ssh.exec_command('uname -a')
        output = stdout.read().decode()
        ssh.close()
        
        st.success("Successfully connected to the device")
        st.write(output)
    except Exception as e:
        st.error(f"Error: {e}")

# Additional functionality can be added here (e.g., executing more commands)
