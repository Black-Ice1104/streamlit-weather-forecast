
from send_email import *

st.header("Subscribe")
with st.form(key="email_forms"):
    city = st.text_input("The city / region to subscribe")
    address = st.text_input("Your email address")
    firstname = st.text_input("Your firstname")
    lastname = st.text_input("Your lastname")
    button = st.form_submit_button("Subscribe Now")
    if button:
        store_subscribe(firstname, lastname, address, city)
        send_subscribe(firstname, address, city)
        st.info("Subscription Successful!")