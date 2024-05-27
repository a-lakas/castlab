import streamlit as st
import requests
import uuid
import paramiko
from PIL import Image



DEFAULT_USERNAME = "swavaf"
DEFAULT_PASSWORD = "swavaf@123"
# Hardcoded IP address
ip_address = "10.101.247.225"

def fetch_data_from_host(ip_address):
    try:
        # Define default authentication credentials
        auth = (DEFAULT_USERNAME, DEFAULT_PASSWORD)
        
        # Make the request with authentication
        response = requests.get(f'http://{ip_address}/endpoint', auth=auth)
        
        if response.status_code == 200:
            return response.text
        else:
            return f"Error: {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

# def fetch_data_from_host(ip_address):
#     try:
#         # Create an SSH client instance
#         ssh_client = paramiko.SSHClient()
        
#         # Automatically add the host keys
#         ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
#         # Connect to the SSH server
#         ssh_client.connect(hostname=ip_address, username=DEFAULT_USERNAME, password=DEFAULT_PASSWORD)
        
#         # Execute a command to fetch data (replace 'your_command' with the actual command you want to run)
#         stdin, stdout, stderr = ssh_client.exec_command('your_command')
        
#         # Read the output from the command
#         data = stdout.read().decode()
        
#         # Close the SSH connection
#         ssh_client.close()
        
#         return data
        
    except Exception as e:
        return f"Error: {str(e)}"
        

        
def main():
    st.set_page_config(page_title="UAEU A100 Portal")

    # Header
    st.markdown(
        """
        <style>
            .header {
                background-color: #00acc1;
                padding: 20px;
                color: white;
                text-align: center;
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 30px;
            }
            .form-container {
                background-color: #f0f0f0;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            }
            .input-field label {
                color: #00acc1 !important;
            }
            .input-field input[type="text"]:focus + label,
            .input-field input[type="password"]:focus + label {
                color: #00acc1 !important;
            }
            .btn {
                background-color: #00acc1 !important;
                margin-top: 20px;
                margin-bottom: 10px;
            }
        </style>
        """
        ,unsafe_allow_html=True
    )

    st.markdown("<div class='header'>A100 Portal</div>", unsafe_allow_html=True)

    # Button to trigger the request
    if st.button('Connect Host'):
        if ip_address:
            st.write("Connecting...")
            data = fetch_data_from_host(ip_address)
            st.write("Response:")
            st.write(data)
        else:
            st.write("Connection failed")

        

    # Login Form
    with st.sidebar:
        st.markdown("<div class='form-container'>", unsafe_allow_html=True)
        st.markdown("<h2>Login</h2>", unsafe_allow_html=True)
        login_email = st.text_input("Your Email", key=str(uuid.uuid4()))
        login_password = st.text_input("Your Password", type="password", key=str(uuid.uuid4()))
        login_button = st.button("Login", key=str(uuid.uuid4()))
        st.markdown("<a href='/reset_password'>Forgot password?</a>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Sign up Form
        st.markdown("<div class='form-container'>", unsafe_allow_html=True)
        st.markdown("<h2>Sign up</h2>", unsafe_allow_html=True)
        affiliation = st.selectbox("Affiliation", ["Student", "Faculty", "Research"], key=str(uuid.uuid4()))
        signup_name = st.text_input("Your Name", key=str(uuid.uuid4()))
        signup_email = st.text_input("Your Email", key=str(uuid.uuid4()))
        signup_password = st.text_input("Your Password", type="password", key=str(uuid.uuid4()))
        signup_confirm_password = st.text_input("Confirm Password", type="password", key=str(uuid.uuid4()))
        signup_button = st.button("Sign up", key=str(uuid.uuid4()))
        st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
