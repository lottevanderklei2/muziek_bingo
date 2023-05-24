import streamlit as st
import pandas as pd
import random
from openpyxl import reader,load_workbook,Workbook
from pdfdocument import PDFDocument

uploaded_file = st.file_uploader("Upload je afspeellijst in excel formaat")

if uploaded_file is not None:
    try:
        dataframe = pd.read_excel(uploaded_file)
        st.write(dataframe)
    except Exception as e:
        st.error(f"Error: {str(e)}")
else:
    st.text('Je hebt nog geen bestand geüpload')

playlist = pd.DataFrame(dataframe) 

random_seed = st.number_input('Vul hier je favoriete nummer in', step=1)
st.write('Jouw favoriete nummer is: ', random_seed)
seed_num = random_seed



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
#     test = pd.DataFrame(['  ', '  ', '  ', '  ', '  ']).T
#     test2 = pd.DataFrame(['  ', '  ', '  ', '  ', '  ']).T
    df2 = pd.DataFrame(data) #, ignore_index=True)
#     df2 = df2.concat(test, ignore_index=True)
#     df2 = df2.concat(test2, ignore_index=True)
    df2.columns = cols
    df2['N'][2] = "BINGO"
    table = df2.to_records(index=False)
    return table

# df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

# card_num = st.number_input('Vul hier in hoeveel bingokaartenje wil genereren', step = 1 )
# st.write('Aantal bingokaarten ', card_num)
  
# if card_num is not None:
#     aantal_kaarten = card_num
# else: 
#     aantal_kaarten = 4
    
# def bingo_kaarten_generator2(playlist, aantal_kaarten, seed_num):
#     kaarten_list = []
#     for i in range(0, aantal_kaarten):
#         kaarten_list.append(kaart_generator2(playlist, seed_num + i))
#     return kaarten_list       
    
st.table(kaart_generator2(playlist, seed_num))

df = kaart_generator2(playlist, seed_num)
# Display the pretty DataFrame in Streamlit
st.dataframe(df.style.set_properties(**{'text-align': 'center'}))

# Create a function to download DataFrame as PDF
def download_as_pdf(df):
    # Create a new PDF document
    pdf_doc = PDFDocument()

    # Create a page and add the DataFrame as a table
    page = pdf_doc.add_page()
    table = page.add_table(df.values.tolist(), header=df.columns.tolist())

    # Set table style
    table.style = "Table Grid"

    # Generate the PDF file as binary data
    pdf_bytes = pdf_doc.render()

    return pdf_bytes

# Create a download button
if st.button('Download as PDF'):
    with st.spinner('Generating PDF...'):
        pdf_file = download_as_pdf(df)
        st.success('Download Completed!')
        st.download_button(
            label='Click to Download',
            data=pdf_file,
            file_name='dataframe.pdf',
            mime='application/pdf'
        )
        
        
# def kaart_generator(playlist, seed_num):
#     random.seed(seed_num)
#     nums = list(range(1, 51)) 
#     random.shuffle(nums)
#     playlist['random'] = nums
#     new_df = playlist.sort_values("random")
#     data = list(zip(new_df['title_and_artist'][0:5], 
#     new_df['title_and_artist'][5:10],
#     new_df['title_and_artist'][10:15],
#     new_df['title_and_artist'][15:20],
#     new_df['title_and_artist'][20:25]))
#     cols = ['B', 'I','N','G','O']
#     df2 = pd.DataFrame(data) #, ignore_index=True)
#     df2.columns = cols
#     df2['N'][2] = "BINGO"
#     return df2

# def bingo_kaarten_generator(playlist, aantal_kaarten, seed_num):
#     kaarten_list = []
#     for i in range(0, aantal_kaarten):
#         kaarten_list.append(kaart_generator(playlist, seed_num + i))
#     return kaarten_list


# def highlight_bingo(ser):
#     highlight = 'background-color:#4A707D'
#     default = ''
#     return [highlight if 'BINGO' in str(e) else default for e in ser] 

# df_styled = []
# for i in range(0, aantal_kaarten):
#     df_styled.append(bingo_kaarten_generator(playlist, aantal_kaarten, seed_num)[i]
#      .style     
#      .hide_index()
# #      .set_caption("BINGO AURAI")
#      .set_properties(**{'background-color': 'white',                                                   
#                                     'color': 'black',                       
#                                     'border-color': 'white',
#                                     'text-align': 'center',
#                                     'text': 'bold', 
#                                     'font-family': 'Arial', 
#                                     'font-weight':'bold'})
# #      .apply(highlight_bingo, axis=0, subset=cols)
#      .set_table_styles([dict(selector='th', props=[('text-align', 'center')])]))

# for i in range(0, aantal_kaarten):
#     st.dataframe(df_styled[i])



# def kaart_generator2(playlist, seed_num):
#     random.seed(seed_num)
#     nums = list(range(1, 51)) 
#     random.shuffle(nums)
#     playlist['random'] = nums
#     new_df = playlist.sort_values("random")
#     data = list(zip(new_df['title_and_artist'][0:5], 
#     new_df['title_and_artist'][5:10],
#     new_df['title_and_artist'][10:15],
#     new_df['title_and_artist'][15:20],
#     new_df['title_and_artist'][20:25]))
#     cols = ['B', 'I','N','G','O']
#     test = pd.DataFrame(['  ', '  ', '  ', '  ', '  ']).T
#     test2 = pd.DataFrame(['  ', '  ', '  ', '  ', '  ']).T
#     df2 = pd.DataFrame(data) #, ignore_index=True)
#     df2 = df2.append(test, ignore_index=True)
#     df2 = df2.append(test2, ignore_index=True)
#     df2.columns = cols
#     df2['N'][2] = "BINGO"
#     return df2
    
# def bingo_kaarten_generator2(playlist, aantal_kaarten, seed_num):
#     kaarten_list = []
#     for i in range(0, aantal_kaarten):
#         kaarten_list.append(kaart_generator2(playlist, seed_num + i))
#     return kaarten_list    


    
# test = pd.concat(bingo_kaarten_generator2(playlist, aantal_kaarten, seed_num))
    
# @st.cache
# def convert_df(df):
#     # IMPORTANT: Cache the conversion to prevent computation on every rerun
#     return df.to_csv(index=False, header=False, sep=';').encode('UTF-16')

# csv = convert_df(test)

# st.download_button(
#     label="Download data as CSV",
#     data=csv,
#     file_name='bingo_kaarten.csv',
#     mime='text/csv',
# )



