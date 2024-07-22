import os
from PyPDF2 import PdfReader

# Directory containing PDF files
pdf_directory = 'graphfleet/input/pdf'  
# Directory to save the .txt files
txt_directory = 'graphfleet/input'  

# Function to convert PDF to text (no changes here)
def convert_pdf_to_txt(pdf_path, txt_path):
    with open(pdf_path, 'rb') as pdf_file:
        reader = PdfReader(pdf_file)
        text = ''
        for page_num in range(len(reader.pages)):
            text += reader.pages[page_num].extract_text()
        with open(txt_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(text)

# Loop through all PDF files in the directory
for filename in os.listdir(pdf_directory):
    if filename.endswith('.pdf'):
        pdf_path = os.path.join(pdf_directory, filename)
        # Create the txt_path using the txt_directory:
        txt_path = os.path.join(txt_directory, filename.replace('.pdf', '.txt'))  
        convert_pdf_to_txt(pdf_path, txt_path)
        print(f'Converted {filename} to text.')
