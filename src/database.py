from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings


# Create a vector store (database) using FAISS
def save_to_database(documents, databasename="faiss"):
    # Check if documents is None or empty
    if documents is None or len(documents) == 0:
        return

    # Append all documents to form a large text string.
    text = " "
    for document in documents:
        text += document.page_content

    # Remove all problematic characters.
    text= text.replace('»', '').replace('\'','').replace('/','').replace(':','-').replace('(','').replace(')','').replace("*",'')
    text= text.encode('ascii', errors='ignore').decode()

    # Use RecursiveCharacterTextSplitter splits the large text into specified chunk size.
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)

    # Create embeddings using a Google Generative AI model
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    # Create a vector store using FAISS from the provided text chunks and embeddings
    vectordb = FAISS.from_texts(chunks, embedding=embeddings)

    # Save the vectordb locally with the name "faiss"
    vectordb.save_local(databasename)
