import streamlit as st
import pandas as pd
import random
from io import StringIO

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()

    # To convert to a string based IO:
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))

    # To read file as string:
    string_data = stringio.read()

    # Can be used wherever a "file-like" object is accepted:
    dataframe = pd.read_csv(uploaded_file)
    st.write(dataframe)
else: 
    st.text('No file uploaded')

playlist = pd.DataFrame(dataframe)  
# card_num = st.number_input('Insert number of cards')
# st.write('The current number is ', card_num)

random_seed = st.number_input('Insert your favorite number', step=1)
st.write('The current number is ', random_seed)

aantal_kaarten = 2
  
# if card_num is not None:
#     aantal_kaarten = card_num
# else: 
#     aantal_kaarten = 4
seed_num = random_seed

def kaart_generator(playlist, seed_num):
    random.seed(seed_num)
    nums = list(range(1, 51)) 
    random.shuffle(nums)
    playlist['random'] = nums
    new_df = playlist.sort_values("random")
    data = list(zip(new_df['title_and_artist'][0:5], 
        new_df['title_and_artist'][5:10],
        new_df['title_and_artist'][10:15],
        new_df['title_and_artist'][15:20],
        new_df['title_and_artist'][20:25]))
    df2 = pd.DataFrame(data)
    df2[2][2] = "BINGO"
    return df2

def bingo_kaarten_generator(playlist, aantal_kaarten, seed_num):
    kaarten_list = []
    for i in range(0, aantal_kaarten):
        kaarten_list.append(kaart_generator(playlist, seed_num + i))
    return kaarten_list

for i in range(0, aantal_kaarten):
    st.dataframe(bingo_kaarten_generator(playlist, aantal_kaarten, seed_num)[i])

