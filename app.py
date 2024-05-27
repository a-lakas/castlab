import streamlit as st

def main():
    st.set_page_config(page_title="UAEU DGX-1 Portal")

    # Header
    st.markdown(
        """
        <style>
            .nav-wrapper {
                background-color: #00acc1 !important;
            }
            .brand-logo {
                color: white !important;
            }
            .logged-out a {
                color: white !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <nav class="nav-wrapper cyan darken-4">
            <div class="container">
                <a href="/" class="brand-logo">DGX-1 Portal</a>
                <a href="#" class="sidenav-trigger" data-target="mobile-links">
                    <i class="material-icons">menu</i>
                </a>
                <ul class="right hide-on-med-and-down">
                    <li class="logged-out"><a href="/login">Login/Sign Up</a></li>
                    <li class="logged-out"><a href="/faq">FAQ</a></li>
                </ul>
            </div>
        </nav>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <ul class="sidenav" id="mobile-links">
            <li class="logged-out"><a href="/login">Login/Sign Up</a></li>
            <li class="logged-out"><a href="/faq">FAQ</a></li>
        </ul>
        """,
        unsafe_allow_html=True
    )

    # Login Form
    st.markdown(
        """
        <section class="section container" style="width: 100%;">
            <div class="row">
                <div class="col s12 m5 offset-m1 center">
                    <div style="margin:15%">
                        <h2 class="cyan-text text-darken-4 center">Login</h2>
                        <form id="login_form" action="/login" method="POST">
                            <div class="input-field">
                                <input id="login_email" name="login_email" type="email" value="">
                                <label for="login_email">Your Email</label>
                            </div>
                            <div class="input-field">
                                <input id="login_password" name="login_password" type="password" class="validate">
                                <label for="login_password">Your Password</label>
                            </div>
                            <button class="btn waves-effect waves-light right" type="submit" name="login">Login
                                <i class="material-icons right">send</i>
                            </button>
                            <div>
                                <a href="/reset_password">Forgot password?</a>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </section>
        """,
        unsafe_allow_html=True
    )

    # Sign up Form
    st.markdown(
        """
        <div class="col s12 m5 center" style="border-left: 1px solid gray;">
            <div style="margin:10%">
                <h2 class="cyan-text text-darken-4 center">Sign up</h2>
                <form id="signup_form" action="/login" method="POST">
                    <div class="input-field" style="margin-top:30px; margin-bottom:15px;">
                        <select id="affiliation_selector" name="affiliation_id">
                            <option value="1">Student</option>
                            <option value="2">Faculty</option>
                            <option value="3">Research</option>
                        </select>
                        <label>Affiliation</label>
                    </div>
                    <div class="input-field">
                        <input type="text" id="signup_name" name="signup_name" value="">
                        <label for="signup_name">Your Name</label>
                    </div>
                    <div class="input-field">
                        <input type="email" id="signup_email" name="signup_email" value="">
                        <label for="signup_email">Your Email</label>
                    </div>
                    <div class="input-field">
                        <input type="password" id="signup_password" name="signup_password" class="validate" value="">
                        <label for="signup_password">Your Password</label>
                    </div>
                    <div class="input-field">
                        <input type="password" id="signup_confirm-password" name="signup_confirm_password" class="validate" value="">
                        <label for="signup_password">Confirm Password</label>
                    </div>
                    <button class="btn waves-effect waves-light right" type="submit" name="signup">Sign up
                        <i class="material-icons right">send</i>
                    </button>
                </form>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
