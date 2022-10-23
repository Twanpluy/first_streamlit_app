
from distutils.util import execute
import json
#from helper_functions import get_fruityvice_data
import streamlit
import requests
import pandas as pd
import snowflake.connector
from urllib.error import URLError

### function to get fruityvuice data ###
def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get(f'https://fruityvice.com/api/fruit/{this_fruit_choice}')
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

streamlit.title('My Parents New Healty Diner')
streamlit.header('Breakfast menu')
streamlit.text('🥣 Omega 3 & Blueberry OatMeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Eggs')
streamlit.text('🥑🍞 Avocado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

### FORM FILE ###
### load file ###
my_fruit_list = pd.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt')
### Create a list of fruits ###
my_fruit_list = my_fruit_list.set_index('Fruit')
### Create selectboxes for fruits ###
fruits_selected = streamlit.multiselect('Select your fruits: ',list(my_fruit_list.index),['Avocado','Banana'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
### Display items in the list ###
streamlit.dataframe(fruits_to_show)

### FruitList ###
### Fruityvice ###
streamlit.header('Fruityvice Fruit Advice')

try:
    fruit_choice = streamlit.text_input(f'What fruit would you like to know more about?')
    if not fruit_choice:
        streamlit.error('Please enter a fruit name for information')
    else:
        fruityvice_data = get_fruityvice_data(fruit_choice)
        streamlit.dataframe(fruityvice_data)

except URLError as e:
    streamlit.error(f'Error: {e.reason}')

streamlit.header('Fruit list in Snowflake')

### Snowflake connection ###
my_cnx = snowflake.connector.connect(**streamlit.secrets['snowflake'])
### Snowflake select funciton ###
def get_fruit_load_list():
    with my_cnx.cursor() as my_cursor:
        my_cursor.execute('select * from pc_rivery_db.public.fruit_load_list')
        my_fruit_list = my_cursor.fetchall()
        return my_fruit_list

### Button to load in fruit list ###
if streamlit.button('Load Fruit List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets['snowflake'])
    my_data_rows = get_fruit_load_list()
    streamlit.dataframe(my_data_rows)



# streamlit.stop()
# # query snowflake
# # snowflake connection
# my_cnx = snowflake.connector.connect(**streamlit.secrets['snowflake'])
# my_cursor = my_cnx.cursor()
# my_cursor.execute('select * from fruit_load_list')
# my_data_row = my_cursor.fetchall()
# streamlit.text(f'The fruits contain: ')
# streamlit.dataframe(my_data_row)


# add_fruit = streamlit.text_input('Add fruit', '', key="ditismijnunieketest")
# streamlit.write('The current movie title is', add_fruit)

# my_cursor.execute("Insert into fruit_load_list (fruit_name) values ('" + add_fruit + "')")
# my_cnx.commit()

