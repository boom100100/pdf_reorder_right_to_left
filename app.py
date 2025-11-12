#!/usr/bin/python3
"""Reorder PDF pages for right-to-left reading.

Use case: a manga PDF on two-page view shows the pages on the wrong side.

The fix here is to move the even page behind the following odd page.
"""
from pathlib import Path
from typing import Optional

from PyPDF2 import PdfReader, PdfWriter
from tkinter import filedialog as fd


def file_exists_can_be_overwritten(
    output_filename: str, never_overwrite: Optional[bool]
) -> tuple[bool, str]:
    """Checks if the file exists and prompts the user to allow overwriting."""

    if not Path(output_filename).exists():
        return False, "Y"

    file_exists = True

    if never_overwrite:
        return file_exists, "X"
    
    overwrite = input(
        f"This file exists already:\n{output_filename}\nAllow overwrite?\nNo (default) (N)\nYes (Y)\nOverwrite all (A)\nNever overwrite (X)\n"
    ) or "N"

    if overwrite.upper() == "Y":
        return file_exists, "Y"

    if overwrite.upper() == "N":
        return file_exists, "N"

    if overwrite.upper() == "A":
        return file_exists, "A"

    if overwrite.upper() == "X":
        return file_exists, "X"

    return file_exists, "N" # Won't overwrite for some unexpected response. Could do "while overwrite not in acceptable_responses"  instead, but will leave as-is.


def process_reorder(source: str, output_filename: str) -> None:
    """Reorders the pages."""

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

    with open(output_filename, "wb") as out:
        pdf_writer.write(out)
        print(f"Created file:\n{output_filename}\n")


def get_append_name() -> str:
    """Prompts for a value to append to the original file name for multiple file processing."""

    default_append_name = "-updated"
    append_name = input(f"Choose value to append to file names.\nThe default value is '{default_append_name}'. ")
    append_name = append_name or default_append_name

    return append_name


def get_output_filename(source: str) -> str:
    """Prompts for an output file name."""

    last_forward_slash = source.rfind("/")
    last_period = source.rfind(".")
    default_output_filename = f"{source[last_forward_slash + 1: last_period]}-updated"
    output_filename = None

    output_filename = input(f"Please input a file name. Do not include the PDF extension.\nDefault value: {default_output_filename} ")
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

    # Gonna leave this "if" check as is. It seems a bit redundant because it is repeated later. But assigning append_name in the for-loop would make for a repetitive UX. Ommitting the "if" flow and always assigning append_name would be confusing in the case of just one PDF, as the app will later request a name that will not take append_name into account.
    if len_of_sources > 1:
        append_name = get_append_name()

    always_overwrite = None
    never_overwrite = None
    for source in sources:
        last_forward_slash = source.rfind("/")
        last_period = source.rfind(".")
        source_name = source[last_forward_slash + 1: last_period]

        if len_of_sources > 1:
            output_filename = f"{destination}/{source_name}{append_name}.pdf"
        else: 
            output_filename = get_output_filename(source)
            output_filename = f"{destination}/{output_filename}.pdf"

        if always_overwrite:
            process_reorder(source, output_filename)
            continue

        file_exists, can_overwrite = file_exists_can_be_overwritten(output_filename, never_overwrite)

        if not file_exists:
            process_reorder(source, output_filename)
            continue

        if file_exists and (never_overwrite or can_overwrite == "N"):
            print(f"Skipping file:\n{output_filename}\n")
            continue

        if file_exists and can_overwrite == "X":
            never_overwrite = True
            print(f"Skipping file:\n{output_filename}\n")
            continue

        if file_exists and can_overwrite == "Y":
            process_reorder(source, output_filename)
            continue

        if file_exists and can_overwrite == "A":
            always_overwrite = True
            process_reorder(source, output_filename)
            continue


main()
