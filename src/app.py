#!/usr/bin/env python3

from flask import Flask, request, render_template
from datacollector import load_files
from database import save_to_database
from dataanalyzer import chat

app = Flask(__name__)

chat_history = []


@app.route("/")
def main():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload():
    global chat_history

    files = request.files.getlist("documents")
    documents = load_files(files)

    # Message for successfully uploading documents
    filenames = []
    for file in files:
        if file != None and file.filename != '':
            filenames.append(file.filename)

    count = len(files)
    is_are = "s are" if (count > 1) else " is"
    message = "The following file" + is_are + " successfully uploaded: " + ", ".join(filenames) + "."

    # Save documents to vector database
    if documents and len(documents) > 0:
        # Create a vector store (database) using Chroma
        save_to_database(documents, "chroma")

        message += "<br>File" + is_are + " also saved to database."

    # Test the chat_with_chroma() function
    # answer, chat_history = chat("who is openai", chat_history, "chroma")

    return message

if __name__ == '__main__':
   app.run()