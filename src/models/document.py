import docx


class Document:
    ''' Represents a document with tables, paragraphs, and words '''

    def __init__(self, file_path):
        self.doc = None

        try:
            self.doc = docx.Document(file_path)
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}.\nPlease ensure the following:\n\t1. The file path is correct.\n\t2. The file path is not contained within speech or quotation marks.\n\t3. The file is not open in another program.")
            return

        self.tables = []
        self.paras = []
        self.words = []
