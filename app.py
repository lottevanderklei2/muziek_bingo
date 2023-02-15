import streamlit as st
import pandas as pd
import random
from io import StringIO
# from fpdf import FPDF

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

random_seed = st.number_input('Insert your favorite number', step=1)
st.write('The current number is ', random_seed)
seed_num = random_seed

card_num = st.number_input('Insert number of cards', step = 1 )
st.write('The current number is ', card_num)
# aantal_kaarten = card_num
  
if card_num is not None:
    aantal_kaarten = card_num
else: 
    aantal_kaarten = 4


def kaart_generator(playlist, seed_num):
    random.seed(seed_num)
    nums = list(range(1, 51)) 
    random.shuffle(nums)
    playlist['random'] = nums
    new_df = playlist.sort_values("random")
#     test = pd.DataFrame([[' B '],[ ' I '], [' N '], [' G '], [' O ']], columns=['B', 'I', 'N', 'G', 'O'])
    data = list(zip(new_df['title_and_artist'][0:5], 
    new_df['title_and_artist'][5:10],
    new_df['title_and_artist'][10:15],
    new_df['title_and_artist'][15:20],
    new_df['title_and_artist'][20:25]))
    test = pd.DataFrame(['  ', '  ', '  ', '  ', '  ']).T
    test2 = pd.DataFrame([' B ', ' I ', ' N ', ' G ', ' O ']).T
    df2 = test2.append(data, ignore_index=True)
    df2 = df2.append(test, ignore_index=True)
    
#     df2 = pd.DataFrame(data) #, columns=['B', 'I', 'N', 'G', 'O'])
#     df2 = df2.append(test, ignore_index=True)
#     df2 = df2.append(test2, ignore_index=True)
    df2[2][2] = "BINGO"
    return df2

def bingo_kaarten_generator(playlist, aantal_kaarten, seed_num):
    kaarten_list = []
    for i in range(0, aantal_kaarten):
        kaarten_list.append(kaart_generator(playlist, seed_num + i))
    return kaarten_list

for i in range(0, aantal_kaarten):
    st.dataframe(bingo_kaarten_generator(playlist, aantal_kaarten, seed_num)[i])
    
test = pd.concat(bingo_kaarten_generator(playlist, aantal_kaarten, seed_num))
    
@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

csv = convert_df(test)

st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='large_df.csv',
    mime='text/csv',
)

# import streamlit as st

# with open("dummy.pdf", "rb") as pdf_file:
#     PDFbyte = pdf_file.read(bingo_kaarten_generator(playlist, aantal_kaarten, seed_num)[0])

# st.download_button(label="Export_Report",
#                     data=PDFbyte,
#                     file_name="test.pdf",
#                     mime='application/octet-stream')


