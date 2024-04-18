# New-Image-to-Text-Converter
This is a simple application that converts images to text documents. It allows users to select an input directory containing image files and choose an output format (such as DOCX, TXT, or PDF) for the converted text documents.

# Installation
Prerequisites
Python 3.x
Tkinter
PIL (Python Imaging Library)
pytesseract
docx
fpdf

# Installation Steps
Clone or download this repository to your local machine.
Install the required Python packages using pip:
pip install -r requirements.txt

# Usage
Run the Convert_Image_to_Text.py script.
Select the input directory containing the image files you want to convert.
Choose the output directory where you want to save the converted text documents.
Select the desired output format (DOCX, TXT, or PDF).
Click the "Start" button to begin the conversion process.
Once the conversion is complete, a completion message will be displayed, and the converted text documents will be saved in the specified output directory.

# Additional Notes
The application processes images in batches to improve performance.
Pre-processing techniques such as converting to grayscale, applying filters, and enhancing contrast are applied to the images before text extraction.
Text extraction from images is performed using the Tesseract OCR engine (via the pytesseract library).
Converted text documents are saved in the specified output format (DOCX, TXT, or PDF) with appropriate file extensions.

# License
This project is licensed under the MIT License.

# preloader.py

import importlib
import sys

def load_app():
    # Replace 'main' with the name of your main script
    module = importlib.import_module('Convert_Image_to_Text')
    module.main()

if __name__ == '__main__':
    load_app()

Feel free to customize and modify the code according to your requirements. If you have any questions or need further assistance, please don't hesitate to contact me.






