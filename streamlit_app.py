
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

# lets put the fruit list in a streamlit selectbox
streamlit.multiselect('Select your fruits: ',list(my_fruit_list.index))
streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))
#display items in the list
streamlit.dataframe(my_fruit_list)
