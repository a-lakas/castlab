import streamlit as st
import requests
import uuid
import paramiko
from PIL import Image
from requests.exceptions import ConnectionError, Timeout
import subprocess
import pyrebase
from datetime import datetime


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
db = firebase.database()


def ping_server(ip_address):
    try:
        result = subprocess.run(['ping', '-c', '4', ip_address], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10)
        if result.returncode == 0:
            return "Server is reachable."
        else:
            return "Server is unreachable."
    except Exception as e:
        return f"Error: {str(e)}"


def fetch_data_from_host(ip_address, port=22):
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=ip_address, port=port, username=DEFAULT_USERNAME, password=DEFAULT_PASSWORD)
        stdin, stdout, stderr = ssh_client.exec_command('pyspark')
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

    # # Text inputs for SSH connection details
    # server_ip = st.text_input('Enter Server IP Address', '10.101.247.225')
    # port = st.number_input('Enter SSH Port', value=22)
    # username = st.text_input('Enter Username', 'swavaf')
    # password = st.text_input('Enter Password', type='password', value='swavaf@123')

    # # Button to initiate connection
    # if st.button('Connect'):
    #     try:
    #         # Create SSH client
    #         ssh_client = paramiko.SSHClient()
    #         ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    #         # Connect to server
    #         ssh_client.connect(server_ip, port=port, username=username, password=password)

    #         # Display success message
    #         st.success('Connected to server successfully!')
            
    #         # Close the connection
    #         ssh_client.close()
    #     except Exception as e:
    #         # Display error message
    #         st.error(f'Error connecting to server: {e}')

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
        login_email = st.sidebar.text_input('Please enter your email address', value="admin@castlab.com", disabled=False)
        login_password = st.sidebar.text_input('Please enter your password',type = 'password', value="admin@castlab", disabled=False)
        login = st.sidebar.checkbox('Login')

        # st.markdown("<a href='#' id='forgot-password-link'>Forgot password?</a>", unsafe_allow_html=True)

        if st.checkbox("Forgot password?"):
            st.session_state.show_reset_form = True
        else:
            st.session_state.show_reset_form = False

        # if 'show_reset_form' not in st.session_state:
        #     st.session_state.show_reset_form = False

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
                    db.child("cast_lab_users").child(user['localId']).set({
                        "userid": user['localId'],
                        "name": signup_name,
                        "email": signup_email,
                        "affiliation": affiliation,
                        "status": "Not verified"
                    })
                except:
                    st.error("Failed to create account")
            else:
                st.error("Passwords do not match")

        st.markdown("</div>", unsafe_allow_html=True)
        
    if login:
        try:
            user = auth.sign_in_with_email_and_password(login_email, login_password)
            st.success("Successfully logged in!")  
            user_data = db.child("cast_lab_users").child(user['localId']).get().val()
            status = user_data.get("status")
            if status == "Verified":
                # st.write(status)
                # st.write("IP address - 10.101.247.225")
                # st.write("Username - swavaf")
                # st.write("Password - swavaf@123")
                # if st.button('Connect Host'):
                #     if ip_address:
                #         st.write("Connecting...")
                #         data = fetch_data_from_host(ip_address)
                #         st.write("Response:")
                #         st.write(data)
                #     else:
                #         st.write("Connection failed")
                option1 = st.radio("", ('Request Resources', 'Account'), horizontal=True)
                if option1 == 'Account':
                    try:
                        user_data = db.child("cast_lab_users").child(user['localId']).get().val()
                        display_user_data(user_data)
                    except:
                        st.error("Error fetching user")
                else:
                    # Input fields for the form
                    gpus = st.number_input("Number of GPUs required", min_value=1, step=1)
                    hours = st.number_input("Number of hours", min_value=1, step=1)
                    container = st.selectbox("Select a container", ["Container 1", "Container 2", "Container 3"])

                    # Date and time input
                    date = st.date_input("Select a date", value=datetime.today())
                    time = st.time_input("Select a time", value=datetime.now().time())

                    # Additional notes
                    notes = st.text_area("Additional Notes")

                    # Button to send the request
                    if st.button("Send Request"):
                        send_request(gpus, hours, container, date, time, notes)
            elif status == "Not verified":
                st.markdown("**User not verified. Please wait for verification.**")
            elif status == "Admin":
                # st.write(status)
                # st.write("IP address - 10.101.247.225")
                # st.write("Username - swavaf")
                # st.write("Password - swavaf@123")
                # if st.button('Connect Host'):
                #     if ip_address:
                #         st.write("Connecting...")
                #         data = fetch_data_from_host(ip_address)
                #         st.write("Response:")
                #         st.write(data)
                #     else:
                #         st.write("Connection failed")
                option = st.radio("", ('Request Resources', 'Manage User'), horizontal=True)
                if option == 'Manage User':
                    try:
                        user_data = db.child("cast_lab_users").get().val()
                        display_all_user_data(user_data)
                    except:
                        st.error("Error fetching user")
                else:
                    # Input fields for the form
                    gpus = st.number_input("Number of GPUs required", min_value=1, step=1)
                    hours = st.number_input("Number of hours", min_value=1, step=1)
                    container = st.selectbox("Select a container", ["Container 1", "Container 2", "Container 3"])

                    # Date and time input
                    date = st.date_input("Select a date", value=datetime.today())
                    time = st.time_input("Select a time", value=datetime.now().time())

                    # Additional notes
                    notes = st.text_area("Additional Notes")

                    # Button to send the request
                    if st.button("Send Request"):
                        send_request(gpus, hours, container, date, time, notes)
                        
        except:
                st.error("Invalid email or password")

def display_all_user_data(user_data):
    st.write("## Manage User Details")
    for user_id, data in user_data.items():
        st.write(f"**User ID:** {user_id}")
 
        # Create columns for Name and Affiliation
        col1, col2 = st.columns([1, 2])  # Adjust column ratios as needed
        
        with col1:
            st.write(f"**Name:** {data['name']}")
        
        with col2:
            st.write(f"**Affiliation:** {data['affiliation']}") 

        
        # Create columns for Name and Affiliation
        col3, col4 = st.columns([1, 2])  # Adjust column ratios as needed
        
        with col3:
            st.write(f"**Email:** {data['email']}")
        
        with col4:
            st.write(f"**Status:** {data['status']}")

        
        if st.checkbox(f"**Verify:** {user_id}"):
            # Approve user logic here
            st.write(f"Please confirm verification for this User")
            if st.button(f"**Verify:** {user_id}"):
                db.child("cast_lab_users").child(user_id).update({"status": "Verified"})
                st.write(f"User {user_id} verified.")
        
        if st.checkbox(f"**Delete:** {user_id}"):
            # Delete user logic here
            st.write(f"Do you want to delete this User?")
            if st.button(f"**Delete:** {user_id}"):
                db.child("cast_lab_users").child(user_id).remove()
                st.write(f"User {user_id} deleted.")
        
        st.markdown(
            "<hr style='border: 2px solid #f3f3f3; margin-top: 20px; margin-bottom: 20px;'>",
            unsafe_allow_html=True,
        )  # Custom separator with style

def display_user_data(user_data):
    st.write("## User Details")
    st.write(f"**User ID:** {user_data['userid']}")
 
    # Create columns for Name and Affiliation
    col1, col2 = st.columns([1, 2])  # Adjust column ratios as needed
        
    with col1:
        st.write(f"**Name:** {user_data['name']}")
        
    with col2:
        st.write(f"**Affiliation:** {user_data['affiliation']}") 

        
    # Create columns for Name and Affiliation
    col3, col4 = st.columns([1, 2])  # Adjust column ratios as needed
        
    with col3:
        st.write(f"**Email:** {user_data['email']}")
        
    with col4:
        st.write(f"**Status:** {user_data['status']}")

        
    # if st.checkbox(f"**Verify:** {user_id}"):
    #     # Approve user logic here
    #     st.write(f"Please confirm verification for this User")
    #     if st.button(f"**Verify:** {user_id}"):
    #         db.child("cast_lab_users").child(user_id).update({"status": "Verified"})
    #         st.write(f"User {user_id} verified.")
        
    if st.checkbox(f"**Delete:** {user_data['userid']}"):
        # Delete user logic here
        st.write(f"Do you want to delete this User Account?")
        if st.button(f"**Delete:** {user_data['userid']}"):
            db.child("cast_lab_users").child(user_data['userid']).remove()
            st.write(f"User {user_data['userid']} deleted.")
        
    st.markdown(
        "<hr style='border: 2px solid #f3f3f3; margin-top: 20px; margin-bottom: 20px;'>",
        unsafe_allow_html=True,
    )  # Custom separator with style
        

        
if __name__ == "__main__":
    main()
