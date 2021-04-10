import docx

class Document:
    def __init__(self, file_path):
        try:
            self._doc = docx.Document(file_path)
        except Exception:
            print("Document couldn't be found...")

        self._paras = []
        self._words = []

    @property
    def doc(self):
        return self._doc

    @property
    def paras(self):
        return self._paras

    @paras.setter
    def paras(self, value):
        self._paras = value
