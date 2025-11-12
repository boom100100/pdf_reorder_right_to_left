#!/usr/bin/python3
"""Reorder PDF pages.

Use case: a manga PDF on two-page view shows the pages on the wrong side.

The fix here is to move the even page behind the odd page.
"""

from PyPDF2 import PdfReader, PdfWriter
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo

# create the root window
root = tk.Tk()



source = fd.askopenfilename(
    title='Open a file',
    initialdir='.',
    filetypes=(
    ('pdf files', '*.pdf'),
))
print(f"Source: {source}\n")

# Make this a file input dialog
source = "/Users/bernadette/Downloads/black jack ni yoroshiku/001bj.pdf"
pdf = PdfReader(source)
pages = pdf.pages

destination = fd.askdirectory(initialdir=source)
print(f"Destination:\n{destination}\n")

last_forward_slash = source.rfind("/")
last_period = source.rfind(".")
default_output_filename = f"{source[last_forward_slash + 1: last_period]}-updated"
output_filename = input(f"Please select a file name. Do not include the PDF extension.\nDefault value: {default_output_filename}")
print(f"Output filename:\n{output_filename=} Is empty?: {output_filename == ""}\n")
output_filename = output_filename or default_output_filename
print(f"Final output filename:\n{output_filename=}\n")
output_filename = f"{destination}/{output_filename}.pdf"
# Make this file output directory dialog and name input (or all-in-one, if possible).
output_filename = "/Users/bernadette/Downloads/black jack ni yoroshiku/001bj-updated.pdf"

pdf_writer = PdfWriter()
previous_page = None

# Get reach page and add it to corresponding
# output file based on page number
for page_number in range(len(pages)):
    current_page = pages[page_number]
    if page_number % 2 == 0: # modulo distinguishes even value, but for a PDF, page 0 is the odd-numbered page
        pdf_writer.add_page(current_page)
    elif previous_page is not None:
        pdf_writer.add_page(previous_page)
        previous_page = current_page
    else:
        previous_page = current_page

# Write the data to disk
with open(output_filename, "wb") as out:
     pdf_writer.write(out)
     print("created", output_filename)
