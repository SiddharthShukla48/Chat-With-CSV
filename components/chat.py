import streamlit as st
from utils.llm_interface import query_llm
import pandas as pd

class ChatComponent:
    def __init__(self):
        # Initialize session state for messages if it doesn't exist
        if "messages" not in st.session_state:
            st.session_state.messages = []

    def send_message(self, user_input, csv_data=None):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Prepare CSV context if data is available
        csv_context = None
        if csv_data is not None and isinstance(csv_data, pd.DataFrame):
            # Get basic statistics and sample of the CSV
            csv_context = f"CSV Summary: {len(csv_data)} rows, {len(csv_data.columns)} columns\n"
            csv_context += f"Columns: {', '.join(csv_data.columns.tolist())}\n"
            csv_context += f"Sample data:\n{csv_data.head(5).to_string()}\n"
        
        # Query LLM with user input and CSV context
        response = query_llm(user_input, csv_context)
        
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