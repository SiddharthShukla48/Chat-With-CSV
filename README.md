# langchain-csv-chat

This project is a Streamlit application that integrates a chat interface with CSV data visualization using Langchain for language model inferencing. Users can interact with the application to upload CSV files, visualize the data, and engage in a chat that leverages the insights from the CSV.

## Features

- **Chat Interface**: Communicate with the application using natural language. The chat component allows users to send messages and receive responses based on the uploaded CSV data.
- **CSV Visualization**: Upload CSV files and visualize the data in a user-friendly format. The CSV visualizer provides an intuitive way to explore the contents of the file.
- **Language Model Integration**: Utilize Langchain to perform inferencing with a language model, enabling intelligent responses based on user queries related to the CSV data.

## Project Structure

```
langchain-csv-chat
├── src
│   ├── app.py                # Main entry point for the Streamlit application
│   ├── components
│   │   ├── chat.py           # Chat interface component
│   │   └── csv_visualizer.py  # CSV visualization component
│   ├── utils
│   │   ├── csv_processor.py   # CSV processing utilities
│   │   └── llm_interface.py    # Language model interaction utilities
│   └── config.py             # Configuration settings
├── requirements.txt           # Project dependencies
├── .env.example               # Environment variable template
└── README.md                  # Project documentation
```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/langchain-csv-chat.git
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
   - Copy `.env.example` to `.env` and fill in the necessary values.

## Usage

To run the application, execute the following command:
```
streamlit run src/app.py
```

Open your web browser and navigate to `http://localhost:8501` to access the application.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.