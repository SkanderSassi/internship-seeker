import os
from text_extractor import Extractor

INPUT_DIRECTORY = f"/home/{os.environ['USER']}/projects/internship-seeker/pdfs/"
OUTPUT_DIRECTORY = f"/home/{os.environ['USER']}/projects/internship-seeker/pdfs/resultpdf"
LANGUAGE = "fra"
PREPROCESS = True

if __name__ == '__main__':
    extractor = Extractor(INPUT_DIRECTORY, OUTPUT_DIRECTORY, PREPROCESS)
    extractor.apply_ocr()