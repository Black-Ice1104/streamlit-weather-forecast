mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"michaelice2604@gmail.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[email_key]\n\
sender_addr = \"michaelice2604@gmail.com\"\n\
sender_pswd = \"hkkjsmtnckbcxcwp\"\n\
[weather_key]\n\
API_KEY = \"33945f61ed45603d2cb17ef86700b517\"\n\
[oauth_key]\n\
CLIENT_ID = \"731762886466-uikv4v9pfcpjosamgvv7e104jsiq9l5m.apps.googleusercontent.com\"\n\
CLIENT_SECRET = \"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\"\n\
REDIRECT_URI = \"https://streamlit-weather-forecast.herokuapp.com\"\n\
SUBSCRIBE_URI = \"https://streamlit-weather-forecast.herokuapp.com/Subscribe\"\n\
" > ~/.streamlit/secrets.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml
