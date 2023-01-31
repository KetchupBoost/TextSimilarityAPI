import os
import fitz
import ocrmypdf

PATH_PDF = './Data/raw/'


def get_pdf(path=PATH_PDF):
    pdfs_list = [f for f in os.listdir(path) if f.endswith('.pdf') or f.endswith('.PDF')]
    error_log = {}

    for pdfs in pdfs_list:
        try:
            ocrmypdf.ocr(path + pdfs, path + pdfs, output_type='pdf', skip_text=True, deskew=True)
        except Exception as e:
            error_log[pdfs] = e


# PDF extraction
# informations we want to extract
def extract_text(path=PATH_PDF):
    pdfs_list = [f for f in os.listdir(path) if f.endswith('.pdf') or f.endswith('.PDF')]
    extraction_pdfs = {}

    for file in pdfs_list:
        pages_df = []
        # file reader
        doc = fitz.open(f'{path}/{file}')
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            pages_df.append(page.get_text('text'))
        extraction_pdfs[file] = pages_df

    return extraction_pdfs
