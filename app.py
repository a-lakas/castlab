import streamlit as st
import requests
import uuid
import paramiko
from PIL import Image
from requests.exceptions import ConnectionError, Timeout
import subprocess
import pyrebase

DEFAULT_USERNAME = "swavaf"
DEFAULT_PASSWORD = "swavaf@123"
ip_address = "10.101.247.225"

# Firebase configuration
firebaseConfig = {
    'apiKey': "AIzaSyC_1yhveazgVtX-hfmZh6OwFGvODNgCgG4",
    'authDomain': "loginwithstreamlit.firebaseapp.com",
    'projectId': "loginwithstreamlit",
    'databaseURL': "https://loginwithstreamlit-default-rtdb.firebaseio.com",
    'storageBucket': "loginwithstreamlit.appspot.com",
    'messagingSenderId': "286638028806",
    'appId': "1:286638028806:web:931ff9cffb9421e4b42b87",
    'measurementId': "G-SFTNJ19HS6"
}

# Initialize Firebase
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()


def ping_server(ip_address):
    try:
        result = subprocess.run(['ping', '-c', '4', ip_address], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10)
        if result.returncode == 0:
            return "Server is reachable."
        else:
            return "Server is unreachable."
    except Exception as e:
        return f"Error: {str(e)}"


def fetch_data_from_host(ip_address):
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=ip_address, username=DEFAULT_USERNAME, password=DEFAULT_PASSWORD)
        stdin, stdout, stderr = ssh_client.exec_command('your_command')
        data = stdout.read().decode()
        ssh_client.close()
        return data
    except Exception as e:
        return f"Error: {str(e)}"

def reset_password(email):
    try:
        auth.send_password_reset_email(email)
        return "Password reset email sent successfully"
    except:
        return "Error: Unable to send password reset email"

def main():
    st.set_page_config(page_title="UAEU A100 Portal")

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
        , unsafe_allow_html=True
    )

    st.markdown("<div class='header'>A100 Portal</div>", unsafe_allow_html=True)
    st.sidebar.image('uaeu.png', caption='', width=300)


    with st.sidebar:
        # st.markdown("<div class='form-container'>", unsafe_allow_html=True)
        st.markdown("<h2>Login</h2>", unsafe_allow_html=True)
        login_email = st.sidebar.text_input('Please enter your email address', value="admin@cd3.com", disabled=False)
        login_password = st.sidebar.text_input('Please enter your password',type = 'password', value="admin@123", disabled=False)
        login = st.sidebar.checkbox('Login')

        if login:
            try:
                user = auth.sign_in_with_email_and_password(login_email, login_password)
                st.success("Successfully logged in!")            
            except:
                st.error("Invalid email or password")

        # st.markdown("<a href='#' id='forgot-password-link'>Forgot password?</a>", unsafe_allow_html=True)

        if st.sidebar.button("Forgot password?"):
            st.session_state.show_reset_form = True

        if 'show_reset_form' not in st.session_state:
            st.session_state.show_reset_form = False

        if st.session_state.show_reset_form:
            st.markdown("<h2>Reset Password</h2>", unsafe_allow_html=True)
            reset_email = st.sidebar.text_input('Enter your email to reset password', value="", disabled=False)
            if st.sidebar.button("Send reset email"):
                message = reset_password(reset_email)
                st.sidebar.write(message)
        

        # st.markdown("<a href='/reset_password'>Forgot password?</a>", unsafe_allow_html=True)
        # st.markdown("</div>", unsafe_allow_html=True)

        # st.markdown("<div class='form-container'>", unsafe_allow_html=True)
        st.markdown("<h2>Sign up</h2>", unsafe_allow_html=True)
        affiliation = st.selectbox("Affiliation", ["Student", "Faculty", "Research"])
        signup_name = st.sidebar.text_input('Your Name', value="", disabled=False)
        signup_email = st.sidebar.text_input('Your Email', value="", disabled=False)
        signup_password = st.sidebar.text_input('Your Password', type="password", value="", disabled=False)
        signup_confirm_password = st.sidebar.text_input('Confirm Password',type = 'password', value="", disabled=False)
        signup_button = st.button("Sign up")

        if signup_button:
            if signup_password == signup_confirm_password:
                try:
                    user = auth.create_user_with_email_and_password(signup_email, signup_password)
                    st.success("Successfully signed up!")
                except:
                    st.error("Failed to create account")
            else:
                st.error("Passwords do not match")

        st.markdown("</div>", unsafe_allow_html=True)
        
    if login:
            st.write("IP address - 10.101.247.225")
            st.write("Username - swavaf")
            st.write("Password - swavaf@123")
            if st.button('Connect Host'):
                if ip_address:
                    st.write("Connecting...")
                    data = fetch_data_from_host(ip_address)
                    st.write("Response:")
                    st.write(data)
                else:
                    st.write("Connection failed")

if __name__ == "__main__":
    main()
