
from send_email import *
import streamlit as st
import time
st.header("Subscribe")

IS_RELEASED = st.secrets.oauth_key.IS_RELEASED
if IS_RELEASED == "True":
    main = "https://streamlit-weather-forecast.herokuapp.com"
    original = "https://streamlit-weather-forecast.herokuapp.com/Subscribe"
elif IS_RELEASED == "Streamlit":
    main = "https://weather-forecast-subscribe.streamlit.app"
    original = "https://weather-forecast-subscribe.streamlit.app/~/+/Subscribe"
else:
    main = "http://localhost:8501"
    original = "http://localhost:8501/Subscribe?email=None"

# subscribe
with st.form(key="subscribe_forms"):
    city = st.text_input("The city / region to subscribe")
    address = st.text_input("Your Email address")
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

# unsubscribe
st.subheader("Unsubscribe")
addr_unsub = st.text_input("Please enter your email address")
if addr_unsub:
    cities = cities_subscribed(addr_unsub)
    if cities:
        city_to_del = st.multiselect("Select city / region to unsubscribe", cities)
        submit = st.button(label="Submit")
        if submit:
            for city_name in city_to_del:
                unsubscribe(addr_unsub, city_name)
                st.info("Successfully unsubscribed " + city_name + "!")
                time.sleep(5)
                st.experimental_rerun()
    else:
        st.info("You have not subscribed any cities yet!")


# entrance for administrator to download users.xlsx
for i in range(1, 20):
    st.text("")
with st.expander("Administrator Entrance"):
    id = st.text_input("Please enter admin ID number")
    password = st.text_input("Please enter admin password")
    adminID = st.secrets.admin_key.ID
    adminPSWD = st.secrets.admin_key.PSWD
    if id == adminID and password == adminPSWD:
        download_excel()
