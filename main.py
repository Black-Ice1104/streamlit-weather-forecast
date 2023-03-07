
from frontend import web
from send_email import *
import datetime
import time
import multiprocessing as mp


def send_email():
    while True:
        if datetime.datetime.now().minute == 0:  # if it is on the hour
            send_weather()
            time.sleep(60 * 59)  # sleep for 59 minutes after sending email


if __name__ == "__main__":
    web()  # run the web app
    mp.Process(target=send_email).start()  # run the regular email sending service
