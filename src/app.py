#!/usr/bin/env python3

from flask import Flask, request, render_template
from datacollector import load_files
from database import save_to_chroma

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload():
    files = request.files.getlist("documents")
    documents = load_files(files)

    # Message for successfully uploading documents
    filenames = []
    for file in files:
        if file != None and file.filename != '':
            filenames.append(file.filename)

    message = "The following documents are successfully uploaded: " + ", ".join(filenames) + "."

    # Save documents to vector database
    if documents and len(documents) > 0:
        # Create a vector store (database) using Chroma
        save_to_chroma(documents, "chroma")

        message += " Files are also saved to database."

    return message

if __name__ == '__main__':
   app.run()