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
    # wb overwrite
    # xb write if not exists
    with open(output_filename, "wb") as out:
        pdf_writer.write(out)
        print("created", output_filename)


def get_append_name() -> str:
    """Get name-related values for output files."""

    # multiple file processing
    default_append_name = "-updated"
    append_name = input(f"Choose value to append to file names.\nThe default value is '{default_append_name}'.\n")
    append_name = append_name or default_append_name

    return append_name


def get_output_filename(file_path: str, source: str) -> str:
    """Get name-related values for output files."""

    last_forward_slash = file_path.rfind("/")
    last_period = file_path.rfind(".")
    default_output_filename = f"{source[last_forward_slash + 1: last_period]}-updated"
    output_filename = None

    output_filename = input(f"Please input a file name. Do not include the PDF extension.\nDefault value: {default_output_filename}\n")
    output_filename = output_filename or default_output_filename

    return output_filename


def main() -> None:
    """Reorders a PDF for right-to-left reading on two-page view."""

    sources = fd.askopenfilenames(
        title="Choose at least one file",
        initialdir=".",
        filetypes=(
        ("pdf files", "*.pdf"),
    ))

    if not sources:
        raise Exception("There are no PDFs to reorder.")

    len_of_sources = len(sources)

    file_path = sources[0]
    destination = fd.askdirectory(
        initialdir=file_path,
        title="Choose a destination directory for the files"
    )

    # TODO: this "if" check seems a bit redundant because it is repeated later. But assigning append_name in the for-loop would make for a repetitive UX. And ommitting the "if" flow while still assigning append_name would be confusing in the case of just one PDF, as the app will later request a name that will not take append_name into account.
    if len_of_sources > 1:
        append_name = get_append_name()

    for source in sources:
        last_forward_slash = source.rfind("/")
        last_period = source.rfind(".")
        source_name = source[last_forward_slash + 1: last_period]

        if len_of_sources > 1:
            output_filename = f"{destination}/{source_name}{append_name}.pdf"
        else: 
            output_filename = get_output_filename()
            output_filename = f"{destination}/{output_filename}.pdf"

        process_reorder(source, output_filename)


main()
