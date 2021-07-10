import re
import shutil
import os
from nltk.tokenize import word_tokenize
import pytesseract as tess
import logging
from PIL import Image
from pdf2image import convert_from_path
from nltk.corpus import stopwords
from textblob import TextBlob
# Download steps required for nltk


logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)

LANG_MAP = {"ar": ["ar","arabic"], "en": ["eng", "english"], "fr": ["fra", "french"]}


class Extractor:
 
    
    def __init__(
        self,
        files_directory: str,
        output_directory: str,
        preprocess: bool,
    ) -> None:
        self.preprocess = preprocess
        self.files_directory = files_directory
        self.output_directory = output_directory
        self.files_list = [
            file for file in os.listdir(f"{files_directory}") if file.endswith(".pdf")
        ]

    def __convert_page_to_image(
        self, page, directory_path: str, file_basename: str, image_id: int
    ) -> None:
        page.save(f"{directory_path}/{file_basename}_page_{image_id}", "JPEG")
    
    def __get_language_name(self, text : str) -> str:
        blob = TextBlob(text)
        logging.info(f"Detected language {blob.detect_language()}")
        return blob.detect_language()
        
        
    def __extract_text_from_image(self, image_path: str) -> str:
        img = Image.open(image_path)
        text = tess.image_to_string(img)
        text.replace("-\n", "")
        return text

    
    def __preprocess_text(self, text: str, language : str) -> str:
        stop_words = set(stopwords.words(language))
        tokens = word_tokenize(text)
        preprocessed_text = " ".join(
            [word.lower() for word in tokens if word not in stop_words]
        )
        preprocessed_text = re.sub(r'\W+|\d+',' ',preprocessed_text)
        preprocessed_text = re.sub(r'\s{2,}', ' ',preprocessed_text)
        
        return preprocessed_text

    def __convert_pdf_to_images(self, file_basename: str) -> str:
        logging.info(f"Converting file : {file_basename}.pdf")
        temporary_dir_path = f"{self.output_directory}/{file_basename}_temp"
        try:
            pages_list = convert_from_path(
                f"{self.files_directory}/{file_basename}.pdf"
            )
            os.mkdir(temporary_dir_path)
            for image_id in range(len(pages_list)):
                self.__convert_page_to_image(
                    pages_list[image_id], temporary_dir_path, file_basename, image_id
                )
            logging.info(f"File {file_basename}.pdf converted")
        except FileExistsError:
            print("File already exists")

        return temporary_dir_path


    def __clean_up(self, dir_path) -> None:
        logging.info(f"Cleaning files")
        try:
            shutil.rmtree(dir_path)
        except FileNotFoundError:
            print(f"Directory not found at {dir_path}")

    def __dump_text(self, text: str, file_path: str, mode: str) -> None:
        with open(file_path, mode) as file:
            logging.info(f"Dumping text")
            file.write(text)

    def apply_ocr(self) -> None:
        if (not os.path.isdir(self.output_directory)):
            os.mkdir(self.output_directory)
            
        if len(self.files_list) > 0:
            for file_name in self.files_list:
                try:
                    file_basename = re.sub("\.pdf", "", file_name)
                    output_path = os.path.join(self.output_directory, file_basename + ".txt")
                    logging.info(f"Handling {file_name}")
                    temporary_dir_path = self.__convert_pdf_to_images(file_basename)

                    extracted_text = []
                    logging.info("Applying OCR")
                    for image_file_name in os.listdir(temporary_dir_path):
                        extracted_text.append(
                            self.__extract_text_from_image(
                                os.path.join(temporary_dir_path, image_file_name),
                            )
                        )
                        
                    sample_text = extracted_text[0]
                    lang = self.__get_language_name(sample_text) #Detect language based on a sample
                    extracted_text = ' '.join(extracted_text)
                    lang = LANG_MAP[lang][1]  #map detected abbreviation to its corresponding string

                    if self.preprocess:
                        logging.info("Preprocessing text")
                        extracted_text = self.__preprocess_text(extracted_text, lang)     
                    self.__dump_text(extracted_text, output_path, "w+")
                finally:
                    self.__clean_up(temporary_dir_path)
        else:
            logging.info('No files to work on')    
            