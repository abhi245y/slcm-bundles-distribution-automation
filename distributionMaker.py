import extract_distribution_xl as e_dxl
import four_camp_distribution as four_cd
import pandas as pd
import yaml

# Loading configurations from a YAML file
with open('configurations.yaml', 'r') as file:
    configurations = yaml.safe_load(file)

distribution_excel_filepath: str = configurations["distributionDetailsFile"]
bundle_details_excel_files_folderpath: str = configurations["undallocatedBundlesFolder"]
generated_distributions_folderpath: str = configurations["generatedDistributionsSaveFolder"]

distribution_places: list = configurations["campList"]
qp_code_letter: str = configurations["qpSeries"]
course_and_sem_name: str = configurations["examName"]

def add_data(data: dict, camp: str, bundle_code: str, value: int, district: str, total_value: int) -> None:
    """
    Adds bundle code details to a dictionary.

    Args:
    data (dict): Dictionary to store data.
    camp (str): Camp information.
    bundle_code (str): Bundle code.
    value (int): Value associated with the bundle.
    district (str): District name.
    total_value (int): Total value for the bundle.
    """
    data["Camp"].append(camp)
    data["Bundle Code"].append(bundle_code)
    data["Value"].append(value)
    data["District"].append(district)
    data["Total Value"].append(total_value)

def save_distribution_to_excel(generated_distribution: dict) -> None:
    """
    Saves the generated distribution of each QP code to an Excel file.

    Args:
    generated_distribution (dict): The distribution data to be saved.
    """
    data = {
        "Camp": [],
        "Bundle Code": [],
        "Value": [],
        "District": [],
        "Total Value": []
    }
    for place in distribution_places:
        camp = f"{place}"
        for packet_id, value, origin_place in generated_distribution[place]:
            total_value = sum(value for _, value, _ in generated_distribution[place])
            add_data(data, camp, packet_id, value, origin_place, total_value)

    df = pd.DataFrame(data)
    file_name = f"{course_and_sem_name} Camp Distribution QP Code {qp_code_letter} {distributionData['Qp_Code']}"
    output_file = f"{generated_distributions_folderpath}/{file_name}.xlsx"
    df.to_excel(output_file, index=False)

if __name__ == "__main__":
    list_of_distribution = e_dxl.start_extraction(distribution_excel_filepath)

    for distribution_data in list_of_distribution:
        print(f"Generating Distribution for QP Code: {distribution_data['Qp_Code']}")
        generated_distribution = four_cd.main(distribution_data, distribution_places, course_and_sem_name, bundle_details_excel_files_folderpath)
        save_distribution_to_excel(generated_distribution)
