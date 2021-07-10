import os
from text_extractor import Extractor

INPUT_DIRECTORY = f"/home/{os.environ['USER']}/projects/internship-seeker/data"
OUTPUT_DIRECTORY = f"/home/{os.environ['USER']}/projects/internship-seeker/data/resultpdf"
PREPROCESS = True

if __name__ == '__main__':
    extractor = Extractor(INPUT_DIRECTORY, OUTPUT_DIRECTORY, PREPROCESS)
    extractor.apply_ocr()