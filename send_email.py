
import yagmail
import pandas
from backend import get_data

sender_addr = "michaelice2604@gmail.com"
sender_pswd = "hkkjsmtnckbcxcwp"


# store the user info from the subscribe form
def store_subscribe(firstname, lastname, address, city):
    # read in previous user data
    firstnames = []
    lastnames = []
    addresses = []
    cities = []
    df = pandas.read_excel('users.xlsx', sheet_name="users")
    for idx, row in df.iterrows():
        firstnames.append(row['firstname'])
        firstnames.append(row['firstname'])
        lastnames.append(row['lastname'])
        addresses.append(row['address'])
        cities.append(row['city'])

    # add the new subscriber to the last row
    firstnames.append(firstname)
    lastnames.append(lastname)
    addresses.append(address)
    cities.append(city)

    # write in file
    columns = ['firstname', 'lastname', 'address', 'city']
    df = pandas.DataFrame(list(zip(firstnames, lastnames, addresses, cities)), columns=columns)
    with pandas.ExcelWriter('users.xlsx', mode='a', if_sheet_exists='overlay') as writer:
        df.to_excel(writer, sheet_name='users')


# send emails to the user about subscription successful
def send_subscribe(firstname, address, city):
    body = f""" 
           Hi, {firstname}\n
           \tThis is Weather Forecast Web App
           \tYou have successfully subscribed to our daily reminder service!
           \tWe will send you an email about the weather in {city} at 6pm every day.
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
        place = row['city']
        days = 1
        filtered_data = get_data(place, days)
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