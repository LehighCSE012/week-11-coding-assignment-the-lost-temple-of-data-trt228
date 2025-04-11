"""
Adventure Parser Module

This module provides functions to process archaeological data files including:
- Excel files with artifact data
- TSV files with location notes
- Text journal entries with dates and secret codes
"""

import pandas as pd
import re

def load_artifact_data(excel_filepath):
    """
    Reads artifact data from a specific sheet ('Main Chamber') in an Excel file,
    skipping the first 3 rows.

    Args:
        excel_filepath (str): The path to the artifacts Excel file.

    Returns:
        pandas.DataFrame: DataFrame containing the artifact data.
    """
    artifact_df = pd.read_excel(excel_filepath, sheet_name='Main Chamber', skiprows=3)
    return artifact_df

def load_location_notes(tsv_filepath):
    """
    Reads location data from a Tab-Separated Value (TSV) file.

    Args:
        tsv_filepath (str): The path to the locations TSV file.

    Returns:
        pandas.DataFrame: DataFrame containing the location data.
    """
    location_df = pd.read_csv(tsv_filepath, sep='\t')
    return location_df

def extract_journal_dates(journal_text):
    """
    Extracts all valid dates in MM/DD/YYYY format from the journal text.
    Only returns dates where:
    - Month is between 01-12
    - Day is between 01-31 (doesn't validate specific month lengths)
    - Year is between 1000-2999

    Args:
        journal_text (str): The full text content of the journal.

    Returns:
        list[str]: A list of valid date strings found in the text.
    """
    date_pattern = r"\b(0[1-9]|1[0-2])/(0[1-9]|[12][0-9]|3[01])/([12]\d{3})\b"
    found_dates = re.findall(date_pattern, journal_text)
    return ['/'.join(date) for date in found_dates]

def extract_secret_codes(journal_text):
    """
    Extracts all secret codes in AZMAR-XXX format (XXX are digits) from the journal text.

    Args:
        journal_text (str): The full text content of the journal.

    Returns:
        list[str]: A list of secret code strings found in the text.
    """
    code_pattern = r"AZMAR-\d{3}"
    found_codes = re.findall(code_pattern, journal_text)
    return found_codes


# --- Optional: Main execution block for your own testing ---
if __name__ == '__main__':
    # Define file paths (adjust if your files are located elsewhere)
    EXCEL_FILE = 'artifacts.xlsx'
    TSV_FILE = 'locations.tsv'
    JOURNAL_FILE = 'journal.txt'

    print(f"--- Loading Artifact Data from {EXCEL_FILE} ---")
    try:
        ARTIFACTS_DF = load_artifact_data(EXCEL_FILE)
        print("Successfully loaded DataFrame. First 5 rows:")
        print(ARTIFACTS_DF.head())
        print("\nDataFrame Info:")
        ARTIFACTS_DF.info()
    except FileNotFoundError:
        print(f"Error: File not found at {EXCEL_FILE}")

    print(f"\n--- Loading Location Notes from {TSV_FILE} ---")
    try:
        LOCATIONS_DF = load_location_notes(TSV_FILE)
        print("Successfully loaded DataFrame. First 5 rows:")
        print(LOCATIONS_DF.head())
        print("\nDataFrame Info:")
        LOCATIONS_DF.info()
    except FileNotFoundError:
        print(f"Error: File not found at {TSV_FILE}")

    print(f"\n--- Processing Journal from {JOURNAL_FILE} ---")
    try:
        with open(JOURNAL_FILE, 'r', encoding='utf-8') as file:
            JOURNAL_CONTENT = file.read()

        print("\nExtracting Dates...")
        DATE_LIST = extract_journal_dates(JOURNAL_CONTENT)
        print(f"Found dates: {DATE_LIST}")

        print("\nExtracting Secret Codes...")
        CODE_LIST = extract_secret_codes(JOURNAL_CONTENT)
        print(f"Found codes: {CODE_LIST}")

    except FileNotFoundError:
        print(f"Error: File not found at {JOURNAL_FILE}")
