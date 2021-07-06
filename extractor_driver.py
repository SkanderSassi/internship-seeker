import os
from text_extractor import Extractor

INPUT_DIRECTORY = f"/home/{os.environ['USER']}/projects/internship-seeker/pdfs/"
OUTPUT_DIRECTORY = f"/home/{os.environ['USER']}/projects/internship-seeker/pdfs/resultpdf"


if __name__ == '__main__':
    extractor = Extractor(INPUT_DIRECTORY, OUTPUT_DIRECTORY)
    extractor.convert_pdf_to_image()
