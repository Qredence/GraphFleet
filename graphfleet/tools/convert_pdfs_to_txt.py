# Import libraries
import os
from PyPDF2 import PdfReader
import ipywidgets as widgets
from IPython.display import display, clear_output

# Define the directory to save the .txt files
txt_directory = '../graphfleet/input'
if not os.path.exists(txt_directory):
    os.makedirs(txt_directory)

# Create upload button
uploader = widgets.FileUpload(
    accept='.pdf',  # Accept only PDF files
    multiple=True   # Allow uploading multiple files
)

# Create output area
output = widgets.Output()

# Conversion function
def convert_pdfs(change):
    with output:
        clear_output()  # Clear previous output

        uploaded_files = change['new']
        if uploaded_files:
            # Correctly handle uploaded_files as a tuple
            for uploaded_info in uploaded_files:
                uploaded_file_name = uploaded_info.name
                content = uploaded_info.content

                # Save the uploaded PDF temporarily 
                temp_pdf_path = uploaded_file_name
                with open(temp_pdf_path, 'wb') as f:
                    f.write(content)

                # Define output .txt filename within txt_directory
                txt_filename = os.path.join(txt_directory, uploaded_file_name.replace(".pdf", ".txt"))

                # Convert the PDF to text
                convert_pdf_to_txt(temp_pdf_path, txt_filename)
                print(f"Converted {uploaded_file_name} to {txt_filename}")

                # (Optional) Remove the temporary PDF file
                os.remove(temp_pdf_path) 

# Function to convert PDF to text (no changes needed)
def convert_pdf_to_txt(pdf_path, txt_path):
    with open(pdf_path, 'rb') as pdf_file:
        reader = PdfReader(pdf_file)
        text = ''
        for page_num in range(len(reader.pages)):
            text += reader.pages[page_num].extract_text()
    with open(txt_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(text)

# Observe changes in the upload widget
uploader.observe(convert_pdfs, names='value')

# Display the upload button and output area
display(uploader)
display(output)