from langchain.document_loaders import TextLoader, PyPDFLoader, Docx2txtLoader, UnstructuredHTMLLoader
from werkzeug.utils import secure_filename
import os


def load_files(files):
    if files is None or len(files) == 0:
        return None
    
    working_directory = os.getcwd()
    upload_directory = os.path.join(working_directory, 'uploads')

    if not os.path.exists(upload_directory):
        os.makedirs(upload_directory)

    documents = []

    for file in files:
        if file is None or file.filename == '':
            continue

        filename = secure_filename(file.filename)
        filepath = os.path.join(upload_directory, filename)
        file.save(filepath)

        loader = None

        if filepath.endswith('.txt'):
            loader = TextLoader(filepath, encoding = 'UTF-8')
        elif filepath.endswith('.pdf'):
            loader = PyPDFLoader(filepath)
        elif filepath.endswith('.docx') or filepath.endswith('.doc'):
            loader = Docx2txtLoader(filepath)
        elif filepath.endswith('.html') or filepath.endswith('.htm') or filepath.endswith('.mhtml'):
            loader = UnstructuredHTMLLoader(filepath)

        if loader:
            document = loader.load()
            documents.extend(document)

    return documents
