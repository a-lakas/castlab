import streamlit as st

def main():
    st.set_page_config(page_title="UAEU DGX-1 Portal")

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
            .container {
                margin: auto;
                padding: 20px;
                max-width: 800px;
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

    st.markdown("<div class='header'>DGX-1 Portal</div>", unsafe_allow_html=True)

    # Login Form
    with st.container():
        st.markdown("<div class='form-container'>", unsafe_allow_html=True)
        st.markdown("<h2>Login</h2>", unsafe_allow_html=True)
        login_email = st.text_input("Your Email")
        login_password = st.text_input("Your Password", type="password")
        login_button = st.button("Login")
        st.markdown("<a href='/reset_password'>Forgot password?</a>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Sign up Form
    with st.container():
        st.markdown("<div class='form-container'>", unsafe_allow_html=True)
        st.markdown("<h2>Sign up</h2>", unsafe_allow_html=True)
        affiliation = st.selectbox("Affiliation", ["Student", "Faculty", "Research"])
        signup_name = st.text_input("Your Name")
        signup_email = st.text_input("Your Email")
        signup_password = st.text_input("Your Password", type="password")
        signup_confirm_password = st.text_input("Confirm Password", type="password")
        signup_button = st.button("Sign up")
        st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
