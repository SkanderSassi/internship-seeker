from PIL import Image
import pytesseract
import sys
import logging
from pdf2image import convert_from_path
import re
import shutil
import os

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)

class Extractor():
    def __init__(self, files_directory, output_directory) -> None:
        self.files_directory = files_directory
        self.output_directory = output_directory
        self.files_list = [file for file in os.listdir(f'{files_directory}') if file.endswith('pdf')]
        
    def __convert_page_to_image(self, page, directory_path, file_basename, image_id):
        page.save(f'{directory_path}/{file_basename}_page_{image_id}', 'JPEG')
        
    def convert_pdf_to_image(self):
        
        for file in self.files_list:
            logging.info(f'Converting file : {file}')
            pages_list = convert_from_path(f'{self.files_directory}/{file}')
            file_basename = re.sub('\.pdf','',file)
            temporary_dir_path = f"{self.output_directory}/{file_basename}_temp"
            os.mkdir(temporary_dir_path)
            for image_id in range(len(pages_list)):
                self.__convert_page_to_image(pages_list[image_id], temporary_dir_path, file_basename, image_id)
            logging.info(f'File {file} converted')
            self.__clean_up(file_basename)
            
    def __clean_up(self, file_basename):
        logging.info(f"Cleaning temporary files : {file_basename}")
        temporary_dir_path = f"{self.output_directory}/{file_basename}_temp"
        shutil.rmtree(temporary_dir_path)
        
        

        
        
        
        
        
        