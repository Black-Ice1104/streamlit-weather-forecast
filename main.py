
from frontend import web
from send_email import *
import datetime
import time

if __name__ == "__main__":
    web()
    while True:
        if datetime.datetime.now().hour == 6 and datetime.datetime.now().minute == 0:
            send_weather()
        time.sleep(60)

