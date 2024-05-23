import pandas as pd
from typing import List, Dict

def extract_data_from_excel(filename: str) -> List[Dict[str, int]]:
    """
    Extracts details from the excel file containing camp distribution data and converts them into a list of dictionaries for easy processing.

    Args:
        filename (str): The name of the excel file to be processed.

    Returns:
        List[Dict[str, int]]: A list of dictionaries containing extracted data.
    """
    df = pd.read_excel(filename)
    extracted_data = []

    for _, row in df.iterrows():
        data_dict = {
            "Qp_Code": int(row['QP_Code']) if pd.notna(row['QP_Code']) else 0,
            "Thiruvananthapuram": int(row['TVM']) if pd.notna(row['TVM']) else 0,
            "Kollam": int(row['KLM']) if pd.notna(row['KLM']) else 0,
            "Pathanamthitta": int(row['PDLM']) if pd.notna(row['PDLM']) else 0,
            "Alappuzha": int(row['ALP']) if pd.notna(row['ALP']) else 0,
            "Total": int(row['Total_Count'])
        }
        extracted_data.append(data_dict)
    
    return extracted_data

def start_extraction(excel_file: str) -> List[Dict[str, int]]:
    """
    Initiates the extraction process of the Excel file.
    
    Args:
        excel_file (str): The path to the Excel file to be processed.

    Returns:
        List[Dict[str, int]]: Extracted data as a list of dictionaries.
    """
    return extract_data_from_excel(excel_file)
