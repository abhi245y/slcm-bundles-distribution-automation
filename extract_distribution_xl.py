import openpyxl
import json
import pandas as pd

# Function which extract details form the excel file which contains details of camp distribution and converts them to excel for easy processing
def extract_data_from_excel(filename):
    df = pd.read_excel(filename)
    
    extracted_data = []
    
    for index, row in df.iterrows():
        qp_code = int(row['QP_Code']) if pd.notna(row['QP_Code']) else 0
        tvm = int(row['TVM']) if pd.notna(row['TVM']) else 0
        klm = int(row['KLM']) if pd.notna(row['KLM']) else 0
        pdlm = int(row['PDLM']) if pd.notna(row['PDLM']) else 0
        alp = int(row['ALP']) if pd.notna(row['ALP']) else 0
        total =  int(row['Total_Count'])
        
        data_dict ={
            "Qp_Code": qp_code,
            "Thiruvananthapuram": tvm,
            "Kollam": klm,
            "Pathanamthitta": pdlm,
            "Alappuzha": alp,
            "Total": total
        }
        extracted_data.append(data_dict)
    
    return extracted_data

def startExtraction(excel_file):
    return extract_data_from_excel(excel_file)