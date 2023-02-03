import os
import fitz
import ocrmypdf
import json

PATH_PDF = './Data/raw/'


def get_pdf(path=PATH_PDF):
    pdfs_list = [f for f in os.listdir(path) if f.endswith('.pdf') or f.endswith('.PDF')]
    error_log = {}

    for pdfs in pdfs_list:
        try:
            ocrmypdf.ocr(path + pdfs, path + pdfs, output_type='pdf', skip_text=True, deskew=True)
        except Exception as e:
            error_log[pdfs] = e


# Save Dict in a JsonFile
def text_json_save(dict_text):
    json_pdfs = json.dumps(dict_text)

    with open('./Data/json/pdf_dict.json', 'w') as json_file:
        json_file.write(json_pdfs)


# PDF extraction
# informations we want to extract
def extract_text(path):
    pdfs_list = [f.split('.')[0] for f in os.listdir(path) if f.endswith(('.pdf', '.PDF'))]
    extracted_text = {}
    print(pdfs_list)
    for pdf_name in pdfs_list:
        pages_df = []
        # pdf_name reader
        doc = fitz.open(f'{path}/{pdf_name}.pdf')
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            pages_df.append(page.get_text('text'))
        extracted_text[pdf_name] = pages_df

        pdf_json = json.dumps(extracted_text)
        with open(f'./Data/json/{pdf_name}.json', 'w') as file_json:
            file_json.write(pdf_json)



