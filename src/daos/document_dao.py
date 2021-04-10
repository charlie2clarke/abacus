import docx
from models.document import Document


class DocumentDao:
    def __init__(self, file_path):
        self.document = Document(file_path)

        self.initialise_document()

    def initialise_document(self):
        self.document.paras = list(self.set_paragraphs())
        self.document.words = list(self.set_words())

    def set_paragraphs(self):
        counter = 0

        while self.document.doc.paragraphs[counter].text != 'Appendices':
            paragraph = self.document.doc.paragraphs[counter]
            counter += 1

            if not paragraph.style.name.startswith('Heading') and paragraph.text != '':
                yield paragraph

    def set_words(self):
        for paragraph in self.document.paras:
            paragraph = paragraph.text
            words = paragraph.split()
            for word in words:
                if word != '.':
                    yield word

    def print_word_count(self):
        print(len(self.document.words))
