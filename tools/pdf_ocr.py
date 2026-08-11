'''
Convert a PDF into text by rendering each page to an image and running
tesseract OCR on it. The text of all pages is combined into one output file.

USAGE:
    python pdf_ocr.py [-d dpi] [-l lang] [-f first_page] [-t last_page]
                      [-i image_dir] input.pdf output.txt
'''

import getopt
import logging
import os
import sys
import tempfile

import pymupdf
import pytesseract
from PIL import Image

PAGE_SEP = '\n\n--- Page %d ---\n\n'

class PdfOcr:
    def __init__(self, dpi = 300, lang = 'eng', imagedir = None):
        self.dpi      = dpi
        self.lang     = lang
        self.imagedir = imagedir
        self.logger   = logging.getLogger('pdf_ocr')

    def page_to_image(self, page, pagenum, outdir):
        zoom   = self.dpi / 72.0
        pixmap = page.get_pixmap(matrix = pymupdf.Matrix(zoom, zoom))

        imgpath = os.path.join(outdir, 'page-%04d.png' % pagenum)
        pixmap.save(imgpath)
        return imgpath

    def image_to_text(self, imgpath):
        image = Image.open(imgpath)
        try:
            return pytesseract.image_to_string(image, lang = self.lang)
        finally:
            image.close()

    def to_text(self, infile, first = 1, last = None):
        doc = pymupdf.open(infile)
        try:
            numpages = doc.page_count
            if last is None or last > numpages:
                last = numpages

            if self.imagedir:
                os.makedirs(self.imagedir, exist_ok = True)
                outdir  = self.imagedir
                tmpdir  = None
            else:
                tmpdir = tempfile.TemporaryDirectory()
                outdir = tmpdir.name

            try:
                texts = []
                for pagenum in range(first, last + 1):
                    self.logger.info('Processing page %d of %d', pagenum, last)

                    page    = doc.load_page(pagenum - 1)
                    imgpath = self.page_to_image(page, pagenum, outdir)
                    text    = self.image_to_text(imgpath)

                    texts.append(PAGE_SEP % pagenum)
                    texts.append(text)
            finally:
                if tmpdir:
                    tmpdir.cleanup()
        finally:
            doc.close()

        return ''.join(texts)

def print_usage():
    print(__doc__)

if __name__ == '__main__':
    optlist = getopt.getopt(sys.argv[1:], 'd:f:hi:l:t:')

    dpi      = 300
    lang     = 'eng'
    first    = 1
    last     = None
    imagedir = None

    for o, v in optlist[0]:
        if o == '-d':
            dpi = int(v)
        elif o == '-f':
            first = int(v)
        elif o == '-h':
            print_usage()
            sys.exit(0)
        elif o == '-i':
            imagedir = v
        elif o == '-l':
            lang = v
        elif o == '-t':
            last = int(v)

    if len(optlist[1]) != 2:
        print_usage()
        sys.exit(1)

    inputfile, outputfile = optlist[1]

    logging.basicConfig(level = logging.INFO, \
                        format = '%(asctime)s %(levelname)s %(message)s')

    ocr = PdfOcr(dpi = dpi, lang = lang, imagedir = imagedir)
    out = ocr.to_text(inputfile, first = first, last = last)

    with open(outputfile, 'w', encoding = 'utf-8') as f:
        f.write(out)
