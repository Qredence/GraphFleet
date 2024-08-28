import os
from pathlib import Path
from pypdf import PdfReader

def convert_pdf_to_txt(pdf_path, txt_path):
    with open(pdf_path, 'rb') as file:
        pdf_reader = PdfReader(file)
        text = ''
        for page in pdf_reader.pages:
            text += page.extract_text()
    
    with open(txt_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(text)

def main():
    pdf_dir = Path('graphfleet/data/pdf')
    txt_dir = Path('graphfleet/data')

    # Create the output directory if it doesn't exist
    txt_dir.mkdir(parents=True, exist_ok=True)

    for pdf_file in pdf_dir.glob('*.pdf'):
        txt_file = txt_dir / f"{pdf_file.stem}.txt"
        print(f"Converting {pdf_file} to {txt_file}")
        convert_pdf_to_txt(pdf_file, txt_file)

if __name__ == "__main__":
    main()