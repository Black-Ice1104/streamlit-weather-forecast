
import yagmail
import pandas
import streamlit as st
from backend import get_data
import datetime

a = 1
sender_addr = st.secrets.email_key.sender_addr
sender_pswd = st.secrets.email_key.sender_pswd

IS_RELEASED = st.secrets.oauth_key.IS_RELEASED
if IS_RELEASED == "True":
    main = "https://streamlit-weather-forecast.herokuapp.com/"
    original = "https://streamlit-weather-forecast.herokuapp.com/Subscribe"
else:
    main = "http://localhost:8501"
    original = "http://localhost:8501/Subscribe"

# store the user info from the subscribe form
def store_subscribe(firstname, lastname, address, city):
    # read in previous user data
    firstnames = []
    lastnames = []
    addresses = []
    cities = []
    timezones = []
    email_contents = []
    df = pandas.read_excel('users.xlsx', sheet_name="users")
    repeat = False  # will only append new subscriber when unrepeated with current ones

    for idx, row in df.iterrows():
        if row['city'] != "Null":
            firstnames.append(row['firstname'])
            lastnames.append(row['lastname'])
            addresses.append(row['address'])
            cities.append(row['city'])
            timezones.append(row['timezone'])
            email_contents.append(row['email_content'])
            if not repeat:
                if row['city'] == city and row['address'] == address:
                    repeat = True

    # add the new subscriber to the last row
    if not repeat:
        firstnames.append(firstname)
        lastnames.append(lastname)
        addresses.append(address)
        cities.append(city)
        timezone = str(int(get_data(city, 1)[1]))
        timezones.append(timezone)
        email_contents.append("Null")

    # write in file
    columns = ['firstname', 'lastname', 'address', 'city', 'timezone', 'email_content']
    df = pandas.DataFrame(list(zip(firstnames, lastnames, addresses, cities, timezones, email_contents)), columns=columns)
    with pandas.ExcelWriter('users.xlsx', mode='a', if_sheet_exists='overlay') as writer:
        df.to_excel(writer, sheet_name='users')
    return repeat


def cities_subscribed(address):
    cities = []
    df = pandas.read_excel('users.xlsx', sheet_name="users")
    for idx, row in df.iterrows():
        # will only append subscribers other than the ones to unsubscribe
        if address == row['address']:
            cities.append(row['city'])
    return cities


def unsubscribe(address, city):
    # read in previous user data
    firstnames = []
    lastnames = []
    addresses = []
    cities = []
    timezones = []
    email_contents = []
    df = pandas.read_excel('users.xlsx', sheet_name="users")

    for idx, row in df.iterrows():
        # will only append subscribers other than the ones to unsubscribe
        if address != row['address'] or city != row['city']:
            firstnames.append(row['firstname'])
            lastnames.append(row['lastname'])
            addresses.append(row['address'])
            cities.append(row['city'])
            timezones.append(row['timezone'])
            email_contents.append(row['email_content'])

    # add a null position at the end to cover the previous one
    firstnames.append("")
    lastnames.append("")
    addresses.append("")
    cities.append("Null")
    timezones.append("")
    email_contents.append("")

    # write in file
    columns = ['firstname', 'lastname', 'address', 'city', 'timezone', 'email_content']
    df = pandas.DataFrame(list(zip(firstnames, lastnames, addresses, cities, timezones, email_contents)), columns=columns)
    with pandas.ExcelWriter('users.xlsx', mode='a', if_sheet_exists='overlay') as writer:
        df.to_excel(writer, sheet_name='users')




# send emails to the user about subscription successful
def send_subscribe(firstname, address, city):
    body = f""" 
           Hi, {firstname}\n
           \tThis is Weather Forecast Web App
           \tYou have successfully subscribed to our daily reminder service!
           \tWe will send you an email about the weather in {city} at 6am every day.
           \tHave a nice day! \n
           \tTo unsubscribe, visit {original}
           """
    email = yagmail.SMTP(user=sender_addr, password=sender_pswd)
    email.send(to=address,
               subject=f"Subscription successful to the Weather Forecast Web App!",
               contents=body
               )
    print("emails sent to " + address)


# send a weather forecast email to the subscriber at 6pm every day
def send_weather():
    # read in user data
    firstnames = []
    lastnames = []
    addresses = []
    cities = []
    timezones = []
    email_contents = []
    df = pandas.read_excel('users.xlsx', sheet_name="users")

    for idx, row in df.iterrows():
        firstnames.append(row['firstname'])
        lastnames.append(row['lastname'])
        addresses.append(row['address'])
        cities.append(row['city'])
        timezones.append(row['timezone'])

        timezone = int(row['timezone'])
        # the now time is GMT i.e. Greenwich Mean Time
        # store the content of the email(to be sent at 6am) at 9pm in the current timezone
        if datetime.datetime.now().hour == GMT_to_localtime(21, timezone):
            place = row['city']
            days = 1
            filtered_data = get_data(place, days)[0]
            times = [dicts["dt_txt"] for dicts in filtered_data]
            temperatures = [dicts["main"]["temp"] for dicts in filtered_data]
            sky_conditions = [dicts["weather"][0]["main"] for dicts in filtered_data]

            # the weather detail
            layout = []
            for i, item in enumerate(times):
                layout.append(times[i]+'\t'+str(temperatures[i])+'℃\t'+sky_conditions[i]+'\n')

            # the email content
            body = f""" 
                   Hi, {row['firstname']}\n
                   \tThis is Weather Forecast Web App
                   \tSee what's the weather like in {row['city']} today!\n
                   """
            for item in layout:
                body += item
            body += "\nHave a wonderful day! \n"
            body += f"\tTo unsubscribe, visit {original}"

            email_contents.append(body)  # update the email content
        else:
            email_contents.append(row['email_content'])  # update the email content

        # send email if it is 6am at the current timezone
        # if datetime.datetime.now().hour == GMT_to_localtime(6, timezone) and row['email_content'] != "Null":
        if datetime.datetime.now().hour == GMT_to_localtime(6, timezone):
            email = yagmail.SMTP(user=sender_addr, password=sender_pswd)
            email.send(to=row['address'],
                       subject=f"Your Weather Forecast for {row['city']} today!",
                       contents=row['email_content']
                       )
            print("emails sent to " + row['address'])

    columns = ['firstname', 'lastname', 'address', 'city', 'timezone', 'email_content']
    df = pandas.DataFrame(list(zip(firstnames, lastnames, addresses, cities, timezones, email_contents)), columns=columns)
    with pandas.ExcelWriter('users.xlsx', mode='a', if_sheet_exists='overlay') as writer:
        df.to_excel(writer, sheet_name='users')


def GMT_to_localtime(GMT, timezone):
    local = GMT - timezone
    if local > 24:
        return local - 24
    elif local < 0:
        return local + 24
    else:
        return local


def download_excel():
    with open('users.xlsx', "rb") as template_file:
        df = template_file.read()
    st.download_button(label='📥 Download users data',
                       data=df,
                       file_name='users.xlsx')
