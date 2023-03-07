
from send_email import *

st.header("Subscribe")
with st.form(key="email_forms"):
    city = st.text_input("The city / region to subscribe")
    address = st.text_input("Your email address")
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
