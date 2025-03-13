from langchain_groq import ChatGroq
import os

def query_llm(user_input, csv_context=None):
    # Get API key from environment
    api_key = os.getenv("GROQ_API_KEY")
    model_name = os.getenv("LLM_MODEL", "llama3-8b-8192")
    
    # Initialize the language model
    llm = ChatGroq(
        api_key=api_key,
        model_name=model_name
    )
    
    # Prepare prompt with CSV context if available
    if csv_context:
        prompt = f"Based on the following CSV data:\n{csv_context}\n\nUser question: {user_input}"
    else:
        prompt = user_input
    
    # Query the language model
    response = llm.invoke(prompt)
    
    return response.content