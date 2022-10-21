
import json
import streamlit
import requests
import pandas as pd

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

# new section to display the fruityvice api response
fruityvice_response = requests.get('https://fruityvice.com/api/fruit/' + 'kiwi')
# normelize data view
fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
streamlit.dataframe(fruityvice_normalized)

# new section with input fields
streamlit.header('Fruityvice Fruit Advice')
fruit_choice = streamlit.text_input('Enter your fruit of choice: ', 'kiwi')
streamlit.write('the user enterd:', fruit_choice)

fruityvice_response = requests.get(f'https://fruityvice.com/api/fruit/{fruit_choice}')