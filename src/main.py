from daos.document_dao import DocumentDao


if __name__ == '__main__':
    print('Running main.py') #debugging
    file_path = input('File path to document: ')
    print('')
    document_dao = DocumentDao(file_path)
    document_dao.print_word_count()