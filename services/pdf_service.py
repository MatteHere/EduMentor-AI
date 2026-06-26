import pdfplumber


def extract_text_from_pdf(file_path):
    """
    Extract text from all pages of a PDF.
    """

    extracted_text = ""

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()

            if text:
                extracted_text += text + "\n\n"

    return extracted_text.strip()