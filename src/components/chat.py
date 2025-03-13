import streamlit as st
from utils.llm_interface import query_llm
import pandas as pd
from langchain.memory import ConversationBufferMemory

def initialize_memory():
    """Initialize a conversation memory object"""
    return ConversationBufferMemory()

class ChatComponent:
    def __init__(self):
        # Initialize session state for messages if it doesn't exist
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        # Initialize memory if it doesn't exist
        if "memory" not in st.session_state:
            st.session_state.memory = initialize_memory()

    def send_message(self, user_input, csv_data=None):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Show loading spinner while waiting for response
        with st.spinner("Thinking..."):
            # Prepare CSV context if data is available
            csv_context = None
            if csv_data is not None and isinstance(csv_data, pd.DataFrame):
                # Get basic statistics and sample of the CSV
                csv_context = f"CSV Summary: {len(csv_data)} rows, {len(csv_data.columns)} columns\n"
                csv_context += f"Columns: {', '.join(csv_data.columns.tolist())}\n"
                csv_context += f"Sample data:\n{csv_data.head(5).to_string()}\n"
            
            # Query LLM with user input, CSV context, and memory
            response = query_llm(user_input, csv_context, st.session_state.memory)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        return response

    def display_messages(self):
        # Display all messages in the chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
    def clear_chat_history(self):
        st.session_state.messages = []
        # Reset memory when clearing chat
        st.session_state.memory = initialize_memory()