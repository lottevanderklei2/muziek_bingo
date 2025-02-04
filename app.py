import streamlit as st
import pandas as pd
import random
from fpdf import FPDF
from io import BytesIO

# Set up the page title and layout
st.set_page_config(page_title="Muziek Bingo", layout="centered")

# Title of the app
st.title("Muziek Bingo")

# File uploader box
uploaded_file = st.file_uploader("Upload je afspeellijst in Excel-formaat")
if uploaded_file is not None:
    try:
        playlist = pd.read_excel(uploaded_file)
        st.write(playlist)
    except Exception as e:
        st.error(f"Error: {str(e)}")
        st.stop()
else:
    st.warning("Je hebt nog geen bestand geüpload")
    st.stop()

# Random seed input
random_seed = st.number_input('Vul hier je favoriete nummer in', step=1, value=0)
st.write('Jouw favoriete nummer is: ', random_seed)

# Function to generate a single bingo card
def kaart_generator(playlist, seed_num):
    random.seed(seed_num)
    shuffled_playlist = playlist.sample(frac=1, random_state=seed_num).reset_index(drop=True)
    data = [shuffled_playlist.iloc[i * 5:(i + 1) * 5]['title_and_artist'].tolist() for i in range(5)]
    
    df = pd.DataFrame(data, columns=['B', 'I', 'N', 'G', 'O'])
    df.at[2, 'N'] = "BINGO"  # Center free space
    return df

# Input number of bingo cards
card_num = st.number_input('Hoeveel bingokaarten wil je genereren?', step=1, min_value=1, value=1)
st.write(f'Aantal bingokaarten: {card_num}')

# Generate bingo cards
kaarten_list = [kaart_generator(playlist, random_seed + i) for i in range(card_num)]

# Display first generated bingo card
st.table(kaarten_list[0])

# PDF class with proper formatting
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Bingo Cards', ln=True, align='C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def add_table(self, df, card_number):
        self.add_page()
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, f'Bingo Card {card_number}', ln=True, align='C')
        self.ln(5)

        table_size = 180  # Square table fitting within A4 landscape
        col_width = table_size / 5
        row_height = table_size / 5 / 2.5  # Adjusted for multi-line text
        x_start = (self.w - table_size) / 2

        # Table header
        self.set_x(x_start)
        for col_name in df.columns:
            self.cell(col_width, row_height, col_name, border=1, align='C')
        self.ln(row_height)

        # Table rows
        self.set_font('Arial', '', 10)
        for row in df.itertuples(index=False):
            self.set_x(x_start)
            for cell in row:
                self.multi_cell(col_width, row_height, str(cell), border=1, align='C')
            self.ln(row_height)

# Generate PDF function
def generate_pdf(cards):
    pdf = PDF(orientation='L', unit='mm', format='A4')
    for i, card in enumerate(cards, start=1):
        pdf.add_table(card, i)
    pdf_output = BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)
    return pdf_output

# Button to download PDF
if st.button('Download als PDF'):
    with st.spinner('PDF wordt gegenereerd...'):
        pdf_file = generate_pdf(kaarten_list)
        st.download_button(
            label='Klik hier om te downloaden',
            data=pdf_file,
            file_name='bingo_kaarten.pdf',
            mime='application/pdf'
        )
