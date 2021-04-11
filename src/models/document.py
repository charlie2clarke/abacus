import docx

class Document:
    def __init__(self, file_path):
        try:
            self.doc = docx.Document(file_path)
        except Exception:
            print("Document couldn't be found...")

        self.tables = []
        self.paras = []
        self.words = []
