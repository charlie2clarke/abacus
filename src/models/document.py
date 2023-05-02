import docx
from docx.opc.exceptions import PackageNotFoundError


class Document:
    ''' Represents a document with tables, paragraphs, and words '''

    def __init__(self, file_path):
        self.doc = None

        try:
            self.doc = docx.Document(file_path)
        except PackageNotFoundError:
            print("Package not found. Please ensure the file is closed in other programs and has a valid '.docx' format.")
            return 

        self.tables = []
        self.paras = []
        self.words = []
