#!/usr/bin/python3
"""Reorder PDF pages for right-to-left reading.

Use case: a manga PDF on two-page view shows the pages on the wrong side.

The fix here is to move the even page behind the following odd page.
"""

from PyPDF2 import PdfReader, PdfWriter
from tkinter import filedialog as fd

def process_reorder(source, output_filename):
    pdf = PdfReader(source)
    pages = pdf.pages
    pdf_writer = PdfWriter()

    previous_page = None

    for page_number in range(len(pages)):
        current_page = pages[page_number]
        if page_number % 2 == 0: # modulo distinguishes even value, but for a PDF, page 0 is the odd-numbered page
            pdf_writer.add_page(current_page)
        elif previous_page is not None:
            pdf_writer.add_page(previous_page)
            previous_page = current_page # moves the even-numbered page to the right of the odd-numbered page.
        else:
            previous_page = current_page

    # Write the data to disk
    with open(output_filename, "wb") as out:
        pdf_writer.write(out)
        print("created", output_filename)

def get_names(file_path: str, len_of_sources: int, sources: list[str]) -> tuple[str, str]:
    """Get name-related values for output files."""

    # multiple file processing
    default_append_name = "-updated"
    append_name = None

    last_forward_slash = file_path.rfind("/")
    last_period = file_path.rfind(".")
    default_output_filename = f"{sources[0][last_forward_slash + 1: last_period]}-updated"
    output_filename = None

    if len_of_sources > 1:
        append_name = input(f"Choose value to append to file names.\nThe default value is '{default_append_name}'.\n")
        append_name = append_name or default_append_name
    else:
        output_filename = input(f"Please input a file name. Do not include the PDF extension.\nDefault value: {default_output_filename}\n")
        output_filename = output_filename or default_output_filename

    return append_name, output_filename

def set_up():
    sources = fd.askopenfilenames(
        title='Choose at least one file',
        initialdir='.',
        filetypes=(
        ('pdf files', '*.pdf'),
    ))
    len_of_sources = len(sources)

    file_path = sources[0]
    destination = fd.askdirectory(
        initialdir=file_path,
        title="Choose a destination directory for the files"
    )

    append_name, output_filename = get_names(file_path, len_of_sources, sources)
    
    for source in sources:
        last_forward_slash = source.rfind("/")
        last_period = source.rfind(".")
        source_name = source[last_forward_slash + 1: last_period]

        if len_of_sources > 1:
            output_filename = f"{destination}/{source_name}{append_name}.pdf"
        else: 
            output_filename = f"{destination}/{output_filename}.pdf"

        process_reorder(source, output_filename)

set_up()
