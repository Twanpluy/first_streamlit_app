
import streamlit
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

# lets put the fruit list in a streamlit selectbox

# lists to show only selected fruits
fruits_selected = streamlit.multiselect('Select your fruits: ',list(my_fruit_list.index),['Avocado','Banana'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
#display items in the list
streamlit.dataframe(fruits_to_show)
