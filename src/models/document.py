import docx

class Document:
    ''' Represents a document with tables, paragraphs, and words '''

    def __init__(self, file_path):
        try:
            self.doc = docx.Document(file_path)
        except Exception as e:
            raise FileNotFoundError(f"Document couldn't be found at {file_path}") from e

        self.tables = []
        self.paras = []
        self.words = []
