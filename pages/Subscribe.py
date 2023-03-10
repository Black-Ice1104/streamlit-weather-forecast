
import webbrowser
from send_email import *
from auth import *
import time
import streamlit as st
from streamlit_javascript import st_javascript
from streamlit_cookies_manager import EncryptedCookieManager
# from streamlit_extras.switch_page_button import switch_page

# def get_subscribed_city():


st.header("Subscribe")
url = st_javascript("await fetch('').then(r => window.parent.location.href)")

# This should be on top of your script
cookies = EncryptedCookieManager(
    prefix="ktosiek/streamlit-cookies-manager/",
    password=st.secrets.oauth_key.PSWD
)

IS_RELEASED = st.secrets.oauth_key.IS_RELEASED
if IS_RELEASED == "True":
    main = "https://streamlit-weather-forecast.herokuapp.com"
    original = "https://streamlit-weather-forecast.herokuapp.com/Subscribe"
    cache = cookies
    Null = None
elif IS_RELEASED == "Streamlit":
    main = "https://weather-forecast-subscribe.streamlit.app"
    original = "https://weather-forecast-subscribe.streamlit.app/Subscribe"
    cache = cookies
    Null = cookies
else:
    main = "http://localhost:8501"
    original = "http://localhost:8501/Subscribe"
    cache = cookies['a-cookie']
    Null = ''

if not cookies.ready():
    st.stop()

st.write(cookies)

if cache == Null:
    if url == original:  # not login
        st.write(get_login_str(), unsafe_allow_html=True)  # show "Login with Google"
    else:  # login, but not save cookies
        value = get_address()
        cache = value
        if IS_RELEASED == "False":
            cookies['a-cookie'] = cache
        else:
            cookies = cache
        cookies.save()  # Force saving the cookies now, without a rerun
        st.experimental_rerun()
else:  # login, with cookies saved
    # st.write("cookies != Null")
    address = cache
    # Subscribe
    with st.form(key="subscribe_forms"):
        st.subheader("Logged in as " + address)
        city = st.text_input("The city / region to subscribe")
        firstname = st.text_input("Your firstname")
        lastname = st.text_input("Your lastname")
        button = st.form_submit_button("Subscribe Now")
        if button:
            try:
                repeat = store_subscribe(firstname, lastname, address, city)
                if not repeat:
                    send_subscribe(firstname, address, city)
                    st.info("Subscription Successful!")
                else:
                    st.info("Sorry, you have already subscribed!")
            except KeyError:
                st.info("The place does not exist. Please modify the place name and subscribe again.")
    if st.button("Log out"):  # log out, delete cookies, open a new tab
        cache = Null
        if IS_RELEASED == "False":
            cookies['a-cookie'] = cache
        else:
            cookies = cache
        cookies.save()
        st.info("You have logged out. Please close the window.", icon="ℹ️")
        time.sleep(1)
        webbrowser.open(main, new=0)
        st.stop()
    cookies.save()  # Force saving the cookies now, without a rerun

    cities = cities_subscribed(address)
    if cities:
        with st.form(key="unsubscribe_forms"):
            st.subheader("Unsubscribe")
            city_to_del = st.multiselect("Select city / region to unsubscribe", cities)
            submit = st.form_submit_button(label="Submit")
            if submit:
                for city_name in city_to_del:
                    unsubscribe(address, city_name)
                    st.write("Successfully unsubscribed ", city_name)
    else:
        st.info("You have not subscribed any cities yet!")


