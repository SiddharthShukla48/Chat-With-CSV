from langchain_groq import ChatGroq
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
import os

def initialize_memory():
    """Initialize a conversation memory object"""
    return ConversationBufferMemory()

def query_llm(user_input, csv_context=None, memory=None):
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
        input_text = f"Based on the following CSV data:\n{csv_context}\n\nUser question: {user_input}"
    else:
        input_text = user_input
    
    # If memory is provided, use conversational chain
    if memory is not None:
        try:
            # Create conversation with memory
            conversation = ConversationChain(
                llm=llm,
                memory=memory,
                verbose=os.getenv("DEBUG_MODE", "False").lower() == "true"
            )
            response = conversation.predict(input=input_text)
        except Exception as e:
            print(f"Error using conversation chain: {str(e)}")
            # Fallback to direct invocation
            response = llm.invoke(input_text).content
    else:
        # Default behavior without memory
        response = llm.invoke(input_text).content
    
    return response