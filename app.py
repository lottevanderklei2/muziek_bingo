import streamlit as st
import pandas as pd
import random
from io import StringIO

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
#     bytes_data = uploaded_file.getvalue()
#     stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
#     string_data = stringio.read()
    dataframe = pd.read_csv(uploaded_file, sep = ';')
    st.write(dataframe)
else: 
    st.text('No file uploaded')

playlist = pd.DataFrame(dataframe) 

random_seed = st.number_input('Insert your favorite number', step=1)
st.write('Your favorite number is ', random_seed)
seed_num = random_seed

card_num = st.number_input('Insert number of cards you want', step = 1 )
st.write('The number of cars is ', card_num)
  
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
    data = list(zip(new_df['title_and_artist'][0:5], 
    new_df['title_and_artist'][5:10],
    new_df['title_and_artist'][10:15],
    new_df['title_and_artist'][15:20],
    new_df['title_and_artist'][20:25]))
    cols = ['B', 'I','N','G','O']
#     test = pd.DataFrame(['  ', '  ', '  ', '  ', '  ']).T
#     test2 = pd.DataFrame(['  ', '  ', '  ', '  ', '  ']).T
#     test2 = pd.DataFrame([' B ', ' I ', ' N ', ' G ', ' O ']).T
    df2 = pd.DataFrame(data) #, ignore_index=True)
#     df2 = df2.append(test, ignore_index=True)
#     df2 = df2.append(test2, ignore_index=True)
    df2.columns = cols
    df2['N'][2] = "BINGO"
#     df2[2][2] = "BINGO"
    return df2

def bingo_kaarten_generator(playlist, aantal_kaarten, seed_num):
    kaarten_list = []
    for i in range(0, aantal_kaarten):
        kaarten_list.append(kaart_generator(playlist, seed_num + i))
    return kaarten_list


def highlight_bingo(ser):
    highlight = 'background-color:#4A707D'
    default = ''
    return [highlight if 'BINGO' in str(e) else default for e in ser] 

df_styled = []
for i in range(0, aantal_kaarten):
    df_styled.append(bingo_kaarten_generator(playlist, aantal_kaarten, seed_num)[i]
     .style     
     .hide_index()
#      .set_caption("BINGO AURAI")
     .set_properties(**{'background-color': 'white',                                                   
                                    'color': 'black',                       
                                    'border-color': 'white',
                                    'text-align': 'center',
                                    'text': 'bold', 
                                    'font-family': 'Arial', 
                                    'font-weight':'bold'})
#      .apply(highlight_bingo, axis=0, subset=cols)
     .set_table_styles([dict(selector='th', props=[('text-align', 'center')])]))

for i in range(0, aantal_kaarten):
    st.dataframe(df_styled[i])



def kaart_generator2(playlist, seed_num):
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
    cols = ['B', 'I','N','G','O']
    test = pd.DataFrame(['  ', '  ', '  ', '  ', '  ']).T
    test2 = pd.DataFrame(['  ', '  ', '  ', '  ', '  ']).T
#     test2 = pd.DataFrame([' B ', ' I ', ' N ', ' G ', ' O ']).T
    df2 = pd.DataFrame(data) #, ignore_index=True)
    df2 = df2.append(test, ignore_index=True)
    df2 = df2.append(test2, ignore_index=True)
    df2.columns = cols
    df2['N'][2] = "BINGO"
#     df2[2][2] = "BINGO"
    return df2

# cols = ['B', 'I','N','G','O']
# df_styled = []
# for i in range(0, aantal_kaarten):
#     df_styled.append(bingo_kaarten_generator(playlist, aantal_kaarten, seed_num)[i].columns = cols)
    
    


    
test = pd.concat(bingo_kaarten_generator2(playlist, aantal_kaarten, seed_num))
    
@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(index=False, header=False, sep=';').encode('UTF-16')

csv = convert_df(test)

st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='bingo_kaarten.csv',
    mime='text/csv',
)



