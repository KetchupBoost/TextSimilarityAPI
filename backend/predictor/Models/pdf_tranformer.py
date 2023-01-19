import ocrmypdf
import pandas as pd
import fitz
import os
import numpy as np
from pathlib import Path 
from glob import glob as gb
from tempfile import TemporaryDirectory

''' Get PDF '''
pdf_folder = os.chdir('./Data/raw/')
pdfs = [f for f in os.listdir(path = pdf_folder) if f.endswith('.pdf') or f.endswith('.PDF')]

error_log = {}

for file in pdfs:
    try:
        result = ocrmypdf.ocr(file, f"/{file}" ,output_type='pdf',skip_text=True,deskew=True)
    except Exception as e:
        if hasattr(e,'message'):
            error_log[file] = e.message
        else:
            error_log[file] = e
        continue

# PDF extraction
# informations we want to extract
extraction_pdfs = {}
ocr_file_list = [f for f in os.listdir(path='./Data/raw') if f.startswith('Be')]

for file in ocr_file_list:
    # save the results
    # pages_df = pages_df = pd.DataFrame(columns=['text'])
    pages_df = []
    # file reader
    doc = fitz.open(file)

    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        pages_df = pages_df.append(page.get_text('text'))

    extraction_pdfs[file] = pages_df