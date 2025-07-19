import pandas as pd
from ydata_profiling import ProfileReport


def main():
    """
    Main function to load and display a CSV file.
    """
    df = read_csv('data/the_oscar_award.csv')
    if df is None:
        print("No data to display.")
        return
    df = clean_and_transform(df)


def clean_and_transform(df):
    """
    Cleans and transforms the DataFrame.
    - Shows variable types
    - Handles missing values
    - Strips whitespace from object columns
    - Drops duplicates
    """
    print("DataFrame Info (before cleaning):")
    print(df.info())
    print("\nMissing values per column:")
    print(df.isnull().sum())

    # name and film have null or empty values, drop those rows
    # used copy instead of inplace to avoid SettingWithCopyWarning
    df = df.dropna(subset=['name', 'film']).copy()

    for col in df.select_dtypes(include=['object']).columns:
        df.loc[:, col] = df[col].str.strip()

    # delete duplicated data
    df = df.drop_duplicates()

    print("\nDataFrame Info (after cleaning):")
    print(df.info())
    print("\nMissing values per column (after cleaning):")
    print(df.isnull().sum())
    print(f"DataFrame cleaned and transformed. Shape: {df.shape}")
    return df


def read_csv(file_path):
    """
    Reads a CSV file and returns a DataFrame.
    """
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"Error reading file: {e}")
        return None
    print(f"DataFrame loaded from {file_path}")
    print(f"Total Rows: {df.shape[0]}, Total Columns: {df.shape[1]}")
    return df


if __name__ == "__main__":
    main()
