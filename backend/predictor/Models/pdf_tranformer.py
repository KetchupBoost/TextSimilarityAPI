try:
    from PIL import Image
except ImportError:
    import Image
import cv2
import pytesseract
import os
import numpy as np
import pandas as pd
import re

from glob import glob as gb
from pdf2image import convert_from_bytes

'''
    Return a average confidence value of OCR result 
'''


def get_conf(page_gray):
    df = pytesseract.image_to_data(page_gray, output_type='data.frame')
    df.drop(df[df.conf == -1].index.values, inplace=True)
    df.reset_index()

    return df.conf.mean()


'''
    Taking a list of texts and combining them into one large chunk of text.
'''


def combine_texts(list_of_text):
    combined_text = ' '.join(list_of_text)
    return combined_text


'''
Main part of OCR:
pages_df: save eextracted text for each pdf file, index by page
OCR_dic : dict for saving df of each pdf, filename is the key
'''


def main(PATH):
    OCR_dic = {}

    for file in PATH:
        # convert pdf into image
        pdf_file = convert_from_bytes(open(os.path.join(PATH, file), 'rb').read())
        # create a df to save each pdf's text
        pages_df = pd.DataFrame(columns=['conf', 'text'])
        for (i, page) in enumerate(pdf_file):
            try:
                # transfer image of pdf_file into array
                page_arr = np.asarray(page)
                # transfer into grayscale
                page_arr_gray = cv2.cvtColor(page_arr, cv2.COLOR_BGR2GRAY)
                page_arr_gray = cv2.fastNlMeansDenoising(page_arr_gray, None, 3, 7, 21)
                # cal confidence value
                page_conf = get_conf(page_arr_gray)
                # extract string
                d = pytesseract.image_to_data(page_arr_gray, output_type=pytesseract.Output.DICT)
                d_df = pd.DataFrame.from_dict(d)
                # get block number
                block_num = int(d_df.loc[d_df['level'] == 2, ['block_num']].max())
                # drop header and footer by index
                head_index = d_df[d_df['block_num'] == 1].index.values
                foot_index = d_df[d_df['block_num'] == block_num].index.values
                d_df.drop(head_index, inplace=True)
                d_df.drop(foot_index, inplace=True)
                # combine text in dataframe
                text = combine_texts(d_df.loc[d_df['level'] == 5, 'text'].values)
                pages_df = pages_df.append({'conf': page_conf, 'text': text}, ignore_index=True)
            except Exception as e:
                # if can't extract then give some notes into df
                if hasattr(e, 'message'):
                    pages_df = pages_df.append({'conf': -1, 'text': e.message}, ignore_index=True)
                else:
                    pages_df = pages_df.append({'conf': -1, 'text': e}, ignore_index=True)
                continue
        # save df into a dict with filename as key
        OCR_dic[file] = pages_df
        print('{} is done'.format(file))


main(gb("./drive/MyDrive/NLP/PDFs/Cíveis - Classificada/*.pdf"))