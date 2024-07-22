import os
from PyPDF2 import PdfReader

# Directory containing PDF files
directory = 'graphfleet/input/pdf'

# Function to convert PDF to text
def convert_pdf_to_txt(pdf_path, txt_path):
    with open(pdf_path, 'rb') as pdf_file:
        reader = PdfReader(pdf_file)
        text = ''
        for page_num in range(len(reader.pages)):
            text += reader.pages[page_num].extract_text()
        with open(txt_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(text)

# Loop through all PDF files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.pdf'):
        pdf_path = os.path.join(directory, filename)
        txt_path = os.path.join(directory, filename.replace('.pdf', '.txt'))
        convert_pdf_to_txt(pdf_path, txt_path)
        print(f'Converted {filename} to text.')