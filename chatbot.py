import os
import dotenv
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain import PromptTemplate

def get_answer(question):
    # Load environment variables from the .env file
    dotenv.load_dotenv()

    # Load the OpenAI API key from environment variable
    openai_api_key = os.getenv("OPENAI_API_KEY")

    # Check if the OpenAI API key is present
    if openai_api_key is None:
        # If not present, raise an error
        raise ValueError("An OpenAI API key has not been provided")

    # Create an instance of ChatOpenAI using the OpenAI API key
    chat_lm = ChatOpenAI(
        openai_api_key=openai_api_key,
        temperature=0,
        model_name="gpt-3.5-turbo",
        max_tokens=300
    )

    # Create a question answering retrieval model
    retriever = FAISS.load_local("db_docs", OpenAIEmbeddings()).as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3}
    )

    # Create an instance of RetrievalQA
    retrieval_qa = RetrievalQA.from_chain_type(
        llm=chat_lm,
        chain_type="stuff",
        retriever=retriever
    )

    # Define the question template
    template = """
    Eres un asistente virtual especializado en esclerosis múltiple, puedes responder esto: {query}?
    """

    # Create an instance of PromptTemplate
    prompt = PromptTemplate(
        input_variables=["query"],
        template=template
    )

    # Run the chatbot with the provided question
    response = retrieval_qa.run(
        prompt.format(query=question)
    )

    # Return the response
    return response