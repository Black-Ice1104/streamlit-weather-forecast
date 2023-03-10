
import plotly.express as px
from send_email import *
def web():
    # Add title, text input, slider, select box and subheader
    st.title("Weather Forecast for the Next Days")
    place = st.text_input("Place: ")
    days = st.slider("Forecast Days", min_value=1, max_value=5, help="Select the number of forecast days")
    option = st.selectbox("Select data to view",
                          options=["Temperature", "Sky"])
    # using fstring because the header is dynamic (any change in place, days or option would change the header)
    st.subheader(f"{option} for the next {days} days in {place}")
    if place:
        try:
            # Get the temperature / sky data
            filtered_data = get_data(place, days)[0]
            # print(get_data(place, days)[1])

            if option == "Temperature":
                temperatures = [dict["main"]["temp"] for dict in filtered_data]
                dates = [dict["dt_txt"] for dict in filtered_data]
                # Create a temperature plot
                figure = px.line(x=dates, y=temperatures, labels={"x": "Dates", "y": "Temperature (C)"})
                st.plotly_chart(figure, use_container_width=True)

            if option == "Sky":
                images = {"Clear": "images/clear.png",
                          "Clouds": "images/cloud.png",
                          "Rain": "images/rain.png",
                          "Snow": "images/snow.png"}
                sky_conditions = [dict["weather"][0]["main"] for dict in filtered_data]
                image_paths = [images[condition] for condition in sky_conditions]
                text_layout = [condition for condition in sky_conditions]
                st.image(image_paths, width=132)
        except KeyError:
            st.write("The place does not exist. Please modify the place name and press Enter again.")
