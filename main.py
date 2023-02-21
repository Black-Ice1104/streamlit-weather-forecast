
from frontend import web
from send_email import *
import datetime
import time

if __name__ == "__main__":
    web()
    # send_weather()
    # while True:
    #     if datetime.datetime.now().hour == 6 and datetime.datetime.now().minute == 15:
    #         send_weather()
    #     time.sleep(60)

    # technologies = ['Spark', 'Pandas', 'Java', 'Python', 'PHP']
    # fee = [25000, 20000, 15000, 15000, 18000]
    # discount = [2000, 1000, 800, 500, 800]
    # columns = ['Courses', 'Fee', 'Duration', 'Discount']
    # df = pandas.DataFrame(list(zip(technologies, fee, discount)), columns=columns)
    # print(df)
