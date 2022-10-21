
import json
import streamlit
import requests
import pandas as pd
import snowflake.connector


streamlit.title('My Parents New Healty Diner')
streamlit.header('Breakfast menu')
streamlit.text('🥣 Omega 3 & Blueberry OatMeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Eggs')
streamlit.text('🥑🍞 Avocado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pd.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt')
#set idex on fruit name
my_fruit_list = my_fruit_list.set_index('Fruit')
# lets put thefruit list in a streamlit selectbox
# lists to show only selected fruits
fruits_selected = streamlit.multiselect('Select your fruits: ',list(my_fruit_list.index),['Avocado','Banana'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
#display items in the list
streamlit.dataframe(fruits_to_show)

# # new section to display the fruityvice api response
# new section with input fields
streamlit.header('Fruityvice Fruit Advice')
fruit_choice = streamlit.text_input('Enter your fruit of choice: ', 'kiwi')
streamlit.write('the user enterd:', fruit_choice)

fruityvice_response = requests.get(f'https://fruityvice.com/api/fruit/{fruit_choice}')

streamlit.text(f'https://fruityvice.com/api/fruit/{fruit_choice}')

fruityvice_response = requests.get(f'https://fruityvice.com/api/fruit/{fruit_choice}')
fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
streamlit.dataframe(fruityvice_normalized)

# query snowflake
# snowflake connection
my_cnx = snowflake.connector.connect(**streamlit.secrets['snowflake'])
my_cursor = my_cnx.cursor()
my_cursor.execute('select * from fruit_load_list')
my_data_row = my_cursor.fetchall()
streamlit.text(f'The fruits contain: ')
streamlit.dataframe(my_data_row)


# add fruits to list
add_fruit = streamlit.text_input('Enter your fruit of choice: ', 'kiwi')
#streamlit.write('the user enterd:' add_fruit)


#my_cursor.execute(f'insert into fruit_load_list values ({add_my_fruit})')

