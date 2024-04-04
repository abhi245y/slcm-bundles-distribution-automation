import os
import pathlib
import time
from typing import List
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
import yaml
import json
import nopecha
import requests
import base64
import urllib3

urllib3.disable_warnings(urllib3.exceptions.HTTPWarning)

driver = webdriver.Chrome()

driver.get("https://examerp.keralauniversity.ac.in/")

with open('./configs/configurations.yaml', 'r') as file:
    configurations = yaml.safe_load(file)

mergedOutputFolderPath: str = configurations['mergedOutputFolderPath']
undallocatedBundlesFolder: str = configurations["undallocatedBundlesFolder"]

def apply_styles(worksheet, df, workbook):
    worksheet.set_column('A:A', 42 / 7)  # Sl.No.
    worksheet.set_column('B:B', 105 / 7)  # Bundle Code
    worksheet.set_column('C:C', 62 / 7)  # AS Count
    worksheet.set_column('D:D', 171 / 7)  # Course Name
    worksheet.set_column('E:E', 140 / 7)  # District
    worksheet.set_column('F:F', 67 / 7)  # Camp
    worksheet.set_column('G:G', 66 / 7)  # Status

    worksheet.set_default_row(39)

    align_format = workbook.add_format({
        'align': 'center',
        'valign': 'vcenter',
        'text_wrap': True
    })

    worksheet.set_margins(left=0.25, right=0.25, top=0.6, bottom=0.3)

    header_format = workbook.add_format({
        'font_size': 15,
        'bold': True,
        'underline': True
    })
    worksheet.set_header('&C&"Arial"&BSecond Semester PG November 2023&"', {'header_header_spacing': 0.3, 'font': header_format})

    # Apply alignment and wrap text to data cells
    for row_num, row_data in enumerate(df.values):
        for col_num, cell_value in enumerate(row_data):
            worksheet.write(row_num + 1, col_num, str(cell_value), align_format)
    
    worksheet.repeat_rows(0)  

    (max_row, max_col) = df.shape
    column_settings = [{"header": column} for column in df.columns]
    worksheet.add_table(0, 0, max_row, max_col - 1, {"columns": column_settings})

def auto_login(capcha_link: str):
    """
    Auto login to the website when the cookies are expired
    Args:
        capcha_link (str): URL of the capcha image
    """
    print("Fetching captcha solution...")
    nopecha.api_key = configurations['nopecha']

    response = requests.get(capcha_link, verify=False)
    image_data = response.content
    base64_image = base64.b64encode(image_data).decode('utf-8')

    cpacha_text = nopecha.Recognition.solve(
        type='textcaptcha',
        image_data=[base64_image],
    )

    driver.find_element(By.ID, 'username').send_keys(configurations['username'])
    driver.find_element(By.ID, 'password').send_keys(configurations['password'])

    capcha_filed = driver.find_element(By.ID, 'id_captcha_1')
    capcha_filed.clear()
    capcha_filed.send_keys(cpacha_text[0])
    driver.find_element(By.CLASS_NAME, 'btn-primary').click()

def add_cookies(cookies: List[dict]) -> None:
    """
    Adds cookies to the driver for session management.

    Args:
        cookies (List[dict]): List of cookie dictionaries.
    """
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.get("https://examerp.keralauniversity.ac.in/cd-unit/qpcode-wise-bundle-list")

def style_merged_table(merged_data, output_file):
    df = merged_data
    writer = pd.ExcelWriter(output_file, engine='xlsxwriter')
    workbook = writer.book
    df.drop(df.columns[[0]], axis=1, inplace=True)

    for camp in df['Camp'].unique():
        try:
            new_df = df[df['Camp'] == camp]
            new_df.to_excel(writer, sheet_name=camp, index=False, startrow=1, header=False)

            worksheet = writer.sheets[camp]
            apply_styles(worksheet, new_df, workbook)
        except:
            new_df = df[df['Camp'].isnull()]
            new_df.to_excel(writer, sheet_name='Generated', index=False, startrow=1, header=False)

            worksheet = writer.sheets['Generated']
            apply_styles(worksheet, new_df, workbook)
    writer.close()

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
    # merged_data.to_excel(output_file, index=False)

    style_merged_table(merged_data,output_file)
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
    output_file = mergedOutputFolderPath+ exam_name + "_combined.xlsx"
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
    qp_code_details_grabber(qp_codes, str(path) + "/", exam_name)

def check_cookies() -> None:
    """
    Checks if the existing cookies are valid, and if not, prompts for re-login.
    """
    cookies_path = "./configs/cookies.json"
    print("Checking Cookies")

    def create_cookies() -> None:
        with open(cookies_path, "w") as f:
            f.write(json.dumps(driver.get_cookies(), indent=4))
        print("Cookies captured. Redirecting...")
        driver.get("https://examerp.keralauniversity.ac.in/cd-unit/qpcode-wise-bundle-list")
        
    if os.path.exists(cookies_path):
        with open(cookies_path, "r") as f:
            try:
                cookies = json.load(f)
                if cookies[0]['expiry'] <= int(time.time()):
                    try:
                        print("!! Previous Cookies has been expired !!, trying auto login")
                        capcha_link = driver.find_element(By.CLASS_NAME, 'captcha').get_attribute("src")
                        auto_login(capcha_link)
                    except:
                        input("!! Auto login Failed !!, please do relogin and press enter after login completion...")
                        
                    with open(cookies_path, "w") as f:
                        f.write(json.dumps(driver.get_cookies(), indent=4))
                else:
                    print("Redirecting...")
                    add_cookies(cookies)
            except:
                input("Cookies Error, please do relogin and press enter after login completion...")
                create_cookies()
                pass
    else:
        try:
            print("!! No cookies created !!, trying auto login")
            capcha_link = driver.find_element(By.CLASS_NAME, 'captcha').get_attribute("src")
            auto_login(capcha_link)
        except Exception as e:
            print(e)
            input("!! Auto login Failed !!, please do relogin and press enter after login completion...")
        create_cookies()
    

if __name__ == "__main__":
    # input("Press Enter after the page loads")
    check_cookies()
    auto_qp_series_generator(configurations["qpSeries"], int(configurations["qpStartRange"]), int(configurations["qpEndRange"]), configurations["examName"])
    
