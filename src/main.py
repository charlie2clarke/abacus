import sys
from daos.document_dao import DocumentDao

if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = input('Enter file path to document without quotation marks: ')
    print('')
    document_dao = DocumentDao(file_path)
    if document_dao.document_loaded: 
        document_dao.print_word_count()
    print('')
