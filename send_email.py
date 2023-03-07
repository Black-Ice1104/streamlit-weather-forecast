
import yagmail
import pandas
import streamlit as st
from backend import get_data
import datetime

sender_addr = st.secrets.email_key.sender_addr
sender_pswd = st.secrets.email_key.sender_pswd


# store the user info from the subscribe form
def store_subscribe(firstname, lastname, address, city):
    # read in previous user data
    firstnames = []
    lastnames = []
    addresses = []
    cities = []
    timezones = []
    df = pandas.read_excel('users.xlsx', sheet_name="users")
    repeat = False  # will only append new subscriber when unrepeated with current ones
    for idx, row in df.iterrows():
        count = 0
        firstnames.append(row['firstname'])
        lastnames.append(row['lastname'])
        addresses.append(row['address'])
        cities.append(row['city'])
        timezones.append(row['timezone'])
        if not repeat:
            if row['firstname'] == firstname:
                count += 1
            if row['lastname'] == lastname:
                count += 1
            if row['address'] == address:
                count += 1
            if row['city'] == city:
                count += 1
            if count == 4:
                repeat = True

    # add the new subscriber to the last row
    if not repeat:
        firstnames.append(firstname)
        lastnames.append(lastname)
        addresses.append(address)
        cities.append(city)
        timezone = str(int(get_data(city, 1)[1]))
        timezones.append(timezone)

    # write in file
    columns = ['firstname', 'lastname', 'address', 'city', 'timezone']
    df = pandas.DataFrame(list(zip(firstnames, lastnames, addresses, cities, timezones)), columns=columns)
    with pandas.ExcelWriter('users.xlsx', mode='a', if_sheet_exists='overlay') as writer:
        df.to_excel(writer, sheet_name='users')
    return repeat


# send emails to the user about subscription successful
def send_subscribe(firstname, address, city):
    body = f""" 
           Hi, {firstname}\n
           \tThis is Weather Forecast Web App
           \tYou have successfully subscribed to our daily reminder service!
           \tWe will send you an email about the weather in {city} at 6am every day.
           \tHave a nice day! \n
           """
    email = yagmail.SMTP(user=sender_addr, password=sender_pswd)
    email.send(to=address,
               subject=f"Subscription successful to the Weather Forecast Web App!",
               contents=body
               )
    print("emails sent to " + address)


# send a weather forecast email to the subscriber at 6pm every day
def send_weather():
    df = pandas.read_excel('users.xlsx', sheet_name="users")
    for idx, row in df.iterrows():
        timezone = row['timezone']
        # will only send email if it is 6am in the current timezone
        if datetime.datetime.now().hour == 6 - int(timezone):  # the now time is GMT i.e. Greenwich Mean Time
            place = row['city']
            days = 1
            filtered_data = get_data(place, days)[0]
            times = [dicts["dt_txt"] for dicts in filtered_data]
            temperatures = [dicts["main"]["temp"] for dicts in filtered_data]
            sky_conditions = [dicts["weather"][0]["main"] for dicts in filtered_data]

            layout = []
            for i, item in enumerate(times):
                layout.append(times[i]+'\t'+str(temperatures[i])+'℃\t'+sky_conditions[i]+'\n')

            body = f""" 
                   Hi, {row['firstname']}\n
                   \tThis is Weather Forecast Web App
                   \tSee what's the weather like in {row['city']} today!\n
                   """
            for item in layout:
                body += item
            body += "\nHave a wonderful day!"

            email = yagmail.SMTP(user=sender_addr, password=sender_pswd)
            email.send(to=row['address'],
                       subject=f"Your Weather Forecast for {row['city']} today!",
                       contents=body
                       )
            print("emails sent to " + row['address'])
