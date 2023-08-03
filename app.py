import streamlit as st
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

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

def get_fruityvice_data(fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
  fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
  return fruityvice_normalized
  

st.header('Fruityvice Fruit Advice!')

try:
  fruit_choice = st.text_input('What fruit would you like information about ?')
  if fruit_choice:
    fruity_data = get_fruityvice_data(fruit_choice)
    st.dataframe(fruity_data)
  else:
    st.error("Please Select a fruit to get the information.")
except URLError as e:
  st.error()

def get_connections():
  my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
  my_cur = my_cnx.cursor()
  return my_cur

def fruit_load_list():
  conn = get_connections()
  conn.execute("SELECT * FROM FRUIT_LOAD_LIST")
  my_data_row = conn.fetchall()
  st.header("The Fruit Load Contains:")
  st.dataframe(my_data_row)

def load_new_fruit(added_fruit):
  st.write(f"Thanks for Adding {added_fruit}")
  conn = get_connections()
  conn.execute(f"INSERT INTO FRUIT_LOAD_LIST VALUES ('{added_fruit}')")


st.header("The Fruit Load Contains")

if st.button("Get Fruit Load List"):
  fruit_load_list()

added_fruit = st.text_input("What fruit would you like to add ?",placeholder = "jackfruit")

if st.button("Add a fruit to the list"):
  load_new_fruit(added_fruit)
