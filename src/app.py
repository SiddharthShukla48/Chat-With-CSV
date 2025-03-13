import streamlit as st
import pandas as pd
from components.chat import ChatComponent
from components.csv_visualizer import CsvVisualizer
from utils.csv_processor import process_csv
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure page
st.set_page_config(
    page_title="Chat with CSV - Powered by Groq",
    page_icon="📊",
    layout="wide"
)

def main():
    st.title("📊 Chat with CSV - Powered by Groq and LangChain")
    
    # Initialize components
    chat_component = ChatComponent()
    csv_visualizer = CsvVisualizer()
    
    # Sidebar for CSV upload and options
    with st.sidebar:
        st.header("Upload CSV")
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
        
        if uploaded_file is not None:
            # Load and process CSV
            try:
                df = process_csv(uploaded_file)
                csv_visualizer = CsvVisualizer(df)
                st.session_state.csv_data = df
                st.success(f"CSV loaded successfully! ({df.shape[0]} rows, {df.shape[1]} columns)")
            except Exception as e:
                st.error(f"Error processing CSV: {e}")
        
        # Add option to clear chat history
        if st.button("Clear Chat History"):
            chat_component.clear_chat_history()
            st.success("Chat history cleared!")
        
        # Show LLM info
        st.header("Model Information")
        st.info(f"Using: {os.getenv('LLM_MODEL', 'llama3-8b-8192')}")
    
    # Create two columns layout
    col1, col2 = st.columns([3, 2])
    
    with col1:
        # Chat interface
        st.header("Chat with your CSV")
        
        # Display chat messages
        chat_component.display_messages()
        
        # Input for new messages
        user_input = st.chat_input("Ask a question about your CSV data...")
        
        if user_input:
            # Get CSV data if available
            csv_data = st.session_state.get("csv_data", None)
            # Send message and get response
            chat_component.send_message(user_input, csv_data)
            # Force a rerun to update the UI with the new message
            st.rerun()
    
    with col2:
        # CSV visualization
        if "csv_data" in st.session_state:
            csv_visualizer = CsvVisualizer(st.session_state.csv_data)
            csv_visualizer.render_csv()
        else:
            st.info("Upload a CSV file to visualize it here.")

if __name__ == "__main__":
    main()