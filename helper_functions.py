### function to gget fruityvuice data ###
def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get(f'https://fruityvice.com/api/fruit/{this_fruit_choice}')
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
    return fruityvice_normalized