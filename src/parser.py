# src/parser.py

import os
import pdfplumber
from docx import Document


class ResumeParser:
    """
    Reads PDF, DOCX and TXT files and returns extracted text.
    """

    SUPPORTED_FORMATS = {
        ".pdf",
        ".docx",
        ".txt"
    }

    def read_pdf(self, file_path):

        text = []

        with pdfplumber.open(file_path) as pdf:

            for page in pdf.pages:

                page_text = page.extract_text()

                if page_text:
                    text.append(page_text)

        return "\n".join(text)

    def read_docx(self, file_path):

        document = Document(file_path)

        text = []

        for paragraph in document.paragraphs:

            if paragraph.text.strip():

                text.append(
                    paragraph.text
                )

        return "\n".join(text)

    def read_txt(self, file_path):

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            return file.read()

    def extract_text(self, file_path):

        extension = os.path.splitext(
            file_path
        )[1].lower()

        if extension not in self.SUPPORTED_FORMATS:

            raise ValueError(
                f"Unsupported file type: {extension}"
            )

        if extension == ".pdf":

            return self.read_pdf(file_path)

        elif extension == ".docx":

            return self.read_docx(file_path)

        elif extension == ".txt":

            return self.read_txt(file_path)

        raise ValueError(
            "Unsupported file."
        )