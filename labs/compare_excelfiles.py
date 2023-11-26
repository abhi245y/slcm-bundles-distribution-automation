
# Experimental stuff. Still woking on this.

import pandas as pd
import pprint

# Define the paths to the two Excel files
# file1_path = r"D:\\backup\\myCodingLife\\campDistributionApp\\Grabbed_Results\\S1 B.Ed, April 2023 R 6789.xlsx"
# file2_path = r"D:\backup\\myCodingLife\\campDistributionApp\\Generated_Distributions\\S1 B.Ed Camp Distribution QP Code R 6789.xlsx"

examName = ""

file1_path = "./merged_outputs/merged_S1_PG_May_2023_Unallocated.xlsx"
file2_path = "./merged_outputs/merged_distribution_S1_PG_May_2023.xlsx"



# def compare_excel_files(folder_path, output_file):
#     # Initialize an empty DataFrame to store the merged data
#     merged_data = pd.DataFrame()

#     # Loop through all files in the specified folder
#     for file in os.listdir(folder_path_1):
#         # Check if the file is an Excel file with .xlsx extension
#         if file.startswith(examName) and file.endswith(".xlsx"):
#             file_path = os.path.join(folder_path, file)

#             # Read the Excel file into a DataFrame
#             data = pd.read_excel(file_path)

#     # Save the merged data to a new Excel file
#     merged_data.to_excel(output_file, index=False)
#     print(f"Merged data saved to {output_file}")

# Read the Excel files into Pandas dataframes
df1 = pd.read_excel(file1_path)
df2 = pd.read_excel(file2_path)

# Get the bundle codes from each dataframe
bundle_codes1 = df1['Bundle\xa0Code']
bundle_codes2 = df2['Bundle Code']

# Check if all bundle codes from file1 are present in file2
are_all_present = bundle_codes1.isin(bundle_codes2).all()

if are_all_present:
    print("All bundle codes Present")
else:
    missing_bundles = sorted(bundle_codes1[~bundle_codes1.isin(bundle_codes2)], reverse=True)
    print("The following bundles are missing")
    pprint.pprint(missing_bundles)
    print("Missing:",len(missing_bundles))