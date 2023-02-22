mkdir -p ~/.streamlit/

echo "\
[email_key]\n\
sender_addr = \"michaelice2604@gmail.com\"\n\
sender_pswd = \"hkkjsmtnckbcxcwp\"\n\
[weather_key]\n\
API_KEY = \"33945f61ed45603d2cb17ef86700b517\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml
