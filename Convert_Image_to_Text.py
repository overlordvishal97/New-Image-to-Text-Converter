import sys

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    # Running in a PyInstaller bundle
    from preloader import load_app

    load_app()
else:
    # Running in a development environment
    import Convert_Image_to_Text

    Convert_Image_to_Text.main()

import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog, messagebox
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
import warnings
from docx import Document
from fpdf import FPDF

# Ignore the Warning
warnings.filterwarnings("ignore", category=Warning)

# Global variable for output format
output_format = 'docx'


# Function to process images in batches
def process_images():
    global output_format
    # Get the list of image files in the input directory
    image_files = [filename for filename in os.listdir(input_dir) if
                   filename.lower().endswith(('.png', '.jpg', '.jpeg'))]
    num_images = len(image_files)
    if num_images == 0:
        messagebox.showinfo("Error", "No image files found in the input directory.")
        return

    # Initialize progress bar
    progress_bar.config(maximum=num_images, value=0)
    progress_label.config(text="Processing...")

    batch_size = 5  # Adjust the batch size as needed
    num_batches = (num_images + batch_size - 1) // batch_size  # Calculate the number of batches

    # Process images in batches
    for batch_index in range(num_batches):
        start_index = batch_index * batch_size
        end_index = min((batch_index + 1) * batch_size, num_images)
        batch_files = image_files[start_index:end_index]

        # Process each image in the batch
        for i, filename in enumerate(batch_files, start=start_index + 1):
            img_path = os.path.join(input_dir, filename)
            img = Image.open(img_path)

            # Pre-processing the image
            img = img.convert('L')  # Convert to grayscale
            img = img.filter(ImageFilter.MedianFilter())  # Apply a median filter
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(2)  # Increase contrast

            text = pytesseract.image_to_string(img)

            # Choose output format
            if output_format.lower() == 'docx':
                doc_path = os.path.join(output_dir, filename[:-4] + '.docx')
                doc = Document()
                doc.styles['Normal'].font.name = 'Times New Roman'
                doc.styles['Normal'].font.size = 12
                doc.add_paragraph(text)
                doc.save(doc_path)
            elif output_format.lower() == 'txt':
                txt_path = os.path.join(output_dir, filename[:-4] + '.txt')
                with open(txt_path, 'w') as f:
                    f.write(text)
            elif output_format.lower() == 'pdf':
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                pdf.multi_cell(0, 10, text)
                pdf_path = os.path.join(output_dir, filename[:-4] + '.pdf')
                pdf.output(pdf_path)

            # Update progress bar
            progress_bar.step()
            progress_label.config(text=f"Processing... {i}/{num_images}")
            root.update_idletasks()  # Update the GUI

    # Completion message
    progress_label.config(text="Processing complete.")
    messagebox.showinfo("Completion", "All image files have been processed.")


# Function to select input directory
def select_input_dir():
    global input_dir
    input_dir = filedialog.askdirectory(title='Select Input Directory')


# Function to select output directory
def select_output_dir():
    global output_dir
    output_dir = filedialog.askdirectory(title='Select Output Directory')


# Function to select output format
def select_output_format():
    global output_format
    output_format = output_options.get()


# GUI for user input
root = tk.Tk()
root.title("Image to Text Converter")

# Frame for input and output selection
input_frame = tk.Frame(root)
input_frame.grid(row=0, column=0, padx=10, pady=10, sticky='w')
tk.Label(input_frame, text="Select Directories:").pack(fill='x', padx=5, pady=5)
input_button = tk.Button(input_frame, text="Select Input Directory", command=select_input_dir)
input_button.pack(fill='x', padx=5, pady=5)
output_button = tk.Button(input_frame, text="Select Output Directory", command=select_output_dir)
output_button.pack(fill='x', padx=5, pady=5)

# Output format selection
output_options = ttk.Combobox(input_frame, values=['docx', 'txt', 'pdf'])
output_options.set('docx')
output_options.pack(fill='x', padx=5, pady=5)
output_options.bind('<<ComboboxSelected>>', lambda event=None: select_output_format())

# Progress bar and label
progress_frame = tk.Frame(root)
progress_frame.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')
tk.Label(progress_frame, text="Progress:", font=('', 12, 'bold')).pack(padx=5, pady=5)
progress_label = tk.Label(progress_frame, text="", width=30, anchor='w', font=('', 10))
progress_label.pack(padx=5, pady=5)
progress_bar = ttk.Progressbar(progress_frame, orient='horizontal', length=300, mode='determinate')
progress_bar.pack(padx=5, pady=5)

# Frame for start button
start_frame = tk.Frame(root)
start_frame.grid(row=1, column=0, padx=10, pady=10, columnspan=2)
start_button = tk.Button(start_frame, text="Start", command=process_images)
start_button.pack(fill='x', padx=5, pady=5)

root.mainloop()
