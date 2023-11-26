import os
import pathlib
import time
from typing import List, Tuple

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
import yaml

driver = webdriver.Chrome()

driver.get("https://examerp.keralauniversity.ac.in/")

with open('configurations.yaml', 'r') as file:
    configurations = yaml.safe_load(file)

mergedOutputFolderPath: str = configurations['mergedOutputFolderPath']
undallocatedBundlesFolder: str = configurations["undallocatedBundlesFolder"]

def add_cookies(csrftoken: str, sessionid: str, expiry: int) -> None:
    """
    Adds cookies to the driver for session management.

    Args:
    csrftoken (str): CSRF token for the session.
    sessionid (str): Session ID token.
    expiry (int): Expiry time for the cookies.
    """
    cookies = [
        {'domain': 'examerp.keralauniversity.ac.in', 'expiry': expiry, 'httpOnly': True, 'name': 'sessionid', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': sessionid},
        {'domain': 'examerp.keralauniversity.ac.in', 'expiry': expiry, 'httpOnly': False, 'name': 'csrftoken', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': csrftoken}
    ]
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.get("https://examerp.keralauniversity.ac.in/cd-unit/qpcode-wise-bundle-list")

def merge_excel_files(folder_path: str, output_file: str, exam_name: str) -> None:
    """
    Merges multiple Excel files in a given folder into one output file.

    Args:
    folder_path (str): Path to the folder containing Excel files.
    output_file (str): Path to the output Excel file.
    exam_name (str): Name of the exam, used to filter the files.
    """
    merged_data = pd.DataFrame()
    for file in os.listdir(folder_path):
        if file.startswith(exam_name) and file.endswith(".xlsx"):
            file_path = os.path.join(folder_path, file)
            data = pd.read_excel(file_path)
            merged_data = pd.concat([merged_data, data], ignore_index=True)
    merged_data.to_excel(output_file, index=False)
    print(f"Merged data saved to {output_file}")

def check_qp(table: BeautifulSoup, target_qp: str) -> str:
    """
    Checks if the scraped QP code matches the target QP code.

    Args:
    table (BeautifulSoup): The parsed HTML table.
    target_qp (str): Target QP code to match.

    Returns:
    str: Result of the check ('success', 'try again', or 'empty').
    """
    data_tables_empty_td = table.find('tr', class_='odd').find('td', class_='dataTables_empty') if table.find('tr', class_='odd') else None
    if data_tables_empty_td is None:
        qp_in_table = table.find('tr', class_='odd').find_all('td')[2].text.strip()[:6]
        return "success" if qp_in_table == target_qp else "try again"
    else:
        return "empty"

def grab_bundle_codes_from_source(turn: int, data: List[List[str]], file_name: str, qp_code: str, folder_path: str) -> None:
    """
    Scrapes and converts an HTML table with bundle details to an Excel file.
    Each file is saved per QP code and all files are merged into one Excel file.

    Args:
    turn (int): Indicates the iteration number.
    data (List[List[str]]): Data to be written to the file.
    file_name (str): Name of the file to be created.
    qp_code (str): QP code for filtering.
    folder_path (str): Path to the folder where the file will be saved.
    """
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")

    table = soup.find("table", {"id": "style-2"})
    check_res = check_qp(table, qp_code)
    print("Checking QP: ", check_res)
    if check_res == 'success':
        if turn == 1:
            data.clear()
            for row in table.find_all("thead"):
                row_data = [cell.get_text(strip=True) for cell in row.find_all("th") if cell.get_text(strip=True) != "c"]
                if row_data:
                    data.append(row_data)
        for row in table.find_all("tr"):
            row_data = [cell.get_text(strip=True) for cell in row.find_all("td") if cell.get_text(strip=True) != "c"]
            if row_data:
                data.append(row_data)
        print("Grabbed: ", data[-1])
        df = pd.DataFrame(data[1:], columns=data[0])
        final_file_name = str(folder_path) + str(file_name)
        df.to_excel(final_file_name + ".xlsx", index=False)
    elif check_res == 'empty':
        pass

def qp_code_details_grabber(qp_codes: List[str], path: str, exam_name: str) -> None:
    """
    Submits each QP code to the webpage and grabs the HTML code.

    Args:
    qp_codes (List[str]): List of QP codes.
    path (str): Path to save the output files.
    exam_name (str): Name of the exam.
    """
    for i, qp_code in enumerate(qp_codes, start=1):
        print("Grabbing:", qp_code)
        qpCodeInputTag = driver.find_element(By.ID, "qp_code")
        driver.execute_script('document.getElementById("qp_code").value = ""')
        time.sleep(1)
        qpCodeInputTag.send_keys(qp_code)
        submit_button = driver.find_element(By.ID, "submit_button")
        submit_button.click()
        wait = WebDriverWait(driver, 100)
        try:
            wait.until_not(EC.presence_of_element_located((By.CLASS_NAME, "blockOverlay")))
            select_element = Select(driver.find_element(By.NAME, "style-2_length"))
            select_element.select_by_value("1000")
            try:
                grab_bundle_codes_from_source(1, [], exam_name + " " + qp_code, qp_code, path)
                time.sleep(2)
            except Exception as e:
                print(f"Error in {qp_code}. Skipping. Error: {e}")
                pass
        except TimeoutException:
            print('Error Reloading Page')
            driver.refresh()
    output_file = mergedOutputFolderPath + exam_name + "_combined.xlsx"
    merge_excel_files(path, output_file, exam_name)

def auto_qp_series_generator(series: str, range_start: int, range_end: int, exam_name: str) -> None:
    """
    Generates a series of QP codes based on user input and processes them.

    Args:
    series (str): Series identifier (e.g., 'P', 'Q', 'R').
    range_start (int): Starting range of QP codes.
    range_end (int): Ending range of QP codes.
    exam_name (str): Name of the exam.
    """
    qp_codes = [series + ' ' + str(i) for i in range(range_start, range_end + 1)]
    pathlib.Path(mergedOutputFolderPath).mkdir(parents=True, exist_ok=True) 
    path = pathlib.Path(undallocatedBundlesFolder + exam_name)
    path.mkdir(parents=True, exist_ok=True)
    print(path)
    qp_code_details_grabber(qp_codes, str(path) + "/", exam_name)

if __name__ == "__main__":
    add_cookies("", "", "")
    input("Press Enter after login completion...")
    # cookies = driver.get_cookies()
    # print(cookies)
    auto_qp_series_generator(input("Enter Series (P, Q, R..): "), int(input("Enter Start Range: ")), int(input("Enter End Range: ")), input("Enter Exam Name: "))
