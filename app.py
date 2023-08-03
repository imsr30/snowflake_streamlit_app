import streamlit as st
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URL 

my_fruit_list = pd.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt')
my_fruit_list = my_fruit_list.set_index('Fruit')

st.title("My Parents New Healthy Diner")

st.header('Breakfast Menu')
st.text('🥣 Omega 3 & Blueberry Oatmeal')
st.text('🥗 Kale, Spinach & Rocket Smoothie')
st.text('🐔 Hard-Boiled Free-Range Egg')
st.text('🥑🍞 Avacado Toast')


st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
fruits_selected = st.multiselect("Pick some fruits:", list(my_fruit_list.index), default=['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
st.dataframe(fruits_to_show)



st.header('Fruityvice Fruit Advice!')
fruit_choice = st.text_input('What fruit would you like information about ?','Kiwi')
st.write('The User Entered',fruit_choice)
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)

fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
st.dataframe(fruityvice_normalized)

my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
my_data_row = my_cur.fetchall()
st.header("The Fruit Load Contains:")
st.dataframe(my_data_row)


added_fruit = st.text_input("What fruit would you like to add ?","jackfruit")
st.write(f"Thanks for Adding {added_fruit}")
# my_cur.execute(f"INSERT INTO FRUIT_LOAD_LIST VALUES ('{added_fruit}')")
