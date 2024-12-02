from langchain.chains import ConversationalRetrievalChain
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

# Chat to private data saved in FAISS vector database
def chat(question, history, databasename="faiss"):
    # Check values of the passed parameters
    if question is None or question == '':
        return "error: please provide a question", history

    # Create embeddings using a Google Generative AI model
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    # Load a FAISS vector database from a local file
    vectordb = FAISS.load_local(databasename, embeddings, allow_dangerous_deserialization=True)

    # Create a question-answering chain with the specified model and vector database
    chain = ConversationalRetrievalChain.from_llm(
        llm = ChatGoogleGenerativeAI(model="gemini-pro", convert_system_message_to_human=True, temperature=0.3),
        retriever = vectordb.as_retriever(search_kwargs={'k': 6}),
        # memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True),
    )

    # Pass question and chat history to call the question/answer chain to get response
    response = chain.invoke({"question": question, "chat_history": history})

    # Get response/answer and also replace new line character "\n" by line break tag "<br>" in html
    answer = response["answer"].replace("\n", "<br>")

    # Update the chat history
    history.append((question, answer))

    return answer, history
