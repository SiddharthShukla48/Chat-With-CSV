def process_csv(file_path):
    import pandas as pd

    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        raise ValueError(f"Error processing CSV file: {e}")

def validate_csv(df):
    required_columns = ['column1', 'column2']  # Replace with actual required columns
    for column in required_columns:
        if column not in df.columns:
            raise ValueError(f"Missing required column: {column}")
    return True