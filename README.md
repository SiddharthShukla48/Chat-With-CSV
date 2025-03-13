# langchain-csv-chat

This project is a Streamlit application that integrates a chat interface with CSV data visualization using Langchain for language model inferencing. Users can interact with the application to upload CSV files, visualize the data, and engage in a chat that leverages the insights from the CSV.

## Features

- **Chat Interface**: Communicate with the application using natural language. The chat component allows users to send messages and receive responses based on the uploaded CSV data.
- **CSV Visualization**: Upload CSV files and visualize the data in a user-friendly format. The CSV visualizer provides an intuitive way to explore the contents of the file.


## Installation

1. Clone the repository:
   ```
   git clone https://github.com/SiddharthSHukla48/langchain-csv-chat.git
   cd langchain-csv-chat
   ```

2. Create a new Python environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Create `.env` and fill in the necessary values.

## Usage

To run the application, execute the following command:
```
streamlit run src/app.py
```
