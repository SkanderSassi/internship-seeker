from PIL import Image
import pytesseract
import sys
from pdf2image import convert_from_path
import os


class Extractor():
    def __init__(self, files_directory, output_directory) -> None:
        self.files_directory = files_directory
        self.output_directory = output_directory
        self.list_of_files = [file for file in os.listdir(f'{files_directory}') if file.endswith('pdf')]
    def __convert_page_to_image(self, page, output_name):
        page.save(output_name, 'JPEG')
    def __convert_pdf_to_image(self):
        for file in self.list_of_files:
            pass
            
        
        
        
        
        
        