
from numpy import void
import streamlit as st
import asyncio
# https://frankie567.github.io/httpx-oauth/oauth2/
from httpx_oauth.clients.google import GoogleOAuth2


CLIENT_ID = st.secrets.oauth_key.CLIENT_ID
CLIENT_SECRET = st.secrets.oauth_key.CLIENT_SECRET
REDIRECT_URI = st.secrets.oauth_key.REDIRECT_URI

async def get_authorization_url(client: GoogleOAuth2, redirect_uri: str):
    authorization_url = await client.get_authorization_url(redirect_uri, scope=["profile", "email"])
    return authorization_url


async def get_access_token(client: GoogleOAuth2, redirect_uri: str, code: str):
    token = await client.get_access_token(code, redirect_uri)
    return token


async def get_email(client: GoogleOAuth2, token: str):
    user_id, user_email = await client.get_id_email(token)
    return user_id, user_email


def get_login_str():
    client: GoogleOAuth2 = GoogleOAuth2(CLIENT_ID, CLIENT_SECRET)
    authorization_url = asyncio.run(get_authorization_url(client, REDIRECT_URI))
    return f''' 
    <a target="_self" 
    href="{authorization_url}">Login via Google</a>'''

def get_login_url():
    client: GoogleOAuth2 = GoogleOAuth2(CLIENT_ID, CLIENT_SECRET)
    authorization_url = asyncio.run(get_authorization_url(client, REDIRECT_URI))
    return authorization_url

def get_back():
    return st.secrets.oauth_key.SUBSCRIBE_URI

def get_address():
    # get the code from the url
    # if st.experimental_get_query_params() != {}:  # if already logged in
    client: GoogleOAuth2 = GoogleOAuth2(CLIENT_ID, CLIENT_SECRET)
    code = st.experimental_get_query_params()['code']
    token = asyncio.run(get_access_token(client, REDIRECT_URI, code))
    user_id, user_email = asyncio.run(get_email(client, token['access_token']))
    st.write(f"You're logged in as {user_email} and id is {user_id}")
    return user_email
    # else:
    #     return None
