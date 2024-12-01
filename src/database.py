from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings


# Create a vector store (database) using Chroma
def save_to_chroma(documents, databasename="chroma"):
    # Check if documents is None or empty
    if documents is None or len(documents) == 0:
        return

    # Use CharacterTextSplitter to split the large text into smaller chunks
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
    chunks = text_splitter.split_documents(documents)

    # Create embeddings using a Google Generative AI model
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    # Convert the document chunks to embedding
    vectordb = Chroma.from_documents(chunks, embedding=embeddings, persist_directory=databasename)

    # Save the vectordb locally with the name "chroma"
    vectordb.persist()
