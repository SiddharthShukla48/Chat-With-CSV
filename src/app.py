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
    page_title="CSV Chat & Visualizer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/yourusername/Chat-With-CSV',
        'Report a bug': 'https://github.com/yourusername/Chat-With-CSV/issues',
        'About': "# CSV Chat & Visualizer\nInteract with your CSV data using natural language."
    }
)

# Add custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #4CAF50;
        text-align: center;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px #cccccc;
    }
    .subheader {
        font-size: 1.5rem;
        color: #2E86C1;
        margin-bottom: 0.5rem;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 10px;
        display: flex;
    }
    .chat-message.user {
        background-color: #E8F5E9;
    }
    .chat-message.bot {
        background-color: #E3F2FD;
    }
    .visualization-container {
        background-color: #F5F5F5;
        padding: 1.5rem;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.markdown('<h1 class="main-header">CSV Chat & Visualizer</h1>', unsafe_allow_html=True)
    
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
        st.header("Model Settings")
        model_options = [
            "llama3-8b-8192",
            "llama3-70b-8192",
            "mixtral-8x7b-32768",
            "gemma-7b-it"
        ]
        selected_model = st.selectbox(
            "Select LLM Model", 
            model_options, 
            index=model_options.index(os.getenv("LLM_MODEL", "llama3-8b-8192"))
        )
        
        # Update environment variable with selected model
        os.environ["LLM_MODEL"] = selected_model
        
        st.header("Model Information")
        st.info(f"Using: {os.getenv('LLM_MODEL', 'llama3-8b-8192')}")
        
        # Add debug mode checkbox
        st.header("History")
        debug_mode = st.checkbox("Enable History", 
                                value=os.getenv("DEBUG_MODE", "False").lower() == "true")
        
        if debug_mode:
            os.environ["DEBUG_MODE"] = "True"
        else:
            os.environ["DEBUG_MODE"] = "False"
        
        # Display memory content when in debug mode
        if debug_mode and "memory" in st.session_state:
            st.sidebar.write("Memory content:", st.session_state.memory.load_memory_variables({}))
    
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