# PDF Reorderer
Rearranges PDF pages for right-to-left (RTL) reading.

## Features
- Rearrange pages for one or multiple PDFs at a time.
- Overwriting an existing PDF (or many) is optional.

## Setup
### MacOS
    cd projectDir
    brew install python@3.13
    brew install python-tk
    brew install pipenv

    pipenv shell
    pipenv install --python 3.13

# Run
In the pipenv shell, run `python app.py`.

# Demo

Before:

![Side-by-side PDF pages out of order for right-to-left reading.](<Screenshot 2025-11-12 at 2.20.47 PM.png>)

After:

![Side-by-side PDF pages in proper order for right-to-left reading.](<Screenshot 2025-11-12 at 2.17.43 PM.png>)
