
import requests

API_KEY = "33945f61ed45603d2cb17ef86700b517"
API_KEY_2 = "75732110e5199414f9d57155fbed54a6"
units = ["metric", "imperial", ""] # temperature in Celsius / Fahrenheit / Kelvin (absolute temperature scale)


def get_data(place, forecast_days=None):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={place}&appid={API_KEY}&units={units[0]}"
    # Los Angeles: https://api.openweathermap.org/data/2.5/forecast?q=los%20angeles&appid=75732110e5199414f9d57155fbed54a6&units=metric

    response = requests.get(url)
    data = response.json()
    filtered_data = data["list"]

    # Adjust time according to time zone
    time_zone = data["city"]["timezone"] / 3600  # e.g., Los Angeles: -28800 (GMT-9), Shanghai: 28800 (GMT+9)
    time_shift = round(time_zone / 3)  # the forecast gets updated every 3 hours
    if time_shift < 0:  # if later than GMT, move temperature line to former
        for x in range(0, 40 + time_shift):
            filtered_data[x]["main"]["temp"] = filtered_data[x - time_shift]["main"]["temp"]
    elif time_shift > 0:  # if earlier than GMT, move temperature line to later, and set earlier temperature to null
        for x in reversed(range(39 - time_shift)):
            filtered_data[x + time_shift]["main"]["temp"] = filtered_data[x]["main"]["temp"]
        # same thing:
        # for x in range(39 - time_shift, -1, -1):
        # or
        # for x in range(0, 40 - time_shift):
        #     filtered_data[39 - x]["main"]["temp"] = filtered_data[39 - x - time_shift]["main"]["temp"]
        for x in range(0, time_shift):
            filtered_data[x]["main"]["temp"] = None

    # Forecast update 8 times a day
    update_times = 8 * forecast_days
    filtered_data = filtered_data[:update_times]

    return filtered_data
